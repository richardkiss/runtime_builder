from pathlib import Path
from typing import List


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


def calculate_dependencies(source_path: Path, args: dict) -> List[Path]:
    return []


class ChialispBuild:
    def __init__(self, include_paths: List[str] = []):
        self.include_paths = include_paths

    def __call__(self, target_path: Path):
        import clvm_tools_rs

        source_path = target_path.with_suffix(".source")

        dependencies = calculate_dependencies(source_path, self.include_paths)
        latest_date = max(_.stat().st_mtime for _ in [source_path] + dependencies)

        if not target_path.exists() or target_path.stat().st_mtime < latest_date:
            # we need to rebuild
            print(f"rebuilding {source_path}")
            source_path_str, target_path_str = str(source_path), str(target_path)
            clvm_tools_rs.compile_clvm(
                source_path_str, target_path_str, self.include_paths
            )


BUILD_ARGUMENTS = {
    "foo.val": MultiplyBuild(50),
    "bar.count": count_build,
    "program.hex": ChialispBuild(),
}
