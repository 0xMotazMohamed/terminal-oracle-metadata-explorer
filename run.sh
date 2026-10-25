#!/usr/bin/env bash
cd "$(dirname "$(readlink -f "$0")")" || exit 1

# Pick whichever interpreter exists inside the venv
if [ -x ".venv/bin/python" ]; then
    PY=".venv/bin/python"
else
    echo "No Python found in .venv/bin. Recreate it with: python3 -m venv .venv"
    exit 1
fi

# Install the requirements only if a package is missing
if ! "$PY" -c "import oracledb" 2>/dev/null; then
    echo "Installing requirements..."
    "$PY" -m pip install -r requirements.txt || exit 1
fi

exec "$PY" main.py