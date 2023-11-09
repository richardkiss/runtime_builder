from importlib.resources import Package
from pathlib import Path
from os import PathLike
from setuptools import Command
from setuptools.command.build import build
from typing import Any, Callable, Dict, List, Union

try:
    PathType = str | PathLike[Any]
except TypeError:
    # `PathLike[Any]` not supported until 3.9
    # `str | None` syntax not supported until 3.10
    PathType = Union[str, PathLike]


DEFAULT_FN = "runtime_build"


def load_python_config(config_file_path: Path, local_variable_name: str) -> Dict:
    config_file_contents = config_file_path.read_text()
    context: Dict[str, Any] = dict(__file__=str(config_file_path.resolve()))
    exec(config_file_contents, context)
    return context.get(local_variable_name, {})


def base_for_package(package: Package, src_root: PathType) -> Path:
    base_path = Path(src_root).resolve()
    for package_part in package.split("."):
        base_path /= package_part
    return base_path


def load_build_args_for_package(
    package: Package, build_file_name: PathType, src_root: PathType
) -> Dict[PathType, Callable[[Path], Path]]:
    build_path = base_for_package(package, src_root) / build_file_name
    return load_python_config(build_path, "BUILD_ARGUMENTS")


def build_item(
    package: Package,
    base_name: PathType,
    builder: Callable[[Path], Path],
    src_root: PathType,
) -> Path:
    target_path = base_for_package(package, src_root) / base_name
    builder(target_path)
    return target_path


def build_on_demand(
    package: Package,
    base_name: PathType,
    build_file_name: PathType = DEFAULT_FN,
    src_root: PathType = ".",
):
    build_args = load_build_args_for_package(package, build_file_name, src_root)
    builder = build_args.get(base_name)
    if builder is None:
        raise ValueError(f"unknown resource {base_name}")
    return build_item(package, base_name, builder, src_root)


def build_all_at_build_time(
    packages: List[Package],
    build_file_name: PathType = DEFAULT_FN,
    src_root: PathType = ".",
) -> List[Path]:
    built = []
    for package in packages:
        built.extend(build_all_items_for_package(package, build_file_name, src_root))
    return built


def build_all_items_for_package(
    package: Package, build_file_name: PathType = DEFAULT_FN, src_root: PathType = "."
) -> List[Path]:
    build_args = load_build_args_for_package(package, build_file_name, src_root)
    return [
        build_item(package, base_name, builder, src_root)
        for base_name, builder in build_args.items()
    ]


def build_runtime_setuptools(*all_packages: List[Package]) -> Command:
    """
    Use this in `setup.py` as follows:

    ```python
    from runtime_builder import build_runtime_setuptools

    RUNTIME_BUILD_PACKAGE_LIST = ["package.foo", "package.bar", ...]
    # list of packages containing `runtime_build` files (so there is one
    # at `package/foo/runtime_build` and one at `package/bar/runtime_build`)

    setup(
        ...
        include_package_data=True,
        cmdclass={
            "build_runtime_builder_artifacts": build_runtime_setuptools(RUNTIME_BUILD_PACKAGE_LIST),
        },
    )
    ```
    This example invokes `build_all_items_for_package` at just the right time.

    Using `setuptools` to do this build isn't as satisfying as `enscons`, as I've not been able
    to figure out a way to only include source files in the sdist. This is a consequence of
    `setuptools` being a really terrible legacy mess.
    """
    build.sub_commands.insert(0, ("build_runtime_builder_artifacts", lambda x: 1))

    class BuildRuntimeBuilderArtifactsCommand(Command):
        description = "Build runtime_builder artifacts files"
        user_options = []

        def initialize_options(self):
            pass

        def finalize_options(self):
            pass

        def run(self):
            # Custom code to generate the .hex files
            for package in all_packages:
                _built_items = build_all_items_for_package(package)

    return BuildRuntimeBuilderArtifactsCommand
