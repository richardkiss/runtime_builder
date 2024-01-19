from importlib.resources import as_file, files, Package

import sys

import proj_b

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
    bar = proj_b.load_resource("bar_b.count", "proj_b")
    assert bar == b"hello from b\n has 13 characters\n"

    foo = load_resource("foo.val", __package__)
    baz = load_resource("baz_a.val", "proj_a.next")

    print(
        f"TEST: running main proj_a: foo={foo.decode()} vs {sys.argv[1]};"
        f" baz={baz.decode()} vs {sys.argv[2]}"
    )

    assert foo.decode() == sys.argv[1]
    assert baz.decode() == sys.argv[2]


if __name__ == "__main__":
    main()
