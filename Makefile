.PHONY: serve
serve: 
	source bin/activate && gunicorn pantsbot:app &
