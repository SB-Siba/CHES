#!/bin/bash

cd "$jenkins_dir$pipeline_name/"

# copy the envs from .env.template > create new .env > paste the content
cp .env.template .env

sudo rm -rf .env.template