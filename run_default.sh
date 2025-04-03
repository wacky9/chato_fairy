#!/bin/bash
#add no-cache option if necessary
docker compose build > log/dockerbuild.txt 2>&1
docker compose up > log/dockerout.txt 2>&1