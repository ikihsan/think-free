# pyfix fish function - Detect import errors and suggest PyPI distributions
# Usage: pyfix python3 -c "import sklearn"

function pyfix
    # Call pyprovides fix-import with the original arguments
    pyprovides fix-import -- $argv
end