#!/bin/sh

set -e
# exit on first error

python3 -m venv venv
. venv/bin/activate

# debugging is a nightmare because of the pip cache
pip cache remove runtime_builder

export RUNTIME_BUILDER_ROOT=$(cat RUNTIME_BUILDER_ROOT.env)
sed "s|RUNTIME_BUILDER_ROOT|${RUNTIME_BUILDER_ROOT}|" <pyproject.toml.template >pyproject.toml

pip install --no-cache-dir .

cd /

run-test-enscons 250
echo ${?}
