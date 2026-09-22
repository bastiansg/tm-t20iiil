from functools import partial

from tm_t20iiil.printer import print_and_wait
from tm_t20iiil.prints.acopio import get_printer, print_acopio


def main() -> None:
    printer = get_printer()
    try:
        print_and_wait(printer, partial(print_acopio, limit=3))
    finally:
        printer.close()


if __name__ == "__main__":
    main()
