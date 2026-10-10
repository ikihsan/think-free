# pyfix zsh function - Detect import errors and suggest PyPI distributions
# Usage: pyfix python3 -c "import sklearn"

pyfix() {
    set -euo pipefail

    # Set PYTHONPATH to include the think-free repository
    if [[ -z "$PYTHONPATH" ]]; then
        export PYTHONPATH="/home/ubuntu/think-free"
    else
        export PYTHONPATH="${PYTHONPATH}:/home/ubuntu/think-free"
    fi

    python3 -m pyprovides.pyprovides_cli fix-import -- "$@"
}