import sys
import re

#inname = sys.argv[1]
#outname = sys.argv[2]
def readnoncomment(f):
    l = f.readline()
    if l == '':
        return l
    elif l[0] == '#':
        return readnoncomment(f)
    else:
        return l.strip() + '\n' # leave just one \n.

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

inname = 'test.jemdoc'
outname = 'test.html'

infile = open(inname)
outfile = sys.stdout # open(outname, 'w')

def out(s):
    outfile.write(s)

def hb(tag, content):
    """Writes out a halfblock (hb)."""
    out(re.sub(r'\|', content, tag))


def pc(f = infile):
    """Peeks at next character in the file."""
    # Should only be used to look at the first character of a new line.
    c = f.read(1)
    if c: # only undo forward movement if we're not to the end.
        #if c == '#': # interpret comment lines as blank.
        #    return '\n'

        f.seek(-1, 1)

    return c

def nl(withcount=False):
    global linenum
    """Get input file line."""
    s = infile.readline()
    linenum += 1
    # remove any special characters - assume they were checked by pc() before
    # we got here.
    toreturn = s.lstrip(' \t-.=')

    # remove any trailing comments.
    toreturn = re.sub(r'\s*(?<!\\)#.*', '', toreturn)

    if withcount:
        if s[0] == '.':
            m = r'\.'
        else:
            m = s[0]

        r = re.match('(%s+) ' % m, s)
        if not r:
            raise SyntaxError('error on line %d' % linenum)

        return (toreturn, len(r.group(1)))
    else:
        return toreturn



def np(withcount=False):
    """Gets the next paragraph from the input file."""
    # New paragraph markers signalled by characters in following tuple.
    if withcount:
        (s, c) = nl(withcount)
    else:
        s = nl()

    while pc() not in ('\n', '-', '.', '', '=', '#', '~', '{'):
        s += nl()

    while pc() == '\n':
        nl() # burn blank line.

    # in both cases, ditch the trailing \n.
    if withcount:
        return (s[:-1], c)
    else:
        return s[:-1]


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
                r'<a href=\"%s\">%s<\/a>' % (link, linkname) + b[m.end():]

        m = r.search(b, m.start())

    return b

def br(b):
    """Does simple text replacements on a block of text. ('block replacements')"""
    b = allreplace(b)

    # First do the URL thing.
    b = b.lstrip('-. \t') # remove leading spaces, tabs, dashes, dots.
    b = replacelinks(b)

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
    b = re.sub(r, r'&ldquo;\1&rdquo;', b)

    # Deal with left quote `.
    r = re.compile(r"(?<!\\)`", re.M)
    b = re.sub(r, r'&lsquo;', b)

    # Deal with apostrophe '.
    r = re.compile(r"(?<!\\)'", re.M)
    b = re.sub(r, r'&rsquo;', b)

    # Deal with em dash ---.
    r = re.compile(r"(?<!\\)---", re.M)
    b = re.sub(r, r'&mdash;', b)

    # Deal with en dash --.
    r = re.compile(r"(?<!\\)--", re.M)
    b = re.sub(r, r'&ndash;', b)

    # Last remove any remaining quoting backslashes.
    b = re.sub(r'\\([^\\])', r'\1', b)

    return b

def allreplace(b):
    """Replacements that should be done on everything."""
    # Deal with left quote `.
    r = re.compile(r">", re.M)
    b = re.sub(r, r'&gt;', b)

    r = re.compile(r"<", re.M)
    b = re.sub(r, r'&lt;', b)

    return b

# load the grammar.
grammar = parseconf('jemdoc.conf')

# Get the file started with the firstbit.
out(grammar['firstbit'])

linenum = 1
# Look for a title.
if pc() == '=': # don't check exact number of '=' here jem.
    t = br(nl())[:-1]
    hb(grammar['windowtitle'], t)
    out(grammar['bodystart'])
    hb(grammar['doctitle'], t)

    # Look for a subtitle.
    if pc() != '\n':
        hb(grammar['subtitle'], br(np()))
else:
    out(grammar['bodystart'])

# Now (just for the moment) do the rest of the in-text substitutions.
inblock = False
while 1: # wait for EOF.
    p = pc()

    if p == '':
        break

    # look for lists.
    elif p == '-':
        out('<ul>\n')
        while pc() == '-':
            hb('<li>|</li>\n', br(np()))

        out('</ul>\n')

    elif p == '.':
        out('<ol>\n')
        while pc() == '.':
            hb('<li>|</li>\n', br(np()))

        out('</ol>\n')

    # look for titles.
    elif p == '=':
        (s, c) = nl(True)
        # trim trailing \n.
        s = s[:-1]
        hb('<h%d>|</h%d>\n' % (c, c), br(s))

    # look for comments.
    elif p == '#':
        nl()

    # look for blocks.
    elif p == '~' and not inblock:
        # ignore the first line of separating ~(s).
        nl()

        if pc() == '{':
            l = br(nl())
            r = re.compile(r'(?<!\\){(.*?)(?<!\\)}', re.M)
            g = re.findall(r, l)
        elif pc() == '~':
            nl()
            continue
        else:
            g = []


        if len(g) == 0:
            out(grammar['blockstart'])
            inblock = True
        elif len(g) == 1:
            out(grammar['blockstart'])
            hb(grammar['blocktitle'], g[0])
            inblock = True
        elif len(g) == 2:
            out(grammar['codeblockstart'])
            if len(g[0]):
                hb(grammar['codetitle'], g[0])
            out(grammar['codestart'])

            # Now we are handling code.
            # Handle \~ and ~ differently.
            while 1: # wait for EOF.
                l = nl()
                if not l:
                    break
                elif l.startswith('~'):
                    break
                elif l.startswith('\\~'):
                    l = l[1:]

                out(allreplace(l))

            out(grammar['codeblockend'])
        else:
            raise SyntaxError('error on line %d' % linenum)


    elif p == '~' and inblock:
        # ditch this last line of separating ~(s).
        nl()
        inblock = False
        out(grammar['blockend'])

    else:
        s = br(np())
        if s:
            hb('<p>|</p>\n', br(np()))

out(grammar['lastbit'])
if outfile is not sys.stdout:
    outfile.close()
