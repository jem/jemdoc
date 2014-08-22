jemdoc+MathJax
==============
jemdoc is a light text-based markup language designed for creating websites.  See http://jemdoc.jaboc.net/ for more information and the detailed usage of jemdoc.

jemdoc+MathJax adds the MathJax support to jemdoc.  You can use the same jemdoc syntax, but the equations will be rendered by MathJax.  See http://web.stanford.edu/~wsshin/jemdoc+mathjax.html for more information and examples. 

What's new in jemdoc+MathJax
--------------------------------------
- MathJax support
- Underscore
- Control of the behavior of links: open in the current web broswer tab or in a new tab

How to use jemdoc+MathJax
-------------------------
Once you download jemdoc+MathJax, you can install and use it like the original jemdoc.  See the [jemdoc user guide](http://jemdoc.jaboc.net/using.html), expecially the [example page](http://jemdoc.jaboc.net/example.html).

The usage of the additional features implemented in jemdoc+MathJax can be found in example/ directory in this package.  The directory contains jemdoc source files that create an example website that demonstrates the additional features.  To build the website, execute the following command in this example/ directory:

	../jemdoc -c mysite.conf *.jemdoc

This generates a few HTML files, which you can open in any web browser to see the results.  

MathJax configuration is done in mysite.conf.  Change mysite.conf to control the behavior of MathJax.

Disclaimer
----------
The focus of the implementation of the additional features was to "make them just work," so the implementation is suboptimal, both in terms of performance and style.  

Still, several users and I find jemdoc+MathJax is quite stable and does the job correctly :-)

Wonseok Shin

README of the original jemdoc
-----------------------------
> jemdoc is a light text-based markup language designed for creating websites. It
> takes a text file written with jemdoc markup, an optional configuration file and
> an optional menu file, and makes static websites that look something like
> http://jemdoc.jaboc.net/.
> 
> It was written by me, Jacob Mattingley, in 2007, and definitely isn't the type
> of code I would put on my CV. Lots of people use jemdoc, especially in academia.
> 
> Much more info at http://jemdoc.jaboc.net/.

