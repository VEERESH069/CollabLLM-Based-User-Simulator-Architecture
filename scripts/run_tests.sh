#!/usr/bin/env bash
set -euo pipefail
python3 -m pytest -q --maxfail=1 --disable-warnings
