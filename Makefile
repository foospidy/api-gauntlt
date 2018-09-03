FROM?=RAML
TO?=OAS20
SOURCE?=changeme

build:
	docker build -t api-gauntlt .

build-no-cache:
	docker build --no-cache -t api-gauntlt .

run:
	docker run -i -v $(PWD)/input/:/input \
		-e FROM="$(FROM)" \
		-e TO="$(TO)" \
		-e SOURCE="$(SOURCE)" \
		-t api-gauntlt /bin/bash

scenarios:
	docker run -v $(PWD)/input/:/input \
		-e FROM="$(FROM)" \
		-e TO="$(TO)" \
		-e SOURCE="$(SOURCE)" \
		-t api-gauntlt /convert.sh
