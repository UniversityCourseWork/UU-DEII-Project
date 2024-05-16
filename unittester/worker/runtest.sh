#!/bin/bash

GIT_REPO=""
OUT_PATH="/testRepo"
[ ! -z "$1" ] && GIT_REPO="$1"
[ ! -z "$2" ] && OUT_PATH="$2"

# Print console message
printf "Processing: ${GIT_REPO}"

# Download the Repository
# from GitHub
git clone ${GIT_REPO} ${OUT_PATH} > /dev/null

# Change directory
current=$(pwd)
cd ${OUT_PATH}

# Run maven tests
#mvn test > /dev/null 2>temp-console-output-file.txt
mvn test > temp-console-output-file.txt

# Change directory back
cd ${current}
