### Meduzzen_Internship

## Getting Started 

If you are trying to use this project for the first time, you can get up and running by following these steps.

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

## Install and Run

Make sure you have **Python 3.x**.

Clone the repository using the following command 

```
git clone https://github.com/Motorenger/Meduzzen_Internship.git
or 
bash git clone https://github.com/Motorenger/Meduzzen_Internship.git

# After cloning, move into the project directory
cd Meduzzen_Internship
```

Run the project
```
docker-compose up  --build
```

Apply migrations
```
docker exec mycontainer alembic upgrade head
```


Run tests
```
docker exec mycontainer pytest -v
```
