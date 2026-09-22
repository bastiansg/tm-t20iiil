from collections.abc import Callable
from dataclasses import dataclass
from time import monotonic

from escpos.printer import Usb
from usb.core import USBTimeoutError

from tm_t20iiil.printer.config import config
from tm_t20iiil.utils.console import (
    render_print_completed,
    render_print_started,
)


@dataclass(frozen=True, slots=True)
class PrintStatus:
    raw: int
    paper_near_end: bool
    paper_out: bool


def print_and_wait(
    printer: Usb,
    print_job: Callable[[Usb], None],
    timeout: float = 30,
) -> PrintStatus:
    if timeout <= 0:
        raise ValueError("'timeout' must be greater than zero")

    render_print_started()
    print_job(printer)
    printer._raw(config.print_completion_command)

    device = printer.device
    if device is None:
        raise RuntimeError("The printer USB connection is not open")

    deadline = monotonic() + timeout
    raw_status = None
    while raw_status is None:
        remaining_timeout = deadline - monotonic()
        if remaining_timeout <= 0:
            raise TimeoutError(
                f"The printer did not confirm completion within {timeout} seconds"
            )

        try:
            response = device.read(
                printer.in_ep,
                16,
                timeout=max(1, round(remaining_timeout * 1000)),
            )

        except USBTimeoutError as error:
            raise TimeoutError(
                f"The printer did not confirm completion within {timeout} seconds"
            ) from error

        raw_status = next(
            (
                int(value)
                for value in response
                if (int(value) & config.status_format_mask)
                == config.status_format_value
            ),
            None,
        )

    status = PrintStatus(
        raw=raw_status,
        paper_near_end=bool(raw_status & config.paper_near_end_mask),
        paper_out=bool(raw_status & config.paper_out_mask),
    )

    render_print_completed()

    return status
