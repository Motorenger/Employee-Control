### Meduzzen_Internship

## Getting Started 

If you are trying to use this project for the first time, you can get up and running by following these steps.

## Requirements 
<div align="center">

|                          Technology                          |      Version       |
| :----------------------------------------------------------: | :----------------: |
|           [**fastapi**](https://pypi.org/project/fastapi/)          |      **4.1.6**       |
|           [**uvicorn**](https://pypi.org/project/uvicorn/)          |      **0.20.0**       |
|           [**pytest-asyncio**](https://pypi.org/project/pytest-asyncio/)        |      **0.20.3**       |


</div>

## Install and Run

Make sure you have **Python 3.x**.

Clone the repository using the following command

```
git clone https://github.com/Motorenger/Meduzzen_Internship.git
or 
bash git clone https://github.com/Motorenger/Meduzzen_Internship.git

# After cloning, move into the directory having the project files using the change directory command
cd Meduzzen_Internship
```

Build Docker image
```
docker build -t app .
```

Run conteiner
```
docker run --name my_app -p 80:80 app
```

Run test
```
docker exec mycontainer pytest -v
```