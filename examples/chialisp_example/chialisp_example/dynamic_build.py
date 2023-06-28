from chialisp_includes import include_directory
from chialisp_builder import ChialispBuild


BUILD_ARGUMENTS = {
    "sha256tree.hex": ChialispBuild([str(include_directory())]),
}
