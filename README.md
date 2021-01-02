# WHO mortality data query engine
A set of tools to allow easy exploration of data contained in the WHO mortality dataset - https://www.who.int/data/data-collection-tools/who-mortality-database

### Initial plan
1. Build ETL pipeline to clean up data and load into database (start simple at first, remove most of unnecessary data)
2. Build API that allows questions to be asked of database, e.g. "what was the most common cause of death in Algeria in 2008"

### Future upgrades
* Build an additional pipeline to query weather averages (or other iteresting data) in each country and add that to database (make use of async API calls if necessary)
* Expand API to allow for more questions, e.g. "How many hours of daylight does Finland get each year"
* Analysis notebook that makes use of query engine to perform analysis on data and build models. E.g. "Is there a link between daylight hours and suicide rates?"

## Project components
#### Database
* Postgres database to store required data
* Make this a docker container

#### Ingest pipeline
* Loads WHO mortality datasets into a postgres database
* Transforms the data along the way (replacing codes, removing irrelevant fields, etc)
* Can eventually make this a docker container

#### Query engine
* Allows user to ask limited questions of the database, e.g. "show me mortality data for Algeria in 2008"
* Will provide an API from which the user can ask the questions, e.g. "localhost:8080/mortality?country=algeria&year=2008
* Need to research whether to use REST or graphQl
* Need to research whether to use Flask or Django (or other)
* Provide very simple FE UI that describes what queries are valid
* Will return results in JSON
* Can make this a docker container

#### Analysis notebook
* Notebook that makes use of the query engine to perform some basic analysis, e.g. "Plot mortality rates in algeria between 2000 and 2018", "Plot suicide rate per country in descending order", "Male-female heart attack ratio", etc
