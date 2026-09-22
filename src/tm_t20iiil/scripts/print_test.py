from escpos.printer import Usb

from tm_t20iiil.printer import print_and_wait

SEPARATOR = "------------------------------------------------"


def get_printer() -> Usb:
    return Usb(
        0x04B8,
        0x0E27,
        0,  # type: ignore
        profile="TM-T20II",
    )


def print_test_ticket(printer: Usb) -> None:
    printer.text("\n\n")
    printer.set(
        bold=True,
        align="center",
        font=0,  # type: ignore
        double_width=False,
        double_height=False,
    )

    printer.block_text("* TM-T20IIIL PRINT TEST *")
    printer.set(bold=False)
    printer.text("\n\n")

    printer.text(SEPARATOR)
    printer.text("\n\n")

    printer.set(bold=True, align="center")
    printer.block_text("The printer is working correctly.")
    printer.set(bold=False)
    printer.text("\n\n")

    printer.text(SEPARATOR)
    printer.text("\n\n")

    printer.set(bold=True, align="left")
    printer.block_text("Normal text:")
    printer.set(bold=False)
    printer.text("\n")
    printer.block_text("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    printer.text("\n")
    printer.block_text("abcdefghijklmnopqrstuvwxyz")
    printer.text("\n")
    printer.block_text("0123456789")
    printer.text("\n\n")

    printer.set(align="center", font=1)  # type: ignore
    printer.set(bold=True)
    printer.block_text("TEST COMPLETE")
    printer.set(bold=False)
    printer.text("\n\n")
    printer.block_text("Ticket no válido como factura (:")
    printer.text("\n\n")

    printer.cut()


def main() -> None:
    printer = get_printer()
    try:
        print_and_wait(printer, print_test_ticket)
    finally:
        printer.close()


if __name__ == "__main__":
    main()
