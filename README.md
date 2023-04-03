# Employee-Control
This is a Rest API, that designed for companies. It provides such functionalities as Creating company and inviting members.</br>
Also they can request acceptance to the company. The main workflow are quizzes which company owners or admin's are able to create.</br>
Then members can pass the quizzes. There are detailed statistics with many parameters for specific companies as well as personalized for each user.</br>
Every endpoint supports validation and authentication. Moreover there is a scheduled job for every quizz</br>
to check whether all company members passed on time which sends notifications.</br>
Those have multiple uses across API. Also every endpoint is covered with tests.</br>
## Requirements 
<div align="center">

|                          Technology                          |      Version       |
| :----------------------------------------------------------: | :----------------: |
|           [**fastapi**](https://pypi.org/project/fastapi/)          |      **4.1.6**       |
|           [**uvicorn**](https://pypi.org/project/uvicorn/)          |      **0.20.0**       |
|           [**databases**](https://pypi.org/project/databases/)        |      **0.7.0**       |
|           [**aioredis[asyncpg]**](https://pypi.org/project/aioredis/)        |      **2.0.1**       |
|           [**sqlalchemy**](https://pypi.org/project/SQLAlchemy/)        |      **1.4.42**       |
|           [**pytest-asyncio**](https://pypi.org/project/pytest-asyncio/)        |      **0.20.3**       |
|           [**asyncpg**](https://pypi.org/project/asyncpg/)        |      **0.27.0**       |
|           [**alembic**](https://pypi.org/project/alembic/)        |      **1.9.4**       |
|           [**APScheduler**](https://pypi.org/project/APScheduler/)        |      **4.0.0a2**       |
|           [**pyjwt[crypto]**](https://pypi.org/project/pyjwt/)        |      **2.6.0**       |

</div>

## Getting Started 

Follow these steps to run the project

## Install and Run

Make sure you have **Python 3.x**.

Clone the repository using the following command 

```
git clone https://github.com/Motorenger/Employee-Control.git
or 
bash git clone https://github.com/Motorenger/Employee-Control.git

# After cloning, move into the project directory
cd Employee-Control
```

Run the project
```
docker-compose up --build
```

Apply migrations
```
docker exec mycontainer alembic upgrade head
```


Run tests
```
docker exec mycontainer pytest -v
```
