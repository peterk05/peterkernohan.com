#!/usr/bin/env bash
# Copy the public site into the output folder (default _site), leaving out repo tooling,
# so GitHub Pages never serves tests, specs, evals, lessons or agent config.
set -euo pipefail
cd "$(dirname "$0")/.."
out="${1:-_site}"
rm -rf "$out"
mkdir -p "$out"
rsync -a --exclude='.git/' --exclude='/_site/' \
  --exclude='/tests/' --exclude='/specs/' --exclude='/evals/' --exclude='/lessons/' \
  --exclude='/metrics/' --exclude='/scripts/' --exclude='/.claude/' --exclude='/.github/' \
  --exclude='/.githooks/' --exclude='/.gitignore' --exclude='__pycache__/' --exclude='.pytest_cache/' \
  --exclude='.superpowers/' ./ "$out/"
