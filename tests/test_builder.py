from pathlib import Path

import shutil
import subprocess
import tempfile

from runtime_builder.builder import build_all_items_for_package


def copy_template(dst: Path):
    my_path = Path(__file__).parent.resolve()
    project_template_path = my_path / "project_template"
    shutil.copytree(project_template_path, dst, dirs_exist_ok=True)


def run_shell_test(script_name: str):
    with tempfile.TemporaryDirectory() as dest:
        dest = Path(dest)
        copy_template(dest)
        with open(dest / "RUNTIME_BUILDER_ROOT.env", "w") as f:
            f.write(str(Path(__file__).parent.parent))
        command = str(dest / script_name)
        result = subprocess.run(command, shell=True, cwd=dest)
    assert result.returncode == 0


def test_simple():
    run_shell_test("test_pip_install.sh")
    run_shell_test("test_pip_install_editable.sh")
