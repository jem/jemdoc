#!/usr/bin/python2.5
#from __future__ import with_statement # Until Python 2.6
"""
Converts LaTeX math to png images.
Run latexmath2png.py --help for usage instructions.
"""

"""
Author:
    Kamil Kisiel <kamil@kamilkisiel.net>
    URL: http://www.kamilkisiel.net

Revision History:
    2007/04/20 - Initial version

TODO:
    - Make handling of bad input more graceful?
---

Some ideas borrowed from Kjell Fauske's article at http://fauskes.net/nb/htmleqII/

Licensed under the MIT License:

Copyright (c) 2007 Kamil Kisiel <kamil@kamilkisiel.net>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS 
IN THE SOFTWARE.
"""

import os
import sys
import tempfile
import getopt
from StringIO import StringIO
from subprocess import *

# Default packages to use when generating output
default_packages = [
        #'amsmath',
        #'amsthm',
        #'amssymb',
        ]

def __build_preamble(packages):
    preamble = '\documentclass{article}\n'
    for p in packages:
        preamble += "\usepackage{%s}\n" % p
    #preamble += "\usepackage[active]{preview}\n"
    preamble += "\pagestyle{empty}\n\\begin{document}\n"
    return preamble

def __write_output(infile, outdir, workdir = '.', prefix = '', dpi = 100):
    try:
        # Generate the DVI file
        latexcmd = 'latex -file-line-error-style -interaction=nonstopmode -output-directory %s %s'\
                % (workdir, infile)
        p = Popen(latexcmd, shell=True, stdout=PIPE)
        rc = p.wait()

        # Something bad happened, abort
        if rc != 0:
            print p.stdout.read()
            raise Exception('latex error')


        # Convert the DVI file to PNG's
        dvifile = infile.replace('.tex', '.dvi')
        outprefix = os.path.join(outdir, prefix)
        dvicmd = "dvipng --freetype0 -Q 8 --depth -q -T tight -D %i -z 3 -bg Transparent "\
                "-o %s.png %s" % (dpi, outprefix, dvifile)
        p = Popen(dvicmd, shell=True, stdout=PIPE)
        rc = p.wait()
        if rc != 0:
            raise Exception('dvipng error')
        depth = int(p.stdout.readlines()[-1].split('=')[-1])
    finally:
        # Cleanup temporaries
        basefile = infile.replace('.tex', '')
        tempext = [ '.aux', '.dvi', '.log' ]
        for te in tempext:
            t = basefile + te
            if os.path.exists(t):
                os.remove(t)

    return depth

def math2png(eq, outdir, packages = default_packages, prefix = '', dpi = 100):
    #try:

    # Set the working directory
    workdir = tempfile.gettempdir()

    # Get a temporary file
    fd, texfile = tempfile.mkstemp('.tex', '', workdir, True)

    # Create the TeX document
    #with os.fdopen(fd, 'w+') as f:
    f = os.fdopen(fd, 'w')
    f.write(__build_preamble(packages))
    f.write("$%s$\n" % eq)
    f.write('\end{document}')
    f.close()

    depth = __write_output(texfile, outdir, workdir, prefix, dpi)

    #finally:
    #    pass
    #    #if os.path.exists(texfile):
    #    #    os.remove(texfile)

    return depth

def math2pngwl(eq, outdir, packages = default_packages, prefix = '', dpi = 100):
    #try:

    # Set the working directory
    workdir = tempfile.gettempdir()

    # Get a temporary file
    fd, texfile = tempfile.mkstemp('.tex', '', workdir, True)

    # Create the TeX document
    #with os.fdopen(fd, 'w+') as f:
    f = os.fdopen(fd, 'w')
    f.write(__build_preamble(packages))
    f.write("\\[%s\\]\n\\newpage\n" % eq)
    f.write('\end{document}')
    f.close()

    depth = __write_output(texfile, outdir, workdir, prefix, dpi)

    #finally:
    #    pass
    #    #if os.path.exists(texfile):
    #    #    os.remove(texfile)

    return depth
