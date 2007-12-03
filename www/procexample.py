#!/usr/bin/env python

f = open('exampleIN.jemdoc')
outf = open('example.jemdoc', 'w')

l = f.readline()
while not l.startswith('## jemdoc: start now.'):
    outf.write(l)
    l = f.readline()
outf.write(l)

outf.write('~~~\n{}{raw}\n<table class="dual-mode" cellpadding="0" cellspacing="0">\n')
outf.write('<tr><td class="leftcell">\n~~~\n')
s = ''
t = ''
l = f.readline()
while l != '':
    s += l
    if l.startswith('~'):
        t += '\\'
    t += l

    if not l.strip():
        # First write out real deal.
        outf.write(s)
        # Separate this from the source.
        outf.write('~~~\n{}{raw}\n</td><td class="sepcell">&nbsp;</td>\n')
        outf.write('<td class="rightcell">\n~~~\n~~~\n{}{jemdoc}\n')
        # Output the stuff again, but raw.
        if not t.splitlines()[-1].strip():
            t = t[:-1] + '\n'
        outf.write(t)
        # Separate this from the source.
        outf.write('~~~\n~~~\n{}{raw}\n</td></tr><tr>\n<td class="leftcell">\n~~~\n')
        s = ''
        t = ''

    l = f.readline()

# First write out real deal.
outf.write(s)
# Separate this from the source.
outf.write('~~~\n{}{raw}\n</td><td class="sepcell">&nbsp;</td>\n')
outf.write('<td class="rightcell">\n~~~\n~~~\n{}{jemdoc}\n')
# Output the stuff again, but raw.
#if not t.splitlines()[-1].strip():
#    t = t[:-1]
outf.write(t)
# Separate this from the source and end the table.
outf.write('~~~\n~~~\n{}{raw}\n</td></tr></table>\n~~~\n')

f.close()
outf.close()
