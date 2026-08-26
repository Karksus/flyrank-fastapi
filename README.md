# FlyRank - AI Backend Track - Build you first CRUD API

##  Task API with FastAPI & SQLModel

A simple, lightweight CRUD API built with FastAPI and SQLModel, backed by a persistent SQLite database.

## Database Design & Persistence

* **Why SQLite was chosen:** SQLite was chosen because it is lightweight, requires **zero setup** or external server configuration, stores everything in a **single file**, and **survives restarts** to preserve your data between sessions.
* **Where the database file lives:** The database file is named **`tasks.db`** and is created automatically in your project root upon startup. It is typically included in `.gitignore` so that each new clone of the repository starts with a fresh database.

### How to run it

1 - Clone this repo:

```bash
git clone https://github.com/Karksus/flyrank-fastapi.git
cd flyrank-fastapi
```
2 - Start a `uv` project and install `FASTAPI`:
```bash
uv init .
uv add "fastapi[standard]"
```
3 - Start `FASTAPI` app (dev)
```bash
uv run fastapi dev
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
## DB-Browser example

### Database
<img width="377" height="209" alt="image" src="https://github.com/user-attachments/assets/f2827846-e8a3-4442-964e-12b2a6c41cdd" />

### Query
<img width="367" height="376" alt="image" src="https://github.com/user-attachments/assets/d507c973-d993-4583-8968-550ab71cbb68" />

## AI vs Me

I built `main.py` step by step, endpoint by endpoint. Then I asked an AI to generate its own version from a single detailed prompt describing the same API.

### What did the AI do better?

The AI version is more polished in several concrete ways:

- I built every endpoint except the one that lists all tasks — the most obvious starting point for any CRUD API. The AI included it without being asked.
- AI declared `response_model=Task` or `response_model=List[Task]` on each route, which gives you automatic Pydantic validation of the response and proper OpenAPI schema output. I return raw dicts and FastAPI just trusts them.
- The AI raises `HTTPException` with `detail`, which FastAPI serializes into a standard `{"detail": "..."}` error body. I manually set `response.status_code` and return an `{"error": ...}` .
- The AI version groups endpoints into tags (`Tasks`, `Root`, `Health Check`) and adds summary lines, so the `/docs` page is actually organized. Mine is a flat wall of endpoints with no grouping.
- Pydantic used to enforce input lenght validation, while I do manual `.strip()` checks.

I understand the AI version well enough to explain every line, but the gap is real: it took me several focused sessions to reach the state I have, and the AI produced something objectively more complete in one shot.

### What did the AI get wrong or quietly ignore?

- **No `400` on empty request body for `PUT`.** My version explicitly checks whether the client sent an empty body (`title` and `done` are both `None`) and returns a `400 Bad Request`. The AI version silently accepts it and returns the task unchanged.
- `Optional[str]` with `min_length` doesn't reject an empty string in the same way. If a client sends `"   "`, my version catches it; the AI version would pass it through (min_length counts whitespace characters).

### What did my prompt forget to specify — and what did the AI silently decide for you?

I never told the AI:

- **Which endpoints to include.** I described the CRUD operations but didn't explicitly say "include a `GET /tasks` to list all tasks." The AI decided to add it.
- I didn't say "use `HTTPException`" or "use the `Response` object.".
- I never specified min/max title length. The AI invented `min_length=3, max_length=100`.
- I didn't specify `{"error": "..."}` vs `{"detail": "..."}`. The AI went with FastAPI's convention.

Conclusion: the AI is a better FastAPI practitioner than I am right now, but it also makes a dozen silent decisions that a human reviewer needs to catch.
