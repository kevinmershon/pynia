#!/bin/bash
curdir=`dirname $0`
coffee -b -o "$curdir/../static/js" \
  -c "$curdir/../src/coffee"

