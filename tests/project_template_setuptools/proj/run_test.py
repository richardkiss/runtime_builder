from importlib.resources import as_file, files, Package

import sys

try:
    from runtime_builder import build_on_demand
except ImportError:
    # `runtime_builder` is an optional dependency for development only
    def build_on_demand(*args):
        pass


def load_resource(
    resource_path: str,
    package: Package,
) -> bytes:
    build_on_demand(package, resource_path)
    with as_file(files(package).joinpath(resource_path)) as target_path:
        return target_path.read_bytes()


def main():
    print("WE ARE RUNNING TESTS")
    val = load_resource("foo.val", __package__)
    assert val.decode() == sys.argv[1]
    bar = load_resource("bar.count", __package__)
    assert bar == b"6\n"


if __name__ == "__main__":
    main()
