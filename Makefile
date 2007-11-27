.PHONY : update
update :
	@make -C doc update

.PHONY : realupdate
realupdate :
	@make -C doc realupdate

.PHONY : docs
docs :
	@make -C doc docs

.PHONY : clean
clean :
	@make -C doc clean
