#!/bin/sh

git submodule update --init --remote
git add .
git commit -m "Child repository update"

