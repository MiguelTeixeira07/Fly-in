#!/bin/bash

for file in $(find ./maps/invalid/ -type f -name '*.txt' | sort); do
    if [ "$file" = "./maps/invalid/README.txt" ]; then
        continue
    fi
    echo "Testing $file..."

    python3 fly_in.py "$file"

    if [ $? -ne 0 ]; then
        echo
        echo "ERROR: parser failed on $file"
        exit 1
    fi
done

echo
echo "All tests passed!"