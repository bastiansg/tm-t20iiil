import json
from itertools import islice
from pathlib import Path

from escpos.printer import Usb

from tm_t20iiil.printer import print_and_wait

STUDIO_SEPARATOR = "#" * 48
ITEM_SEPARATOR = "-" * 48
QR_PATH = Path("resources/acopio/acopio-qr.png")

SECTION_IMAGES = {
    "2 * BOUGIE WOOGIE": (
        Path("resources/acopio/images/01-bougie-woogie.png"),
    ),
    "3 * DE LA FORMA": (Path("resources/acopio/images/01-de-la-forma.png"),),
    "7 * ITEM": (Path("resources/acopio/images/01-items.png"),),
    "10 * JUAN CRUZ": (
        Path("resources/acopio/images/01-juan-cruz.png"),
        Path("resources/acopio/images/02-juan-cruz.png"),
        Path("resources/acopio/images/03-juan-cruz.png"),
    ),
    "11 * LO ENCONTRADO": (
        Path("resources/acopio/images/01-lo-encontrado.png"),
    ),
    "12 * MARÍA EGAN": (Path("resources/acopio/images/01-maria-egan.png"),),
    "14 * LA POLTRONA": (Path("resources/acopio/images/01-la-poltrona.png"),),
    "16 * PEDRO LEAL": (Path("resources/acopio/images/01-pedro-leal.png"),),
}

ENTRIES = json.loads(
    Path(__file__).with_name("acopio.json").read_text(encoding="utf-8")
)


def get_printer() -> Usb:
    return Usb(
        0x04B8,
        0x0E27,
        0,  # type: ignore
        profile="TM-T20II",
    )


def print_item(printer: Usb, item: dict[str, str]) -> None:
    for field in ("title", "description", "measures", "year", "price"):
        printer.block_text(item[field])
        printer.text("\n")


def print_entry(
    printer: Usb,
    heading: str,
    items: list[dict[str, str]],
) -> None:
    printer.block_text(STUDIO_SEPARATOR)
    printer.text("\n\n")
    printer.set(bold=True)
    printer.block_text(heading)
    printer.set(bold=False)
    printer.text("\n\n")

    for index, item in enumerate(items):
        if index:
            printer.text("\n")
            printer.block_text(ITEM_SEPARATOR)
            printer.text("\n\n")

        print_item(printer, item)

    for image_path in SECTION_IMAGES.get(heading, ()):
        printer.image(str(image_path), center=True)

    printer.text("\n")


def print_acopio(printer: Usb, limit: int | None = None) -> None:
    printer.text("\n\n")
    printer.set(
        bold=True,
        align="left",
        font=0,  # type: ignore
        double_width=False,
        double_height=False,
    )

    printer.block_text("LISTADO")
    printer.text("\n\n\n")

    for entry in islice(ENTRIES, limit):
        print_entry(printer, entry["title"], entry["items"])

    printer.block_text(STUDIO_SEPARATOR)
    printer.text("\n\n\n\n")
    printer.set(align="center")
    printer.block_text("Curaduría: Delfina Rabán ACOPIO")
    printer.text("\n\n\n\n")
    printer.image(str(QR_PATH), center=True)
    printer.text("\n")
    printer.cut()


def main() -> None:
    printer = get_printer()
    try:
        print_and_wait(printer, print_acopio)
    finally:
        printer.close()


if __name__ == "__main__":
    main()
