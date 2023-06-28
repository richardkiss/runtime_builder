# Runtime Builder

Sometimes python developers want to include compiled output or other binary blob artifacts in their wheels. The source materials for this output is checked into git, but the blobs are not (since they risk getting out of sync with the source distribution).

When building the wheel, the blobs need to be generated. But it may also be nice to rebuild the blobs if the source have changed at runtime to automate a step of the edit/test cycle.

This project lets you declare a single configuration describing how to build the artifacts, and build them at runtime during the development cycle or at wheel build time.


## Use

There is an example project in `tests/project_template`.

Note that it uses `enscons` to build, as the more commonly used `setuptools` does not easily allow fine-grained control of the contents of the `sdist` and `wheel` files. In particular, this example takes pains to include the source files `dynamic_build.py`, `foo.source`, `bar.source` and `program.source` in the sdist but not the wheel.

### Configuration

Artifacts to be build must be declared in a `dynamic_build.py` file. Each submodule can have zero or one of these build files.

This configuration file can be loaded at build time or at run time, so it *cannot* import anything that isn't made available in the `build-system.requires` section of `pyproject.toml`. In particular, it cannot import anything from the project being built since it has to be built before it can be installed in the build package, leading to a bootstrap problem.

```python

class MultiplyBuild:
    def __init__(self, factor):
        self.factor = factor

    def __call__(self, target_path):
        source_path = target_path.with_suffix(".source")
        t = int(open(source_path).read())
        with open(target_path, "w") as f:
            f.write(f"{t * self.factor}")


def count_build(target_path):
    source_path = target_path.with_suffix(".source")
    t = open(source_path).read()
    with open(target_path, "w") as f:
        f.write(f"{len(t)}\n")


BUILD_ARGUMENTS = {
    "foo.val": MultiplyBuild(50),
    "bar.count": count_build,
}
```

These examples could potentially build the artifacts every time they are referenced. If a build takes long enough, you may want to add code to only build when necessary to speed the edit/test cycle.


### Build-time

This is primarily a build-time dependency. If you want to take advantage of the run-time building, you need to install it in your runtime virtual environment. However, it generally should not be installed in the release version of your package.

Add it to your `pyproject.toml` file:

```toml
[build-system]
requires = ["runtime_builder", ...]

```

In the `SConstruct` file is the following line:

`built_items = build_all_items_for_package("proj")`

This returns the list of artifacts as a list of `Path` objects. These files must be included in the final wheel.


### Runtime

To use the dynamic build capabilities at runtime, use something like this boilerplate function:

```python

try:
    from runtime_builder.builder import build_on_demand
except ImportError:
    # `runtime_builder` is an optional dependency for development only
    def build_on_demand(*args): pass


def load_resource(
    resource_path: str,
    package: Package,
) -> bytes:
    build_on_demand(package, resource_path)
    with as_file(files(package).joinpath(resource_path)) as target_path:
        return target_path.read_bytes()
```

This checks for presence of `runtime_builder`, and invokes it if it's available just before accessing the resource.

## Examples

### chialisp_builder
- extends `runtime_builder` to add utilities to dynamically build chialisp clvm artifacts

### chialisp_library
- clib "header files" for use with chialisp

### chialisp_example
- an example that uses `chialisp_library` and shows how an optimal edit/test cycle, building just the minimum necessary


## License
- Runtime Builder is licensed under the MIT License. See the LICENSE file for more details.
