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
    return re.sub(r"""[\\*/+"']""", r'\\\g<0>', s)

def replacelinks(b):
    r = re.compile(r'([ \(]|^)([^ \n]+?)(?<!\\)\[(.*?)(?<!\\)\]', re.M)
    m = r.search(b)
    while m:
        if '@' in m.group(2) and not m.group(2).startswith('mailto:'):
            link = 'mailto:' + m.group(2)
        else:
            link = m.group(2)

        link = quote(link)


        if m.group(3):
            linkname = m.group(3)
        else:
            linkname = re.sub('^mailto:', '', link)

        b = b[:m.start()] + m.group(1) + \
                '<a href=\\"%s\\">%s<\\/a>' % (link, linkname) + \
                b[m.end():]

        m = r.search(b, m.start())

    return b

def blockreplacements(b):
    """Does simple text replacements on a block of text."""
    # First do the URL thing.
    b = replacelinks(b)

    # First remove double backslashes.
    b = re.sub(r'\\\\', r'GONNABEBACKSLASH', b)

    # Deal with /italics/ first because the '/' in other tags would otherwise
    # interfere.
    r = re.compile(r'(?<!\\)/(.*?)(?<!\\)/', re.M)
    b = re.sub(r, r'<i>\1</i>', b)

    # Deal with *bold*.
    r = re.compile(r'(?<!\\)\*(.*?)(?<!\\)\*', re.M)
    b = re.sub(r, r'<b>\1</b>', b)

    # Deal with +monospace+.
    r = re.compile(r'(?<!\\)\+(.*?)(?<!\\)\+', re.M)
    b = re.sub(r, r'<tt>\1</tt>', b)

    # Deal with "double quotes".
    r = re.compile(r'(?<!\\)"(.*?)(?<!\\)"', re.M)
    b = re.sub(r, r'&#8220;\1&#8221;', b)

    # Deal with left quote `.
    r = re.compile(r"(?<!\\)`", re.M)
    b = re.sub(r, r'&#8216;', b)

    # Deal with apostrophe '.
    r = re.compile(r"(?<!\\)'", re.M)
    b = re.sub(r, r'&#8217;', b)

    # Deal with em dash ---.
    r = re.compile(r"(?<!\\)---", re.M)
    b = re.sub(r, r'&mdash;', b)

    # Deal with en dash --.
    r = re.compile(r"(?<!\\)--", re.M)
    b = re.sub(r, r'&ndash;', b)

    # Last remove any remaining backslashes, and replace GONNABEBACKSLASHes.
    b = re.sub(r'\\', '', b)
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

# Get the file started with the firstbit.
out(s['firstbit'])

# Look for a title.
if pc() == '=':
    t = blockreplacements(titletrim(nl()))
    hb(s['windowtitle'], t)
    hb(s['doctitle'], t)

# Look for a subtitle.
if pc() != '\n':
    hb(s['subtitle'], blockreplacements(np()))

# Now (just for the moment) do the rest of the in-text substitutions.
p = np()
while p:
    out('<p>' + blockreplacements(p) + '</p>')
    p = np()

out(s['endheader'])

out(s['lastbit'])
if outfile is not sys.stdout:
    outfile.close()
