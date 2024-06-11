from typing import Any
from colorama import Back, Fore, Style
from pprint import pprint


def normal_text(text: str) -> str:
    return Fore.WHITE + text + Fore.RESET


def success_text(text: str) -> str:
    return Fore.GREEN + text


def error_text(text: str) -> str:
    return Style.BRIGHT + Fore.RED + text


def hightlight_text(text: str) -> str:
    return Fore.LIGHTMAGENTA_EX + text


def warning_text(text: str) -> str:
    return Fore.YELLOW + text


def text_reset() -> str:
    return Style.RESET_ALL


def print_normal(text: str) -> None:
    print(normal_text(text))


def print_error(text: str) -> None:
    print(error_text(text))


def print_success(text: str) -> None:
    print(success_text(text))


def print_highlight(text: str) -> None:
    print(hightlight_text(text))


def print_warning(text: str) -> None:
    print(warning_text(text))


def pprint_debug(content: Any):
    print(Style.DIM + Fore.WHITE + Back.BLACK, end=None)
    pprint(content)
    print(Style.RESET_ALL, end=None)


def reset_all() -> None:
    print(text_reset(), end=None)
