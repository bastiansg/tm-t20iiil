import re
import subprocess
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageFilter, ImageOps

from tm_t20iiil.scripts.acopio.config import config


def convert_image(source_path: Path, destination_directory: Path) -> None:
    image_config = config.images[source_path.name]
    orientation = image_config.orientation
    brightness_threshold = image_config.brightness_threshold
    horizontal_margin = image_config.horizontal_margin

    with Image.open(source_path) as source_image:
        image = ImageOps.exif_transpose(source_image).convert("RGBA")
        aspect_ratio = image.height / image.width

    width, height = config.get_image_size(orientation, aspect_ratio)
    content_scale = 1 - 2 * horizontal_margin
    width = round(width * content_scale)
    height = round(height * content_scale)
    if height > config.max_height:
        width = round(width * config.max_height / height)
        height = config.max_height

    canvas = Image.new("RGBA", image.size, "white")
    canvas.alpha_composite(image)

    bitmap = BytesIO()
    canvas.convert("L").filter(ImageFilter.MinFilter(3)).save(bitmap, format="PPM")

    destination_path = destination_directory / f"{source_path.stem}.svg"
    subprocess.run(
        (
            "potrace",
            "--svg",
            "--flat",
            "--tight",
            "--blacklevel",
            str(brightness_threshold),
            "--output",
            destination_path,
            "-",
        ),
        input=bitmap.getvalue(),
        check=True,
    )

    svg = destination_path.read_text(encoding="utf-8")
    svg = re.sub(
        r' width="[^"]+" height="[^"]+"',
        f' width="{width}" height="{height}"',
        svg,
        count=1,
    )
    destination_path.write_text(svg, encoding="utf-8")
    png_path = destination_path.with_suffix(".png")
    subprocess.run(
        (
            "rsvg-convert",
            "--background-color",
            "white",
            "--output",
            png_path,
            destination_path,
        ),
        check=True,
    )

    with Image.open(png_path) as rendered_image:
        black_and_white_image = rendered_image.convert("L").point(
            lambda pixel: 255 * (pixel > 127),
            mode="1",
        )

        output_width = round(width / content_scale)
        output_image = Image.new("1", (output_width, height), 1)
        output_image.paste(
            black_and_white_image,
            ((output_width - width) // 2, 0),
        )

        output_image.save(png_path)

    print(f"{source_path.name}: {orientation} -> {destination_path}")


def main() -> None:
    config.images_directory.mkdir(parents=True, exist_ok=True)
    source_paths = (
        path
        for path in sorted(config.raw_images_directory.iterdir())
        if path.is_file() and path.suffix.lower() in config.supported_formats
    )

    for source_path in source_paths:
        convert_image(source_path, config.images_directory)


if __name__ == "__main__":
    main()
