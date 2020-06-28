
# The port was required to be a Variable.
HTTP_PORT=8080

help:		## Show this help.
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'
run:		## Builds, (re)creates, starts, and attaches to containers
	echo "HTTP_PORT=$(HTTP_PORT)" > .env  # Not extensible and hacky :(. 
	docker-compose -f docker-compose.yml up
build:	    	##Build or rebuild all services
	docker-compose -f docker-compose.yml build
up-detached:	## Builds, (re)creates, starts, and attaches to containers detached
	docker-compose -f docker-compose.yml up -d
start:		## Start existing containers
	docker-compose -f docker-compose.yml start
down:		## Stop containers
	docker-compose -f docker-compose.yml down
destroy:	## Stop containers and remove volumes
	docker-compose -f docker-compose.yml down -v
stop:		## Stops containers and removes containers, networks, volumes, and images
	docker-compose -f docker-compose.yml stop
restart:	## Restart Containers
	docker-compose -f docker-compose.yml stop
	docker-compose -f docker-compose.yml up -d
ps:		## List Containers
	docker-compose -f docker-compose.yml ps
