#!/bin/sh
poetry run alembic upgrade head
poetry run fastapi run wg_service
