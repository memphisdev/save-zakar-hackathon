.ONESHELL:

conda_env:
	conda env create -f environment.yml
	conda activate save-zakar
raw_tables:
	python3 src/zakar/warehouse/create_raw_tables.py
truncate_raw_tables:
	python3 src/zakar/warehouse/truncate_raw_tables.py
postgres_consume: raw_tables
	python3 src/zakar/postgres_consumer.py

dashboard:
	streamlit run streamlit/Welcome.py

csv_in_postgres:
	for file in tweets fire_alerts temperature_readings ; do \
		PGPASSWORD=${DATABASE_PASSWORD} psql -h ${POSTGRES_HOST} -d postgres -U postgres -c "\copy raw.$$file from 'data/raw/$$file.csv' with delimiter as ',' csv header;" ; \
	done