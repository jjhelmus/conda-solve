import sys
import json
import os


from conda.base.context import context

# type annotations
from typing import List

from conda.models.match_spec import MatchSpec
from conda.models.records import PackageRecord
from conda.base.context import Context
from collections.abc import MutableSet

from .cli import parse_arguments
from .util import get_specs, get_repodata_fns



def local_solve(
        specs: List[MatchSpec],
        repodata_fns: List[str],
        context: Context,
    ) -> "MutableSet[PackageRecord]":
    prefix = "/fake/fake/fake"
    command = "create"

    channels = context.channels
    subdirs = context.subdirs
    update_modifier = context.update_modifier
    deps_modifier = context.deps_modifier

    for repodata_fn in repodata_fns:
        solver_backend = context.plugin_manager.get_cached_solver_backend()
        solver = solver_backend(
            prefix,
            channels,
            subdirs,
            specs_to_add=specs,
            repodata_fn=repodata_fn,
            command=command,
        )
        unlink_link_transaction = solver.solve_for_transaction(
            deps_modifier=deps_modifier,
            update_modifier=update_modifier,
            force_reinstall=False,
            should_retry_solve=(repodata_fn != repodata_fns[-1]),
        )
        break
        # TODO exceptions to all retry with new repodata
    return unlink_link_transaction.prefix_setups[prefix].link_precs



def solve_subcommand(arguments: List[str]):
    args = parse_arguments(arguments)
    if args.explicit:
        args.json = True
    context.__init__(argparse_args=args)

    specs = get_specs(args)
    repodata_fns = get_repodata_fns(args)
    if args.subdir:
        if args.subdir.startswith("linux-"):
            os.environ["CONDA_OVERRIDE_GLIBC"] = "2.17"
    precs = local_solve(specs, repodata_fns, context)

    if args.explicit:
        print("# This file may be used to create an environment using:")
        print("# $ conda create --name <env> --file <this file>")
        print(f"# platform: {context.subdir}")
        print("@EXPLICIT")
        for prec in precs:
            if args.md5:
                print(f"{prec.url}#{prec.md5}")
            else:
                print(f"{prec.url}")
        return

    if args.json:
        pkgs_dumps = [prec.dump() for prec in precs]
        print(json.dumps(pkgs_dumps, indent=2))
        return

    for prec in precs:
        if args.no_channels:
            if args.no_builds:
                print(f"{prec.name}=={prec.version}")
            else:
                print(f"{prec.name}=={prec.version}={prec.build}")
        else:
            if args.no_builds:
                print(f"{prec.channel.canonical_name}::{prec.name}=={prec.version}")
            else:
                print(f"{prec.channel.canonical_name}/{prec.subdir}::{prec.name}=={prec.version}={prec.build}")


if __name__ == "__main__":
    solve_subcommand(sys.argv[1:])
