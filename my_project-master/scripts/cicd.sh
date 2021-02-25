#!/bin/sh

echo "call cicd.sh"

python deploy.py bk-template -e test -u admin -p blueking -d http://paas.szbke.com