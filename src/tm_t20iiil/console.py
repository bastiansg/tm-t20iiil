from rich.console import Console
from rich.text import Text

console = Console()


def render_print_started() -> None:
    message = Text()
    message.append("\n┌─[ ", style="dim magenta")
    message.append("PRINTER", style="bold white")
    message.append(" ]\n", style="dim magenta")
    message.append("└──> ", style="dim magenta")
    message.append("PRINTING TICKET...\n", style="dim white")
    console.print(message)


def render_print_completed() -> None:
    message = Text()
    message.append(" :: ", style="dim magenta")
    message.append("PRINTER", style="bold white")
    message.append(" // ", style="dim magenta")
    message.append("PRINT COMPLETE", style="bold bright_cyan")
    console.print(message)
