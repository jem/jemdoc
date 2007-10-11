#!/usr/bin/env python

o = open('wholeguide.asciidoc', 'w')
a = ('using', 'matrices', 'parameters', 'variables', 'expressions',
     'classification', 'relations', 'problems', 'builtinatoms', 'customatoms')

o.write("= CVXMOD: User's guide\n")
o.write("Ignored Name\n")
o.write(":email: ignoredemail@lookat.makedocs.py\n\n")

for s in a:
    f = open(s + '.asciidoc')
    for l in f:
        if l.startswith('Ignored Name') or \
           l.startswith(':email: ignoredemail@lookat.makedocs.py'):
            continue

        if l.startswith('='):
            l = '=' + l
        o.write(l)

    o.write('\n')
    f.close()
o.close()
