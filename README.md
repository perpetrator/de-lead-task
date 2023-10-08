# Data engineering lead recrutation task

In this task your objective is to optimize and refactor given Python code.
In file `main.py` you'll find Python code which scrapes data from public free API in an
infinite loop. We are looking to:
- <del>optimize data scraping and saving</del>
- <del>create data validation mechanism - we wouldn't want to save incorrect data</del>
- <del>replace `print` statements with proper informative logging (bonus points for saving the logs in a docker volume)</del>
- <del>refactor the code in a modular manner</del>
- using docker image size reduction techniques will be appreciated
  * partially: using mssql as rdbms results in heavy dependencies. Still image is lighter than original 

Bonus points for:
- <del>inserting data into a transactional database (MySQL, PostgreSQL) which would run as a containerized service (`docker-compose`</del>>
- <del>API url is hardcoded in Dockerfile. Making url dynamic, by properly managing envs would be a plus<del>


This is an open challenge with scope for significant development. While there is no time limit
specified for this challenge, we suggest that you budget at most 8 hours to complete this exercise.

