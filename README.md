[![Docker](https://badgen.net/badge/icon/docker?icon=docker&label)](https://https://docker.com/)
[![CI](https://github.com/agn-7/ifsguid-backend/workflows/build/badge.svg)](https://github.com/agn-7/ifsguid-backend/actions/workflows/github-actions.yml)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![codecov](https://codecov.io/gh/agn-7/ifsguid-backend/graph/badge.svg?token=RGwuSevG8u)](https://codecov.io/gh/agn-7/ifsguid-backend)

# IFSGuid Backend
Async AI Chat Application Powered by gpt4free on top of FastAPI

## Setup
It contains two generic entity models Interaction and Message.
We store all of the data in the Postgres database.
The interaction with the database is done with the [SQLAlchemy](https://www.sqlalchemy.org/) library, and the simple GET and POST endpoints are exposed via the API, which is written with the [FastAPI](https://fastapi.tiangolo.com/) framework.

To manage dependencies, we use [poetry](https://python-poetry.org/).

To launch an API instance, you should:
1. Have a running Postgres instance, e.g. in a container. The application will read the [.env](/.env) file to access the database.
2. Create a virtual environment and install the dependencies in it. You can run `poetry install` for that.
3. Use [start_app.sh](/start_app.sh) to run the server. By default, it will bind to http://localhost:8000.
4. An automatically generated documentation can be found at http://localhost:8000/docs. The endpoints are accessible at http://localhost:8000/api/<endpoint_name>.

You can also run the project via `docker-compose` (i.e. `docker compose up -d`) on port `80` in which you would need the [.docker.env](/.docker.env) containing the following variable to create the database:

```
SQLALCHEMY_DATABASE_URI=postgresql+asyncpg://<username>:<password>@ifsguid_db/<db-name>
```


---
Here is a benchmark of the API using by [wrk](https://github.com/wg/wrk) to demonstrate the performance of the service in different configuration:

| Service      | Loading Strategy | WRK Configuration   | Throughput (reqs/sec) |
|--------------|------------------|---------------------|-----------------------|
| Async        | Joined           | 4 threads, 10 conns | 132                   |
| Async        | Selectin         | 4 threads, 10 conns | 112                   |
| Sync         | Lazy             | 4 threads, 10 conns | 36                    |
| Sync         | Joined           | 4 threads, 10 conns | 132                   |
| Sync         | Selectin         | 4 threads, 10 conns | 114                   |
| Async        | Joined           | 4 threads, 50 conns | 159                   |
| Sync         | Joined           | 4 threads, 50 conns | 1                     |
| **Async**    | **Joined**       | 4 threads, 15 conns | **126**               |
| **Sync**     | **Joined**       | 4 threads, 15 conns | **69**                |


![benchmark](https://github.com/agn-7/ifsguid-backend/assets/14202344/d435b604-f492-4fc0-b6a0-26ca3284d448)
