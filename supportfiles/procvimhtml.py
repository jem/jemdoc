#!/usr/bin/env python2.4

import os
import sys
import re

s = sys.argv[1]
#os.system('/Applications/Vim.app/Contents/MacOS/vim -n -f -u ../srccommands/vim.asciidoc +"run! syntax/2html.vim" +"wq" +"q" ' + s)
os.system('vim -n -f -u ../supportfiles/vim.asciidoc +"run! syntax/2html.vim" +"wq" +"q" ' + s)

h = open(s + '.html')

g = open(s + '.htmlfrag', 'w')
g.write('<pre>')

skip = True
l2 = None
for l2 in h:
    l2 = l2.strip()
    if skip:
        if l2 == '<pre>' or l2 == \
           '<body bgcolor="#ffffff" text="#000000"><font face="monospace">':
            skip = False

        continue

    if l2 == '</pre>' or l2 == '</font></body>':
        break

    l2 = l2.replace('<br>', '')

    # remove all <span> </span> tags.
    l2 = re.sub(r'</?span.*?>', '', l2)

    # hack to deal with single apostrophe representation of matrix transpose.
    # isn't going to work all the time!!
    if l2.count("'") % 2:
        l2 = re.sub("""'(</font>)+<font color="#808080">(.*)</font>""",
                    r"'\1\2", l2)

    if l2.startswith('&gt;&gt;&gt; '):
        g.write('<font color=navy>%s\n</font>' % l2)
    else:
        g.write(l2 + '\n')

g.seek(-1, 2) # back up over the last \n.
g.write('</pre>\n')

g.close()
h.close()

os.system('rm ' + s + '.html')

sys.exit(0)
