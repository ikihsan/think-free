# pyfix fish function - Detect import errors and suggest PyPI distributions
# Usage: pyfix python3 -c "import sklearn"

function pyfix --description "Run a command and suggest fixes for import errors"
    set -euo pipefail

    pyprovides fix-import -- "$argv"
end