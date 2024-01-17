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

run-test-setuptools 250

echo 31 >${BASE_DIR}/proj/foo.source
# shouldn't take effect without `RUNTIME_BUILDER_ROOT` present

run-test-setuptools 250

pip install --no-cache-dir ${RUNTIME_BUILDER_ROOT}

run-test-setuptools 1550
echo 32 >${BASE_DIR}/proj/foo.source
run-test-setuptools 1600
echo 20 >${BASE_DIR}/proj/foo.source
run-test-setuptools 1000
echo 40 >${BASE_DIR}/proj/foo.source
run-test-setuptools 2000
