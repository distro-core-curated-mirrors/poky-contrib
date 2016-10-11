#!/bin/sh

# If we're using compressed generated tests we may need to
# decompress first. This is going to require at least 1.5 GB of space
if [[ /usr/lib/piglit/generated_tests.tar.gz -nt /usr/lib/piglit/generated_tests/ ]]; then
    echo "Decompressing generated tests..."
    tar -C /usr/lib/piglit/ -zxf /usr/lib/piglit/generated_tests.tar.gz || {
        echo "Failed to decompress tests, exiting."
        exit 1
    }
    touch /usr/lib/piglit/generated_tests
fi

if ! [[ -d /usr/lib/piglit/generated_tests ]]; then
    echo "NOTE: No generated tests found, install piglit-generated-tests-compressed"
    echo "      or piglit-generated-tests to include them in the tests."
fi

echo "Now running piglit..."
PIGLIT_NO_WINDOW=1 piglit.real "$@"
