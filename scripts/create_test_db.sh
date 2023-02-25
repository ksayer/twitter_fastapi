#!/bin/bash

set -e
set -u

function create_user_and_database() {
	local database=$1
	echo "  Creating  database '$database'"
	psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" -d postgres <<-EOSQL
	    CREATE DATABASE $database;
	    GRANT ALL PRIVILEGES ON DATABASE $database TO "$POSTGRES_USER";
EOSQL
}

if [[ -v INSTALL_DEV && "$INSTALL_DEV" == "True" ]]; then
	create_user_and_database $TEST_POSTGRES_DB
fi