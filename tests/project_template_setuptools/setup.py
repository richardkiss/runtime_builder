from setuptools import setup, find_packages
from runtime_builder import build_runtime_setuptools


setup(
    packages=["proj"],
    package_data={"proj": ["*.val", "*.count", "*.source", "runtime_build"]},
    cmdclass={
        "build_runtime_builder_artifacts": build_runtime_setuptools("proj"),
    },
)
