
# WHO mortality data query engine (WIP)
A set of tools to allow easy exploration of data contained in the ICD10 revision of the WHO mortality dataset - https://www.who.int/data/data-collection-tools/who-mortality-database

### Note: This repo is a work in progress and is still under development
# Current functionality
* Build and deploy a containerised (using Docker) PostgreSQL database that can model a simplified view of the WHO ICD10 mortality rates dataset. The simplified view consists of the following data attributes:
	* Country - Country of death (in plain text)
	* Year - Year of death
	* Cause - Cause of death (in plain text)
	* Sex - Sex of the deceased
	* Deaths - Total number of deaths for the above defined group
* ETL pipeline to download raw mortality rates data from the WHO website, transform into a human readable format, and write to postgres database.
	* Note as this is an initial implementation, the granular age range data has been ignored, instead only total number of deaths is considered.
	* Transformations include:
		* Replacing country codes with human readable country names
		* Replacing cause codes with human readable causes of death
		* Replacing sex codes with human readable 'm', 'f' or 'u'

# Deployment
Deployment instructions are as followed:

To deploy the whole pipeline, including deployment of database, run `deploy.sh`

To deploy the database in isolation, navigate to the postgres directory and run `postgres-build.sh` followed by `postgres-run.sh`

To run the ingest pipeline in isolation run `python -m pipeline.run_pipeline`
# Future functionality

### Initial plan
1. Build ETL pipeline to clean up data and load into database (start simple at first, remove most of unnecessary data)
2. Build API that allows questions to be asked of database, e.g. "what was the most common cause of death in Algeria in 2008"

### Future upgrades
* Build an additional pipeline to query weather averages (or other iteresting data) in each country and add that to database (make use of async API calls if necessary)
* Expand API to allow for more questions, e.g. "How many hours of daylight does Finland get each year"
* Analysis notebook that makes use of query engine to perform analysis on data and build models. E.g. "Is there a link between daylight hours and suicide rates?"

## Project components
#### Database
* Containerised PostgreSQL database to store required data

#### Ingest pipeline
* Loads WHO mortality datasets into a postgres database
* Transforms the data along the way (replacing codes, removing irrelevant fields, etc)
