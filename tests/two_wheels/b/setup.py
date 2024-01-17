from setuptools import setup
from runtime_builder import build_runtime_setuptools


setup(
    packages=["proj_b"],
    package_data={"proj_b": ["*.count", "*.source", "runtime_build"]},
    package_dir={"" : "src"},
    cmdclass={
        "build_runtime_builder_artifacts": build_runtime_setuptools("proj_b"),
    },
)
