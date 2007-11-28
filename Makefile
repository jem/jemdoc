.PHONY : update
update :
	@make -C www update

.PHONY : realupdate
realupdate :
	@make -C www realupdate

.PHONY : wwws
docs :
	@make -C www docs

.PHONY : clean
clean :
	@make -C www clean
