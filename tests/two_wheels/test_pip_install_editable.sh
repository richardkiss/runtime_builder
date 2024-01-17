#!/bin/sh

set -e
# exit on first error

python3 -m venv venv
. venv/bin/activate

# debugging is a nightmare because of the pip cache
echo runtime_builder proj_a proj_b | xargs -n1 pip cache remove

export RUNTIME_BUILDER_ROOT=$(cat RUNTIME_BUILDER_ROOT.env)
export TEMP_DIRECTORY_ROOT=$(pwd)

sed -e "s|TEMP_DIRECTORY_ROOT|$(pwd)|" -e "s|RUNTIME_BUILDER_ROOT|${RUNTIME_BUILDER_ROOT}|" < a/pyproject.toml.template > a/pyproject.toml
sed "s|RUNTIME_BUILDER_ROOT|${RUNTIME_BUILDER_ROOT}|" < b/pyproject.toml.template > b/pyproject.toml

pip install -vv -e ./a
run-a 450

A_BASE=a/proj_a/
B_BASE=$(dirname $(python3 -c 'import proj_b; print(proj_b.__file__)'))


run-a 450
echo 31 >${A_BASE}/foo.source
run-a 450
echo 20 >${A_BASE}/foo.source
run-a 450
echo 40 >${A_BASE}/foo.source
run-a 450

pip install ${RUNTIME_BUILDER_ROOT}

run-a 2000
echo 31 >${A_BASE}/foo.source
run-a 1550
echo 20 >${A_BASE}/foo.source
run-a 1000

# a missing `runtime_build` or source file should give a warning
#
mv ${B_BASE}/bar_b.source  ${B_BASE}/bar_b.source.missing
run-a 1000

mv ${B_BASE}/bar_b.source.missing  ${B_BASE}/bar_b.source
run-a 1000

mv ${B_BASE}/runtime_build ${B_BASE}/runtime_build.missing
run-a 1000

mv ${B_BASE}/bar_b.source  ${B_BASE}/bar_b.source.missing
run-a 1000
