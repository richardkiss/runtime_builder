from importlib.resources import as_file, files, Package
from pathlib import Path
from typing import List

import clvm_tools_rs


def calculate_dependencies(source_path: Path, args: dict) -> List[Path]:
    return []


class ChialispBuild:
    def __init__(self, include_paths: List[str] = []):
        self.include_paths = include_paths

    def __call__(self, target_path: Path):

        source_path = target_path.with_suffix(".clsp")

        dependencies = calculate_dependencies(source_path, self.include_paths)
        latest_date = max(_.stat().st_mtime for _ in [source_path] + dependencies)

        if not target_path.exists() or target_path.stat().st_mtime < latest_date:
            # we need to rebuild
            print(f"rebuilding {source_path}")
            source_path_str, target_path_str = str(source_path), str(target_path)
            clvm_tools_rs.compile_clvm(
                source_path_str, target_path_str, self.include_paths
            )
