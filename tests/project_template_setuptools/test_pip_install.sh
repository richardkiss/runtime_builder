#!/bin/sh

set -e
# exit on first error


python3 -m venv venv
source venv/bin/activate
export RUNTIME_BUILDER_ROOT=$(cat RUNTIME_BUILDER_ROOT.env)
sed "s|RUNTIME_BUILDER_ROOT|${RUNTIME_BUILDER_ROOT}|" < pyproject.toml.template > pyproject.toml
pip install .
run-test 250
echo ${?}

