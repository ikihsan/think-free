# pyfix fish function - Detect import errors and suggest PyPI distributions
# Usage: pyfix python3 -c "import sklearn"

function pyfix --description "Run a command and suggest fixes for import errors"
    set -euo pipefail

    # Set PYTHONPATH to include the think-free repository
    set -gx PYTHONPATH ${PYTHONPATH:-}${PYTHONPATH:+:}/home/ubuntu/think-free

    python3 -m pyprovides.pyprovides_cli fix-import -- "$argv"
end