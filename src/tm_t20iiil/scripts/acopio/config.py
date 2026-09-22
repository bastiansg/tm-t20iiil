from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field, PositiveInt
from pydantic_settings import BaseSettings


class ImageConfig(BaseModel):
    orientation: Literal["square", "portrait", "landscape"]
    brightness_threshold: float = Field(ge=0, le=1)


class Config(BaseSettings):
    base_width: PositiveInt = 576
    max_height: PositiveInt = 288
    raw_images_directory: Path = Path("resources/acopio/raw-images")
    images_directory: Path = Path("resources/acopio/images")
    supported_formats: frozenset[str] = frozenset({".jpeg", ".jpg", ".png"})
    images: dict[str, ImageConfig] = {
        "01-bougie-woogie.png": ImageConfig(
            orientation="portrait",
            brightness_threshold=0.8,
        ),
        "01-de-la-forma.png": ImageConfig(
            orientation="portrait",
            brightness_threshold=0.8,
        ),
        "01-items.png": ImageConfig(
            orientation="portrait",
            brightness_threshold=0.8,
        ),
        "01-juan-cruz.png": ImageConfig(
            orientation="portrait",
            brightness_threshold=0.8,
        ),
        "01-la-poltrona.jpeg": ImageConfig(
            orientation="portrait",
            brightness_threshold=0.6,
        ),
        "01-lo-encontrado.png": ImageConfig(
            orientation="portrait",
            brightness_threshold=0.8,
        ),
        "01-maria-egan.png": ImageConfig(
            orientation="landscape",
            brightness_threshold=0.8,
        ),
        "01-pedro-leal.png": ImageConfig(
            orientation="portrait",
            brightness_threshold=0.8,
        ),
        "02-juan-cruz.png": ImageConfig(
            orientation="square",
            brightness_threshold=0.8,
        ),
        "02-de-la-forma.png": ImageConfig(
            orientation="portrait",
            brightness_threshold=0.8,
        ),
        "03-juan-cruz.png": ImageConfig(
            orientation="portrait",
            brightness_threshold=0.8,
        ),
    }

    @property
    def image_sizes(self) -> dict[str, tuple[int, int]]:
        return {
            "square": (self.base_width, self.base_width),
            "landscape": (self.base_width, self.base_width // 2),
        }

    def get_image_size(
        self,
        orientation: Literal["square", "portrait", "landscape"],
        aspect_ratio: float,
    ) -> tuple[int, int]:
        if orientation == "portrait":
            return self.base_width, min(
                round(self.base_width * aspect_ratio),
                self.base_width * 2,
            )

        return self.image_sizes[orientation]


config = Config()
