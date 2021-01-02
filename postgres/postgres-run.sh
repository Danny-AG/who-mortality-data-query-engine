#!/bin/bash

docker run -d \
	--name who_postgres  \
	--rm \
	-p 37780:5432 \
	-e POSTGRES_PASSWORD=password \
	who_postgres