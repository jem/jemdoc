import sys
import re

#inname = sys.argv[1]
#outname = sys.argv[2]
def parseconf(sname):
    syntax = {}
    f = open(sname)
    while getnextchar(f) != '':
        l = readnoncomment(f)
        r = re.match(r'\[(.*)\]\n', l)

        if r:
            tag = r.group(1)
            if tag in syntax:
                print 'Warning: ignoring redefinition of %s.' % tag
                continue

            s = ''
            l = readnoncomment(f)
            while l not in ('\n', ''):
                s += l
                l = readnoncomment(f)
            syntax[tag] = s

    f.close()

    return syntax

def readnoncomment(f):
    l = f.readline()
    if l == '':
        return l
    elif l[0] == '#':
        return readnoncomment(f)
    else:
        return l

def halfblock(tag, content):
    return re.sub(r'\|', content, tag)

inname = 'test.jemdoc'
outname = 'test.html'

infile = open(inname)
outfile = open(outname, 'w')

def out(s):
    outfile.write(s)

def titletrim(s):
    s = s.strip()
    return re.sub('=+ ', '', s)

def pc():
    """Peeks at next character in the file."""
    c = infile.read(1)
    if c: # only undo forward movement if we're not to the end.
        infile.seek(-1, 1)

    return c

def nl():
    """Get input file line which isn't a comment."""
    return readnoncomment(infile)

def np():
    """Gets the next paragraph from the input file."""
    # New paragraph markers signalled by characters in following tuple.
    s = ''
    while pc() not in ('\n', '-', '.', ''):
        s += nl()
        while pc() == '\n':
            nl() # burn blank line.

    return s

# load the grammar.
s = parseconf('jemdoc.conf')

# Get the file started with the firstbit.
out(s['firstbit'])

# Look for a title.
if pc() == '=':
    out(halfblock(s['title'], titletrim(l)))

# Look for a subtitle.
if pc() != '\n':
    l.

out(s['lastbit'])
outfile.close()
