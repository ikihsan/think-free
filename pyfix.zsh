# pyfix zsh function - Detect import errors and suggest PyPI distributions
# Usage: pyfix python3 -c "import sklearn"

pyfix() {
    set -euo pipefail

    pyprovides fix-import -- "$@"
}