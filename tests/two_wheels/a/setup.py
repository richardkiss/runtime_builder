from setuptools import setup
from runtime_builder import build_runtime_setuptools


setup(
    packages=["proj_a", "proj_a.next"],
    package_data={
        "proj_a": ["*.val", "*.count", "*.source", "runtime_build"],
        "proj_a.next": ["*.val", "*.source", "runtime_build"],
    },
    cmdclass={
        "build_runtime_builder_artifacts": build_runtime_setuptools(
            "proj_a", "proj_a.next"
        ),
    },
)
