#!/bin/sh

set -e
# exit on first error

python3 -m venv venv
. venv/bin/activate

# debugging is a nightmare because of the pip cache
pip cache remove runtime_builder

export RUNTIME_BUILDER_ROOT=$(cat RUNTIME_BUILDER_ROOT.env)
sed "s|RUNTIME_BUILDER_ROOT|${RUNTIME_BUILDER_ROOT}|" <pyproject.toml.template >pyproject.toml

pip install --no-cache-dir -e .

BASE_DIR=$(pwd)
#cd /

run-test-enscons 250

echo 30 >${BASE_DIR}/proj/foo.source
# shouldn't take effect without `RUNTIME_BUILDER_ROOT` present

run-test-enscons 250

pip install --no-cache-dir ${RUNTIME_BUILDER_ROOT}

run-test-enscons 1500
echo 33 >${BASE_DIR}/proj/foo.source
run-test-enscons 1650
echo 21 >${BASE_DIR}/proj/foo.source
run-test-enscons 1050
echo 41 >${BASE_DIR}/proj/foo.source
run-test-enscons 2050

