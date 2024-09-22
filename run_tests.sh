#!/bin/bash

# Activate the virtual environment
source .quantium_venv/bin/activate

# Run the test suite with pytest
pytest

# Check the exit status of pytest
if [ $? -eq 0 ]; then
    echo "All tests passed."
    exit 0
else
    echo "Some tests failed."
    exit 1
fi


# chmod +x run_tests.sh
# ./run_tests.sh