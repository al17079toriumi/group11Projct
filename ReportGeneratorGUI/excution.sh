#!/usr/bin/env bash

cd `dirname $0`
script -q output.log ./a.out $@
rm a.out
rm cla.sh
ps aux | grep Terminal | grep -v grep | awk '{ print "kill -9", $2 }' | sh
