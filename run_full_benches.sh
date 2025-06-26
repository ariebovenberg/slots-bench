#!/bin/bash
set -eu

PYTHON_VERSIONS=(
    "3.13.3"
    "3.12.11"
    "3.11.13"
    "3.10.18"
    "3.9.23"
)
PYPERF_VERSION="2.9.0"

export PIP_DISABLE_PIP_VERSION_CHECK=1
unset VIRTUAL_ENV

echo "Running benchmarks for optimized Python versions..."
for version in "${PYTHON_VERSIONS[@]}"; do
    echo "Running benchmarks for optimized Python version: $version"
    uv add pyperf=="$PYPERF_VERSION"
    BENCH_SLOTS=1 uv run -q -p "$version" --managed-python bench_slots.py --copy-env --quiet --append getattr-slots-opt.json
    BENCH_SLOTS=0 uv run -q -p "$version" --managed-python bench_slots.py --copy-env --quiet --append getattr-dict-opt.json
done

echo "Running benchmarks for unoptimized Python versions..."
for version in "${PYTHON_VERSIONS[@]}"; do
    echo "Running benchmarks for unoptimized Python version: $version"
    $PYENV_ROOT/versions/$version/bin/python -m venv venv-"$version"
    venv-$version/bin/pip install -q pyperf=="$PYPERF_VERSION"
    BENCH_SLOTS=1 venv-$version/bin/python bench_slots.py --python venv-"$version"/bin/python --copy-env --quiet --append getattr-slots-nonopt.json
    BENCH_SLOTS=0 venv-$version/bin/python bench_slots.py --python venv-"$version"/bin/python --copy-env --quiet --append getattr-dict-nonopt.json
done

python -m pyperf compare_to --table getattr-dict-opt.json getattr-slots-opt.json
python -m pyperf compare_to --table getattr-dict-nonopt.json getattr-slots-nonopt.json
