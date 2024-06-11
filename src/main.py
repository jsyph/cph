from text_formatter import *
from problem import Problem
from jinja2 import Environment, FileSystemLoader, Template
from urllib.parse import ParseResult, urlparse, parse_qs
import os
import subprocess
from datetime import datetime
import tomllib
import atexit
import re
from pathlib import Path
import sys

MAIN_FOLDER_PATH = Path(__file__).parent


def load_template() -> Template:
    env = Environment(loader=FileSystemLoader(MAIN_FOLDER_PATH))
    return env.get_template("template.jinja.cpp")


def open_nvim(file_path: str) -> None:
    nvim_open = option_input("Open nvim?", "y")
    if not nvim_open:
        return

    subprocess.call(["nvim", "+:1", "+/solve", "+noh", file_path])


def clang_format(filepath: str) -> str:
    res = subprocess.run(["clang-format", filepath], stdout=subprocess.PIPE, text=True)

    return res.stdout


def done_text(problem_file_name: str) -> None:
    print(
        success_text(f"🌟 Done 🌟\nFile name is ") + hightlight_text(problem_file_name)
    )


def option_input(prompt: str, default: str) -> bool:
    """
    Displays input prompt for user with options `y` and `n`
    Returns `True` if the user input is equal to `default` value
    """
    user_input = (
        input(normal_text(f"{prompt} [YNyn] [default: {default}]: ")) or default
    )
    user_input = user_input.lower()

    return user_input == default


def main():
    with open(f"{MAIN_FOLDER_PATH}/sources.toml", mode="rb") as f:
        sources: dict[str, Any] = tomllib.load(f)

    code_template: Template = load_template()

    if len(sys.argv) == 2:
        user_input: str = sys.argv[1]
    else:
        user_input: str = input(normal_text("Enter url or question number: "))

    url: ParseResult = urlparse(user_input)

    problem = Problem()
    if url.scheme:
        # is url
        for name in sources:
            if url.netloc == sources[name]["domain"]:
                website = sources[name]
                break
        else:
            print_error(f"{url.netloc} is not supported")
            return

        problem.source = website["name"]

        if website.get("param"):
            problem.id = parse_qs(url.query)[website["param"]][0]
        else:
            for re_format in website["format"]:
                result = re.match(re_format, user_input)
                if result:
                    result_dict = result.groupdict()
                    problem.id = "".join([res for _, res in result_dict.items()])

        if problem.id == "":
            print_error(f"Failed to parse {user_input}")
            return

    else:
        problem.id = user_input.upper()
        problem.source = input(normal_text("Enter source name: "))

    use_file_io: bool = option_input("Use file IO?", "n")

    if not use_file_io:
        problem.fileio = True
        problem.input_file_name = input(normal_text("    Input file name: "))
        problem.output_file_name = input(normal_text("    Output file name: "))

    multi_input: bool = option_input("Multiple Input?", "n")
    problem.multi_input = multi_input

    rendered_code = code_template.render(
        id=problem.id,
        source=problem.source,
        url=user_input if url.scheme else "-",
        start_time=datetime.now().strftime("%I:%M:%S %p on %Y/%m/%d"),
        file_input=problem.fileio,
        input_file=problem.input_file_name,
        output_file=problem.output_file_name,
        multi_input=problem.multi_input,
    )

    current_dir: str = os.getcwd()
    file_path: str = f"{current_dir}/{problem.file_name()}"

    if os.path.exists(file_path):
        print(
            f"{hightlight_text(problem.file_name())} {warning_text("already exists.")}"
        )
        overwrite: bool = option_input("Overwrite?", "y")

        if not overwrite:
            done_text(problem.file_name())
            open_nvim(file_path)
            return

    with open(file_path, "w") as file:
        file.write(rendered_code)

    formated_code = clang_format(file_path)

    with open(file_path, "w") as file:
        file.write(formated_code)

    done_text(problem.file_name())
    open_nvim(file_path)


if __name__ == "__main__":
    atexit.register(reset_all)
    main()
