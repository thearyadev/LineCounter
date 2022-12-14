#! /usr/bin/python
import argparse
import os
from rich import print


def display_single_err(prompt, path):
    print(f"[dim red]{prompt} {path}[/dim red]")


def display_single_file(line_count, path):
    print(f"[dim white]{line_count} {path}[/dim white]")


def get_line_count(path: str) -> int | None:
    try:
        with open(path, "r") as file:
            c = len(list(filter(lambda ln: ln != "\n", file.readlines())))

            display_single_file(c, os.path.relpath(path, os.curdir))
            return c

    except UnicodeDecodeError:
        display_single_err(":heavy_exclamation_mark:",
                           os.path.relpath(path, os.curdir))
        return None


def record_files(*, directory: str, ignore: list[str], extensions: list[str] | None = None) -> list[str]:
    if ignore is None:
        ignore = list()
    files_to_scan: list[str] = list()
    directory = os.path.abspath(directory)
    for scannedDir in os.listdir(directory):
        if scannedDir not in ignore:
            if os.path.isdir(os.path.abspath(f"{directory}/{scannedDir}")):
                for root, _, files in os.walk(os.path.abspath(f"{directory}/{scannedDir}")):
                    for f in files:
                        fp = os.path.abspath(f"{root}/{f}")
                        _, ext = os.path.splitext(fp)
                        if isinstance(extensions, list):
                            if ext in extensions:
                                files_to_scan.append(fp)
                        else:
                            files_to_scan.append(fp)
            else:
                fp = os.path.abspath(f"{directory}/{scannedDir}")
                _, ext = os.path.splitext(fp)
                if isinstance(extensions, list):
                    if ext in extensions:
                        files_to_scan.append(fp)
                else:
                    files_to_scan.append(fp)

    return files_to_scan


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--ignore", action="append", type=str, required=False,
                        help="Name of directory in target directory which should be ignored.")
    parser.add_argument("-e", "--extension", action="append", type=str, required=False, help="File extensions to accept")
    parser.add_argument("-d", "--directory", required=False, default="./", help="Directory to run scan")

    args = parser.parse_args()
    print(f"Selected Directory: [green]{args.directory}[/green]\n"
          f"Ignored Directories: [green]{args.ignore}[/green]\n"
          f"Searching for: [yellow]{args.extension if args.extension else 'All'}[/yellow]")
    lineCount: int = 0
    f = record_files(directory=args.directory, ignore=args.ignore, extensions=args.extension)
    for x in f:
        c: int = get_line_count(x)

        if isinstance(c, int):
            lineCount += c

    print(f"[bold yellow]Total: {lineCount}")


if __name__ == "__main__":
    main()
