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

# Default packages to use when generating output
default_packages = [
        'amsmath',
        'amsthm',
        'amssymb',
        'bm'
        ]

def __build_preamble(packages):
    preamble = '\documentclass{article}\n'
    for p in packages:
        preamble += "\usepackage{%s}\n" % p
    preamble += "\pagestyle{empty}\n\\begin{document}\n"
    return preamble

def __write_output(infile, outdir, workdir = '.', prefix = '', size = 1):
    try:
        # Generate the DVI file
        latexcmd = 'latex -interaction=nonstopmode -output-directory %s %s'\
                % (workdir, infile)
        print latexcmd
        rc = os.system(latexcmd)
        # Something bad happened, abort
        if rc != 0:
            raise Exception('latex error')

        # Convert the DVI file to PNG's
        dvifile = infile.replace('.tex', '.dvi')
        outprefix = os.path.join(outdir, prefix)
        dvicmd = "dvipng -T tight -x %i -z 9 -bg Transparent "\
                "-o %s.png %s" % (size * 1000, outprefix, dvifile)
        rc = os.system(dvicmd)
        if rc != 0:
            raise Exception('dvipng error')
    finally:
        # Cleanup temporaries
        basefile = infile.replace('.tex', '')
        tempext = [ '.aux', '.dvi', '.log' ]
        for te in tempext:
            tempfile = basefile + te
            if os.path.exists(tempfile):
                os.remove(tempfile)


def math2png(eqs, outdir, packages = default_packages, prefix = '', size = 1):
    """
    Generate png images from $...$ style math environment equations.

    Parameters:
        eqs         - A list of equations
        outdir      - Output directory for PNG images
        packages    - Optional list of packages to include in the LaTeX preamble
        prefix      - Optional prefix for output files
        size        - Scale factor for output
    """
    try:
        # Set the working directory
        workdir = tempfile.gettempdir()

        # Get a temporary file
        fd, texfile = tempfile.mkstemp('.tex', 'eq', workdir, True)

        # Create the TeX document
        #with os.fdopen(fd, 'w+') as f:
        f = os.fdopen(fd, 'w+')
        f.write(__build_preamble(packages))
        for eq in eqs:
            f.write("$%s$\n\\newpage\n" % eq)
        f.write('\end{document}')

        __write_output(texfile, outdir, workdir, prefix, size)
    finally:
        if os.path.exists(texfile):
            os.remove(texfile)
