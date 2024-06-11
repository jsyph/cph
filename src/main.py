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
import sys


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def load_template() -> Template:
    env = Environment(loader=FileSystemLoader(resource_path("")))
    return env.get_template("template.jinja.cpp")


def load_sources() -> dict[str, Any]:
    with open(resource_path("sources.toml"), mode="rb") as f:
        sources: dict[str, Any] = tomllib.load(f)
    return sources


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


def option_input(prompt: str, default: str) -> str:
    """
    Displays input prompt for user with options `y` and `n`
    Returns `True` if the user input is equal to `default` value
    """
    user_input = (
        input(normal_text(f"{prompt} [YNyn] [default: {default}]: ")) or default
    )
    user_input = user_input.lower()

    if user_input not in ["y", "n"]:
        print_error(f"{user_input} is invalid input")
        exit()

    return user_input


def main():
    sources: dict[str, Any] = load_sources()

    code_template: Template = load_template()

    if len(sys.argv) == 2:
        user_input: str = sys.argv[1]
    else:
        user_input: str = input(normal_text("Enter url or question number: "))

    url: ParseResult = urlparse(user_input)

    problem = Problem()
    source_data: dict[str, Any] = {}
    if url.scheme:
        # is url
        for name in sources:
            if url.netloc == sources[name]["domain"]:
                source_data = sources[name]
                break
        else:
            print_error(f"{url.netloc} is not supported")
            return

        if source_data.get("param"):
            problem.id = parse_qs(url.query)[source_data["param"]][0]
        else:
            for re_format in source_data["format"]:
                result = re.match(re_format, user_input)
                if result:
                    result_dict = result.groupdict()
                    problem.id = "".join([res for _, res in result_dict.items()])

        if problem.id == "":
            print_error(f"Failed to parse {user_input}")
            return
    else:
        problem.id = user_input.upper()
        source_data["name"] = input(normal_text("Enter source name: "))

    problem.source = source_data["name"]

    use_stdio_source_default = "y" if source_data.get("fileio") else "n"
    use_fileio = option_input("Use file IO?", use_stdio_source_default)

    if use_fileio == "y":
        problem.fileio = True
        same_file_name = option_input("    Same file name?", "y")
        if same_file_name:
            file_name = input(normal_text("        File name: "))

            problem.input_file_name = f"{file_name}.in"
            problem.output_file_name = f"{file_name}.out"

            print_normal(
                f"    Input  file name: {hightlight_text(problem.input_file_name)}"
            )
            print_normal(
                f"    Output file name: {hightlight_text(problem.output_file_name)}"
            )

            ok_file_names = option_input("Confirm? ", "y")
            if not ok_file_names:
                problem.input_file_name = input(normal_text("    Input  file  name: "))
                problem.output_file_name = input(normal_text("    Output file name: "))
        else:
            problem.input_file_name = input(normal_text("    Input  file  name: "))
            problem.output_file_name = input(normal_text("    Output file name: "))
    single_input: bool = option_input("Multiple Input?", "n") == "n"
    problem.multi_input = not single_input

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
        overwrite: bool = option_input("Overwrite?", "y") == "y"

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
