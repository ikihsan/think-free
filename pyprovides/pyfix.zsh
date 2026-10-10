# pyfix zsh function - Detect import errors and suggest PyPI distributions
# Usage: pyfix python3 -c "import sklearn"
# Add to ~/.zshrc or source this file directly

function pyfix() {
    setopt local_options pipe_fail
    python3 -m pyprovides.pyprovides_cli fix-import -- "$@"
}

# Optional: alias for convenience
alias fiximport='pyfix'