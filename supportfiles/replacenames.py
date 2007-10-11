#!/usr/bin/env python

import os
import sys

f = open(sys.argv[1])
g = open(sys.argv[2], 'w')
for l in f:
    if l.find('span id="author"') != -1:
        g.write(r'<span id="author"><a href="http://stanford.edu/~jacobm/">Jacob Mattingley</a> and <a href="http://stanford.edu/~boyd/">Stephen Boyd</a></span>&nbsp;')
    elif l.find('span id="email"') != -1:
        g.write(r'<span id="email">(<tt><a href="mailto:jacobm@stanford.edu">jacobm@stanford.edu</a></tt> and <tt><a href="mailto:boyd@stanford.edu">boyd@stanford.edu</a></tt>)</span><br />')
    else:
        g.write(l)

sys.exit(0)

# vim:tw=0
