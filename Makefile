
build-docker:
	cd docker && docker build -t audioset_augmentor:latest .

start-docker:
	docker run -it -v $(shell pwd):/audioset_augmentor --rm audioset_augmentor:latest

	
	