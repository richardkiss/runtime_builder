#!/bin/sh

set -e
# exit on first error


python3 -m venv venv
. venv/bin/activate

# debugging is a nightmare because of the pip cache
echo runtime_builder proj_a proj_b | xargs -n1 pip cache remove

export RUNTIME_BUILDER_ROOT=$(cat RUNTIME_BUILDER_ROOT.env)

sed -e "s|TEMP_DIRECTORY_ROOT|$(pwd)|" -e "s|RUNTIME_BUILDER_ROOT|${RUNTIME_BUILDER_ROOT}|" < a/pyproject.toml.template > a/pyproject.toml
sed "s|RUNTIME_BUILDER_ROOT|${RUNTIME_BUILDER_ROOT}|" < b/pyproject.toml.template > b/pyproject.toml

pip install -vv ./a
run-a 450
pip install ${RUNTIME_BUILDER_ROOT}
run-a 450
echo ${?}

