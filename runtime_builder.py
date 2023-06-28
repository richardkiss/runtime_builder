from importlib.resources import as_file, files, Package
from pathlib import Path
from os import PathLike
from typing import List


DEFAULT_FN = "runtime_build"


def load_python_config(
    config_file_path: Path, local_variable_name: str
) -> dict:
    config_file_contents = config_file_path.read_text()
    context = {}
    exec(config_file_contents, context)
    return context.get(local_variable_name, {})


def load_build_args_for_package(
    package: Package, build_file_name: PathLike, src_root: PathLike
) -> dict:
    build_path = Path(src_root).resolve()
    for package_part in package.split("."):
        build_path /= package_part
    build_path /= build_file_name
    return load_python_config(build_path, "BUILD_ARGUMENTS")


def build_item(package, base_name, builder):
    with as_file(files(package).joinpath(base_name)) as target_path:
        builder(target_path)
        return target_path


def build_on_demand(
    package: Package,
    base_name: PathLike,
    build_file_name: PathLike = DEFAULT_FN,
    src_root: PathLike = ".",
):
    build_args = load_build_args_for_package(package, build_file_name, src_root)
    builder = build_args.get(base_name)
    return build_item(package, base_name, builder)


def build_all_at_build_time(
    packages: List[Package],
    build_file_name: PathLike = DEFAULT_FN,
    src_root: PathLike = ".",
):
    # call this from `scons` or whatever to create all the `.hex` files
    for package in packages:
        build_all_items_for_package(package, build_file_name, src_root)


def build_all_items_for_package(
    package: Package, build_file_name: PathLike = DEFAULT_FN, src_root: PathLike = "."
):
    build_args = load_build_args_for_package(package, build_file_name, src_root or ".")
    return [
        build_item(package, base_name, builder)
        for base_name, builder in build_args.items()
    ]
