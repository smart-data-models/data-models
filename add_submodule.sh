#!/bin/sh

git submodule add --name $1 https://github.com/front-runner-smart-cities/dataModel.$1 specs/$1
