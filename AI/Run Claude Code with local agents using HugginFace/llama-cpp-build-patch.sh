#!/bin/bashsh

set -e

FILE="llama.cpp/.devops/cuda.Dockerfile"

if [ ! -f "$FILE" ]; then
  echo "File not found: $FILE"
  exit 1
fi

echo "Updating GCC references in $FILE..."

sed -i -E \
  -e 's/gcc-14/gcc-12/g' \
  -e 's/g\+\+-14/g++-12/g' \
  "$FILE"

echo "Done."
