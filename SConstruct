# Starter SConstruct for enscons

import enscons
import pytoml


metadata = dict(pytoml.load(open("pyproject.toml")))["project"]

full_tag = "py3-none-any"  # pure Python packages compatible with 2+3

env = Environment(
    tools=["default", "packaging", enscons.generate],
    PACKAGE_METADATA=metadata,
    WHEEL_TAG=full_tag,
    ROOT_IS_PURELIB=full_tag.endswith("-any"),
)

py_source = Glob("runtime_builder/*.py")

source = env.Whl("purelib", py_source, root="")
wheel = env.WhlFile(source=source)

sdist_source = (
    File(["PKG-INFO", "README.md", "SConstruct", "pyproject.toml"]) + py_source
)
sdist = env.SDist(source=sdist_source)
env.NoClean(sdist)
env.Alias("sdist", sdist)

# needed for pep517 (enscons.api) to work
env.Default(wheel, sdist)
