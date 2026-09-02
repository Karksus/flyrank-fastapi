# FlyRank - AI Backend Track - Build you first CRUD API

##  Task API with FastAPI & SQLModel

A simple, lightweight CRUD API built with FastAPI and SQLModel, backed by PostgreSQL.

## Database Design & Persistence

* **Why PostgreSQL was chosen:** PostgreSQL is a production-grade relational database with robust concurrency, ACID compliance, and rich data types.
* **How to run it:** A Docker container provides the database with zero host-side installation. Data persists in a named Docker volume across restarts.
* **Configuration:** The database password is read from a `.env` file (variable `DATABASE_PASSWORD`). Create a `.env` in the project root with `DATABASE_PASSWORD=dev` before running. It is already gitignored.

### How to run it

1 - Clone this repo:

```bash
git clone https://github.com/Karksus/flyrank-fastapi.git
cd flyrank-fastapi
```
2 - Start a `uv` project and install dependencies:
```bash
uv init .
uv add "fastapi[standard]" psycopg2-binary python-dotenv
```
3 - Create a `.env` file with your database password:
```bash
echo "DATABASE_PASSWORD=dev" > .env
```
4 - Start a PostgreSQL container:
```bash
docker run \
    --name taskdb \
    -e POSTGRES_PASSWORD=dev \
    -e POSTGRES_DB=tasks \
    -p 5432:5432 \
    -v taskdata:/var/lib/postgresql/data \
    -d postgres
```
5 - Start `FASTAPI` app (dev)
```bash
uv run fastapi dev
```

### Docker & PostgreSQL Usage

```bash
docker run \
    --name taskdb \
    -e POSTGRES_PASSWORD=dev \
    -e POSTGRES_DB=tasks \
    -p 5432:5432 \
    -v taskdata:/var/lib/postgresql/data \
    -d postgres
```

```bash
docker ps -a
```

```bash
docker image ls
```

```bash
docker logs taskdb
```

```bash
docker exec -it taskdb psql -U postgres -d tasks
```

The project holds a full CRUD example, with `GET`, `POST`, `PUT` and `DELETE` HTTP methods.

|Method|Endpoint        |Description                                              |
|------|----------------|---------------------------------------------------------|
|GET   |/               |Holds API info and metadata                              |
|GET   |/health         |Classic API health check                                 |
|GET   |/tasks/{task_id}|Gets a specific task by its ID                           |
|POST  |/tasks/         |Creates a new task                                       |
|PUT   |/tasks/{task_id}|Updates an existing task's title and/or completion status|
|DELETE|/tasks/{task_id}|Removes a task by its ID                                 |


### GET /ROOT - Holds API info
```bash
curl -i http://127.0.0.1:8000/
```
<img width="333" height="297" alt="image" src="https://github.com/user-attachments/assets/52d50217-651e-4749-a1ce-82fa02ad2118" />

### GET /HEALTH - Classic API health check
```bash
curl -i http://127.0.0.1:8000/health
```
<img width="320" height="236" alt="image" src="https://github.com/user-attachments/assets/a4197e50-94f5-436d-b9a2-f1acc4bb6807" />

### GET /tasks/{task_id} - Gets task id
> SQLModel/SQLAlchemy parameterizes queries behind the scenes (e.g. `WHERE id = %s`), so the id is passed as a bound parameter rather than glued into the SQL string — preventing SQL injection such as `SELECT * FROM tasks WHERE id = $1`/`WHERE id = %s`.
```bash
curl -i http://127.0.0.1:8000/tasks/1
```
<img width="212" height="163" alt="image" src="https://github.com/user-attachments/assets/d6051ea2-0929-4d87-9370-a20fac85c27e" />

<img width="391" height="270" alt="image" src="https://github.com/user-attachments/assets/474ccdb1-cd95-4c17-adc3-991180d33905" />

### POST /tasks/ - Creates a task
```bash
curl -i -X POST "http://127.0.0.1:8000/tasks" \
     -H "Content-Type: application/json" \
     -d '{"title": "Something you should know about FASTAPI"}'
```
<img width="333" height="232" alt="image" src="https://github.com/user-attachments/assets/e3afe595-8f9a-4c36-88c2-71a9df2197eb" />

<img width="413" height="272" alt="image" src="https://github.com/user-attachments/assets/6bb24c2e-9668-4b9f-bd1c-5adc43ee6b1c" />

### PUT /tasks/ - Updates a task
```bash
curl -i -X PUT "http://127.0.0.1:8000/tasks/2" \
     -H "Content-Type: application/json" \
     -d '{"title": "Something you should know about FASTAPI", "done": true}'
```
<img width="353" height="380" alt="image" src="https://github.com/user-attachments/assets/d1966a91-9bf9-410a-9bb9-3b22f0ddd7c0" />

<img width="419" height="270" alt="image" src="https://github.com/user-attachments/assets/a5816dd8-22d4-4cf0-969d-f4484094d775" />

### DELETE /tasks/ - Deletes a task
```bash
curl -i -X DELETE "http://127.0.0.1:8000/tasks/2"
```
<img width="315" height="202" alt="image" src="https://github.com/user-attachments/assets/2c63e1dd-ef5f-4b74-95d0-21cb262182fd" />

<img width="316" height="146" alt="image" src="https://github.com/user-attachments/assets/5b12f716-d0ca-4c72-a545-e7401381bf95" />

---
## AI vs Me

I built `main.py` step by step, endpoint by endpoint. Then I asked an AI to generate its own version from a single detailed prompt describing the same API.

### What did the AI do better?

The AI version is more polished in several concrete ways:

- I built every endpoint except the one that lists all tasks. The AI included `GET /tasks` without being asked.
- The AI version is more concise: it uses inline `Session` blocks instead of a separate `SqlOperator` class, making it shorter and arguably easier to follow for a toy project.
- The AI version sets a default value on `done` (`done: bool = False`), so a `Task` can be created without explicitly passing it. My model has `done: bool` with no default, meaning it must always be provided.
I understand the AI version well enough to explain every line, but the gap is real: it took me several focused sessions to reach the state I have, and the AI produced something objectively more complete in one shot.

### What did the AI get wrong or quietly ignore?

- **No `400` on empty request body for `PUT`.** My version explicitly checks whether the client sent an empty body (`title` and `done` are both `None`) and returns a `400 Bad Request`. The AI version silently accepts it and returns the task unchanged.
- **No dependency injection.** The AI version opens a new `Session` block inside every endpoint. My version uses FastAPI's `Depends(get_session)` pattern, which makes testing easier.
- **No input validation on `PUT` title.** The AI checks `if task_in.title is not None` but doesn't `.strip()` and re-validate the title. My version catches whitespace-only titles like `"   "` and rejects them with a `400`.
- **Typo in my code.** Line 149 of my `main.py` has `status_status_code` instead of `status_code` — a bug the AI version doesn't have.

### What did my prompt forget to specify — and what did the AI silently decide for you?

I never told the AI:

- **Which endpoints to include.** I described the CRUD operations but didn't explicitly say "include a `GET /tasks` to list all tasks." The AI decided to add it.
- I didn't say "use inline sessions" or "use dependency injection." The AI chose inline sessions.
- I didn't specify `{"error": "..."}` vs `{"detail": "..."}`. The AI went with the same `{"error": ...}` pattern I used.

Conclusion: the AI is a better FastAPI practitioner than I am right now, but it also makes a dozen silent decisions that a human reviewer needs to catch. My version has better architecture (dependency injection, reusable operator class) while the AI's is cleaner and more complete.
