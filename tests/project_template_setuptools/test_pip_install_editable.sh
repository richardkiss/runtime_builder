#!/bin/sh

set -e
# exit on first error


python3 -m venv venv
source venv/bin/activate
export RUNTIME_BUILDER_ROOT=$(cat RUNTIME_BUILDER_ROOT.env)
sed "s|RUNTIME_BUILDER_ROOT|${RUNTIME_BUILDER_ROOT}|" < pyproject.toml.template > pyproject.toml
pip install -e .
pip install ${RUNTIME_BUILDER_ROOT}
run-test 250
echo ${?}
echo 31 > proj/foo.source
run-test 1550
echo 20 > proj/foo.source
run-test 1000
echo 40 > proj/foo.source
run-test 2000
