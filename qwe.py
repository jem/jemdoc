import sys
import re

#inname = sys.argv[1]
#outname = sys.argv[2]
def readnoncomment(f):
    l = f.readline()
    if l == '':
        return l
    elif l[0] == '#': # jem: be a little more generous with the comments we accept?
        return readnoncomment(f)
    else:
        return l.rstrip() + '\n' # leave just one \n and no spaces etc.

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

def insertmenuitems(mname, current):
    f = open(mname)
    while pc(f) != '':
        l = readnoncomment(f)
        l = l.strip()
        if l == '':
            continue

        r = re.match(r'\s*(.*?)\s*\[(.*)\]', l)

        if r: # then we have a link.
            if r.group(2) == current: 
                hb(grammar['currentmenuitem'], r.group(2), br(r.group(1)))
            else:
                hb(grammar['menuitem'], r.group(2), br(r.group(1)))

        else: # menu category.
            hb(grammar['menucategory'], br(l))

    f.close()

inname = 'test.jemdoc'
outname = 'test.html'

infile = open(inname)
outfile = sys.stdout # open(outname, 'w')

def out(s):
    outfile.write(s)

def hb(tag, content1, content2=None):
    """Writes out a halfblock (hb)."""
    if content2 is None:
        out(re.sub(r'\|', content1, tag))
    else:
        r = re.sub(r'\|1', content1, tag)
        r = re.sub(r'\|2', content2, r)
        out(r)

def pc(f = infile):
    """Peeks at next character in the file."""
    # Should only be used to look at the first character of a new line.
    c = f.read(1)
    if c: # only undo forward movement if we're not at the end.
        #if c == '#': # interpret comment lines as blank.
        #    return '\n'

        if c in ' \t':
            return pc()

        f.seek(-1, 1)

    return c

def nl(withcount=False):
    global linenum
    """Get input file line."""
    s = infile.readline()
    linenum += 1
    # remove any special characters - assume they were checked by pc() before
    # we got here.
    s = s.lstrip(' \t')

    # remove any trailing comments.
    s = re.sub(r'\s*(?<!\\)#.*', '', s)

    if withcount:
        if s[0] == '.':
            m = r'\.'
        else:
            m = s[0]

        r = re.match('(%s+) ' % m, s)
        if not r:
            raise SyntaxError('error (code 12039) on line %d' % linenum)

        s = s.lstrip('-.=')

        return (s, len(r.group(1)))
    else:
        s = s.lstrip('-.=')

        return s



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

linenum = 0

menu = None
if pc() == '#':
    l = infile.readline()
    linenum += 1
    if l.startswith('# jemdoc: '):
        l = l[len('# jemdoc: '):]
        a = l.split(',')
        # jem only handle one argument for now.
        b = a[0]
        b = b.strip()
        if b.startswith('sidemenu'):
            sidemenu = True
            r = re.compile(r'(?<!\\){(.*?)(?<!\\)}', re.M)
            g = re.findall(r, l)
            if len(g) != 2:
                raise SyntaxError('sidemenu error on line %d' % linenum)

            menu = (g[0], g[1])


# Look for a title.
if pc() == '=': # don't check exact number of '=' here jem.
    t = br(nl())[:-1]
    hb(grammar['windowtitle'], t)
    out(grammar['bodystart'])

else:
    out(grammar['bodystart'])
    t = None

if menu:
    out(grammar['menustart'])
    insertmenuitems(*menu)
    out(grammar['menuend'])
else:
    out(grammar['nomenu'])

if t is not None:
    hb(grammar['doctitle'], t)

    # Look for a subtitle.
    if pc() != '\n':
        hb(grammar['subtitle'], br(np()))

def pyint(l):
    l = l.rstrip()
    if l.startswith('>>>'):
        hb('<span class="pycommand">|</span>\n', allreplace(l))
    else:
        out(allreplace(l) + '\n')

# Now (just for the moment) do the rest of the in-text substitutions.
while 1: # wait for EOF.
    p = pc()

    if p == '':
        break

    # look for lists.
    elif p == '-':
        level = 0

        while pc() == '-':
            (s, newlevel) = np(True)

            # first adjust list number as appropriate.
            if newlevel > level:
                for i in range(newlevel - level):
                    if newlevel > 1:
                        out('\n')
                    out('<ul>\n<li>')
            elif newlevel < level:
                for i in range(level - newlevel):
                    out('</li>\n</ul>\n</li><li>')
            else:
                out('</li>\n<li>')

            out(br(s))
            level = newlevel

        for i in range(level):
            out('</li>\n</ul>\n')

    elif p == '.':
        level = 0

        while pc() == '.':
            (s, newlevel) = np(True)

            # first adjust list number as appropriate.
            if newlevel > level:
                for i in range(newlevel - level):
                    if newlevel > 1:
                        out('\n')
                    out('<ol>\n<li>')
            elif newlevel < level:
                for i in range(level - newlevel):
                    out('</li>\n</ol>\n</li><li>')
            else:
                out('</li>\n<li>')

            out(br(s))
            level = newlevel

        for i in range(level):
            out('</li>\n</ol>\n')

    # look for titles.
    elif p == '=':
        (s, c) = nl(True)
        # trim trailing \n.
        s = s[:-1]
        hb('<h%d>|</h%d>\n' % (c, c), br(s))

    # look for comments.
    elif p == '#':
        nl()

    elif p == '\n':
        nl()

    # look for blocks.
    elif p == '~':
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

        if len(g) in (0, 1): # info block.
            out(grammar['infoblock'])
            
            if len(g) == 1: # info block.
                hb(grammar['blocktitle'], g[0])

            out(grammar['infoblockcontent'])

            while 1: # wait for EOF.
                if pc() == '~':
                    out(grammar['infoblockend'])
                    nl()
                else:
                    l = np()
                    if not l:
                        break
                    elif l.startswith('\\~'):
                        l = l[1:]

                    out(br(l) + '\n')

        elif len(g) == 2: # code block.
            out(grammar['codeblock'])
            if len(g[0]):
                hb(grammar['blocktitle'], g[0])
            out(grammar['codeblockcontent'])

            if g[1] not in ('', 'pyint'):
                raise SyntaxError('unrecognised syntax '
                                  'highlighting on line %d' % linenum)

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

                if g[1] == 'pyint':
                    pyint(l)
                else:
                    out(allreplace(l))

            out(grammar['codeblockend'])
        else:
            raise SyntaxError('error (code 0192977) on line %d' % linenum)

    else:
        s = br(np())
        if s:
            hb('<p>|</p>\n', s)

if menu:
    out(grammar['menulastbit'])
else:
    out(grammar['nomenulastbit'])

if outfile is not sys.stdout:
    outfile.close()
