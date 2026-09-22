from itertools import islice, repeat

from escpos.printer import Usb

from tm_t20iiil.printer import print_and_wait
from tm_t20iiil.prints.acopio import ITEM_SEPARATOR, get_printer

REPEAT_COUNT = 10
TEXT_BLOCK = (
    "apertura apertura apertura",
    "Local 6",
    "acopio",
    "Delaforma",
    "estudiojunto",
    "fzsmestudio",
)


def print_apertura(printer: Usb) -> None:
    printer.text("\n\n")
    printer.set(
        bold=True,
        align="left",
        font=0,  # type: ignore
        double_width=False,
        double_height=False,
    )

    for index, text_block in enumerate(repeat(TEXT_BLOCK, REPEAT_COUNT)):
        if index:
            printer.block_text(ITEM_SEPARATOR)
            printer.text("\n\n")

        printer.set(bold=True)
        printer.block_text(text_block[0])
        printer.text("\n")
        printer.set(bold=False)

        for line in islice(text_block, 1, None):
            printer.block_text(line)
            printer.text("\n")

        printer.text("\n")

    printer.cut()


def main() -> None:
    printer = get_printer()
    try:
        print_and_wait(printer, print_apertura)
    finally:
        printer.close()


if __name__ == "__main__":
    main()
