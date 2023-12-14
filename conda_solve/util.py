from argparse import Namespace
from typing import List

from conda.base.context import context
from conda.cli import common
from conda.models.match_spec import MatchSpec
from conda.base.constants import REPODATA_FN


def get_specs(args: Namespace) -> List[MatchSpec]:
    args_packages = [s.strip("\"'") for s in args.packages]
    specs = []
    if args.file:
        for fpath in args.file:
            try:
                specs.extend(common.specs_from_url(fpath, json=context.json))
            except UnicodeError:
                raise CondaError(
                    "Error reading file, file should be a text file containing"
                    " packages \nconda create --help for details"
                )
        if "@EXPLICIT" in specs:
            explicit(specs, prefix, verbose=not context.quiet, index_args=index_args)
            return
    specs.extend(common.specs_from_args(args_packages, json=context.json))
    return specs


def get_repodata_fns(args) -> List[str]:
    repodata_fns = args.repodata_fns
    if not repodata_fns:
        repodata_fns = context.repodata_fns
    if REPODATA_FN not in repodata_fns:
        repodata_fns.append(REPODATA_FN)
    return repodata_fns
