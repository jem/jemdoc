import sys
import re

#inname = sys.argv[1]
#outname = sys.argv[2]
def parseconf(sname):
    syntax = {}
    f = open(sname)
    while pc(f) != '':
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

inname = 'test.jemdoc'
outname = 'test.html'

infile = open(inname)
outfile = sys.stdout # open(outname, 'w')

def out(s):
    outfile.write(s)

def hb(tag, content):
    """Writes out a halfblock (hb)."""
    out(re.sub(r'\|', content, tag))

def titletrim(s):
    s = s.strip()
    return re.sub('=+ ', '', s)

def pc(f = infile):
    """Peeks at next character in the file."""
    # Should only be used to look at the first character of a new line.
    c = f.read(1)
    if c: # only undo forward movement if we're not to the end.
        if c == '#':
            f.readline() # burn comment line.
            return pc(f)

        f.seek(-1, 1)

    return c

def nl():
    """Get input file line which isn't a comment."""
    return readnoncomment(infile)

def quote(s):
    return re.sub(r'[\\*/+]', r'\\\g<0>', s)

def blockreplacements(b):
    """Does simple text replacements on a block of text."""
    # First remove double backslashes.
    b = re.sub(r'\\\\', r'GONNABEBACKSLASH', b)

    # Deal with /italics/ first because the '/' in other tags would otherwise
    # interfere.
    b = re.sub(r'(?M)(?<!\\)/(.*?)(?<!\\)/', r'<i>\1</i>', b)

    # Deal with *bold*.
    b = re.sub(r'(?M)(?<!\\)\*(.*?)(?<!\\)\*', r'<b>\1</b>', b)

    # Deal with +monospace+.
    b = re.sub(r'(?M)(?<!\\)\+(.*?)(?<!\\)\+', r'<tt>\1</tt>', b)

    # Last remove any remaining backslashes, and replace GONNABEBACKSLASHes.
    b = re.sub('GONNABEBACKSLASH', '\\\\', b)

    return b

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

## Get the file started with the firstbit.
#out(s['firstbit'])
#
## Look for a title.
#if pc() == '=':
#    t = titletrim(nl())
#    hb(s['windowtitle'], t)
#    hb(s['doctitle'], t)
#
## Look for a subtitle.
#if pc() != '\n':
#    hb(s['subtitle'], np())
#
#out(s['endheader'])
#
#out(s['lastbit'])
#if outfile is not sys.stdout:
#    outfile.close()
