#!/usr/bin/env python2.4

import sys
import subprocess


c = 'tidy -q -c -o ' + sys.argv[2] + ' ' + sys.argv[1]
a = subprocess.call(c, shell=True)

if a <= 1:
    # handle warnings only, too.
    sys.exit(0)
else:
    sys.exit(1)
