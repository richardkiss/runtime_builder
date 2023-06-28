from importlib import import_module
from importlib.resources import as_file, files, Package
from typing import Iterator, List

import contextlib
import pathlib
import sys


DEFAULT_FN = "dynamic_build"


@contextlib.contextmanager
def add_sys_path(path: None | str) -> Iterator[None]:
    """Temporarily add the given path to `sys.path`."""
    try:
        if path:
            path = pathlib.Path(path).resolve()
            sys.path.insert(0, path)
        yield
    finally:
        if path:
            sys.path.remove(path)


def load_build_args_for_package(package: Package, build_file_name, src_root) -> dict:
    # pass in `src_root` if its during build time and the source package tree is
    # not at `.` (relative to the build files)
    with add_sys_path(src_root):
        mod = import_module(f"{package}.{build_file_name}")
        return mod.BUILD_ARGUMENTS


def build_item(package, base_name, builder):
    with as_file(files(package).joinpath(base_name)) as target_path:
        builder(target_path)
        return target_path


def build_on_demand(
    package: Package, base_name: str, build_file_name: str = DEFAULT_FN
):
    build_args = load_build_args_for_package(package, build_file_name, None)
    builder = build_args.get(base_name)
    return build_item(package, base_name, builder)


def build_all_at_build_time(
    packages: List[Package],
    build_file_name: str = DEFAULT_FN,
    src_root=None,
):
    # call this from `scons` or whatever to create all the `.hex` files
    for package in packages:
        build_all_items_for_package(package, build_file_name, src_root)


def build_all_items_for_package(
    package: Package, build_file_name: str = DEFAULT_FN, src_root=None
):
    build_args = load_build_args_for_package(package, build_file_name, src_root)
    return [
        build_item(package, base_name, builder)
        for base_name, builder in build_args.items()
    ]
