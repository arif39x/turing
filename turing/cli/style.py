from rich.console import Console
from rich.theme import Theme

custom_theme = Theme({
    "error": "bold red",
    "warning": "bold yellow",
    "success": "bold green",
    "info": "cyan",
})

console = Console(theme=custom_theme)


def error(msg: str) -> None:
    console.print(f"[error]ERROR:[/error] {msg}")


def success(msg: str) -> None:
    console.print(f"[success]SUCCESS:[/success] {msg}")


def warning(msg: str) -> None:
    console.print(f"[warning]WARNING:[/warning] {msg}")


def info(msg: str) -> None:
    console.print(f"[info]INFO:[/info] {msg}")