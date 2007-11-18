" Vim syntax file
" Language:     jemdoc
" Author:       Jacob Mattingley <jacobm@stanford.edu> (inspired by
"               Stuart Rackham's asciidoc).
" Last Change:  jemdoc 0.1.1
" URL:          http://jaboc.net/
" Licence:      GPL (http://www.gnu.org)
" Remarks:      Vim 6 or greater
" Limitations:  See 'Appendix J: Vim Syntax Highlighter' in the AsciiDoc 'User
"               Guide'.

"if exists("b:current_syntax")
"  finish
"endif

syn clear
syn sync fromstart " change this if it gets slow.
syn sync linebreaks=1

" Run :help syn-priority to review syntax matching priority.
"
" remove about 100 of the backslashes in what follows.
syn keyword jemdocToDo TODO FIXME XXX ZZZ
syn match jemdocQuotedCharError /\\./
syn match jemdocQuotedChar /\\[\\\*{}\/\.\-\+"=~n#%RC`'\$%]/
syn match jemdocListBullet /^\s*[-.:]\+\s/
syn match jemdocCommentLine "\\\@<!#.*$" contains=jemdocToDo
syn region jemdocMonospaced start=/\(\\\\\)*\\\@<!+/ end=/\(\\\\\)*\\\@<!+/
syn region jemdocEmphasized start=/\(\\\\\)*\\\@<!\/\S/ end=/\(\\\\\)*\\\@<!\//
syn region jemdocBold start=/\(\\\\\)*\\\@<!\*\S/ end=/\(\\\\\)*\\\@<!\*/
syn region jemdocLink start=/\(\\\\\)*\\\@<!\[/ end=/\(\\\\\)*\\\@<!\]/
syn match jemdocOneLineTitle /^=\{1,5}\s\+\S.*$/
syn region jemdocBlock start=/^\~\{3,}$/ end=/^\~\{3,}$/ contains=jemdocBlockTitle
syn region jemdocBlockTitle start=/^{/ end=/}$/ contained
syn match jemdocLiteralBackslash /\(\\\\\)\+/

" Define this item last.
syn region jemdocBracedPassthrough start=/+\?{{/ end=/}}+\?/
syn region jemdocDollarPassThrough start=/\\\@<!%/ end=/\\\@<!%/

highlight link jemdocMacroAttributes Label
highlight link jemdocIdMarker Special
highlight link jemdocBlockTitle Special
highlight link jemdocLink Type
highlight link jemdocOneLineTitle Title
highlight link jemdocMacro Macro
highlight link jemdocAnchorMacro Macro 
highlight link jemdocEmail Macro
highlight link jemdocListBullet Special
highlight link jemdocListNumber Label
highlight link jemdocBlock Structure
highlight link jemdocPassthroughBlock Identifier
highlight link jemdocCommentBlock Comment
highlight link jemdocFilterBlock Type
highlight link jemdocBold Special
highlight link jemdocEmphasized Type
highlight link jemdocMonospaced Identifier
highlight link jemdocToDo Todo
highlight link jemdocCommentLine Comment
highlight link jemdocQuotedChar Special
highlight link jemdocQuotedCharError Error
highlight link jemdocCallout Label
highlight link jemdocLineBreak Special
highlight link jemdocRuler Type

" Special highlighting for this one.
highlight link jemdocLiteralBackslash Keyword

" Define this one last.
highlight link jemdocBracedPassthrough Special
highlight link jemdocDollarPassThrough Special

let b:current_syntax = "jemdoc"

" vim: wrap et sw=2 sts=2:
