import argparse
from typing import List

from conda.cli.helpers import (
    add_parser_channels,
    add_parser_default_packages,
    add_parser_json,
    add_parser_networking,
    add_parser_platform,
    add_parser_solver,
    add_parser_solver_mode,
    add_parser_show_channel_urls,
)

def parse_arguments(arguments: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    channel_options = add_parser_channels(parser)
    add_parser_platform(channel_options)

    solver_mode_options = add_parser_solver_mode(parser)
    add_parser_default_packages(solver_mode_options)
    add_parser_solver(solver_mode_options)

    add_parser_networking(parser)

    output_and_prompt_options = add_parser_json(parser)
    add_parser_show_channel_urls(output_and_prompt_options)

    output_and_prompt_options.add_argument(
        "--no-builds",
        default=False,
        action="store_true",
        required=False,
        help="Remove build specification from package list",
    )
    output_and_prompt_options.add_argument(
        "--no-channels",
        default=False,
        action="store_true",
        required=False,
        help="Remove channel specification from package list",
    )
    output_and_prompt_options.add_argument(
        "--explicit",
        default=False,
        action="store_true",
        required=False,
        help="Output an explicit list of conda packages. ",
    )
    output_and_prompt_options.add_argument(
        "--md5",
        default=False,
        action="store_true",
        required=False,
        help="Include the md5 in the explicit listing. ",
    )

    parser.add_argument(
        "--file",
        default=[],
        action="append",
        help="Read package versions from the given file. Repeated file "
        "specifications can be passed (e.g. --file=file1 --file=file2).",
    )
    parser.add_argument(
        "packages",
        metavar="package_spec",
        action="store",
        nargs="*",
        help="List of packages to install or update in the conda environment.",
    )
    return parser.parse_args(arguments)
