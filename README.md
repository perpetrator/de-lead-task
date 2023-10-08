# Data engineering lead recrutation task

In this task your objective is to optimize and refactor given Python code.
In file `main.py` you'll find Python code which scrapes data from public free API in an
infinite loop. We are looking to:
- <del>optimize data scraping and saving</del>
- <del>create data validation mechanism - we wouldn't want to save incorrect data</del>
- <del>replace `print` statements with proper informative logging (bonus points for saving the logs in a docker volume)</del>
- <del>refactor the code in a modular manner</del>
- using docker image size reduction techniques will be appreciated

Bonus points for:
- inserting data into a transactional database (MySQL, PostgreSQL) which would run as a containerized service (`docker-compose`)
- API url is hardcoded in Dockerfile. Making url dynamic, by properly managing envs would be a plus


This is an open challenge with scope for significant development. While there is no time limit
specified for this challenge, we suggest that you budget at most 8 hours to complete this exercise.

To start local instance of ms sql server in docker:
```
docker run -e "ACCEPT_EULA=Y" -e "MSSQL_SA_PASSWORD=yourStrong(!)Password" -e "MSSQL_PID=Express" -p 1433:1433 -d mcr.microsoft.com/mssql/server:2019-latest 
```