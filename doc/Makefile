DOCS=index cheatsheet contact download revision using menu stuff

HDOCS=$(addsuffix .html, $(DOCS))
PHDOCS=$(addprefix html/, $(HDOCS))

.PHONY : update
update : $(PHDOCS)
	@echo -n 'Copying to (hidden) server...'
	@cp -r $(PHDOCS) dist/ /var/www/jemdoc/
	@echo ' done.'

.PHONY : extra
extra :
	cp ~/jemdoc/jemdoc dist/jemdoc.py
	cp ~/.vim/syntax/jemdoc.vim dist/

.PHONY : docs
docs : $(PHDOCS)

html/%.html : %.jemdoc MENU jemdoc.conf ~/jemdoc/jemdoc
	~/jemdoc/jemdoc -o $@ -c jemdoc.conf $< 

.PHONY : realupdate
realupdate : $(PHDOCS)
	@echo -n 'Copying to (hidden) server...'
	@cp -r $(PHDOCS) dist/* /var/www/jemdoc/
	@echo ' done.'
	@echo 'Copying to anteater...'
	rsync -av --delete --copy-unsafe-links /var/www/jemdoc/ anteater:/var/www/jemdoc/
	@echo ' done.'

.PHONY : clean
clean :
	-rm -f html/*.html
