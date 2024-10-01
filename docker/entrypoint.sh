#!/bin/sh
#alembic init -t async migrations
# alembic revision --autogenerate -m "add game"
echo "start fastapi app";
echo "migrate db";
# alembic upgrade head;
echo "run...";
exec "$@"