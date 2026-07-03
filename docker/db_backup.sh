#!/bin/bash
docker compose exec -T db pg_dump -U postgres django_boiler > /home/ubuntu/db_dump.sql
