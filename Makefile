THIS_FILE := $(lastword $(MAKEFILE_LIST))
.PHONY: build restart restart2 run del up connect stop
build:
	docker build . --tag fastapi_test
restart:
	docker stop fastapi_test
	docker start fastapi_test
	docker attach fastapi_test
restart2:
	docker stop fastapi_test
	docker container prune
	docker run -p 80:80 --name fastapi_test fastapi_test
run:
	git pull
	docker build . --tag fastapi_test
	docker run -p 80:80 --name fastapi_test fastapi_test
del:
	docker container prune
	docker rmi fastapi_test
	docker system prune
up:
	docker update --cpu-shares 512 -m 300M fastapi_test
connect:
	docker attach fastapi_test
stop:
	docker stop fastapi_test