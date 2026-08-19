## FlyRank - AI Backend Track - Build you first CRUD API

The current repository holds a toy example o CRUD implementation using FASTAPI.

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

<img width="309" height="199" alt="image" src="https://github.com/user-attachments/assets/e4bdd8ff-1713-4c4e-9e84-f48265dacfc1" />


### GET /ROOT - Holds API info
<img width="333" height="297" alt="image" src="https://github.com/user-attachments/assets/52d50217-651e-4749-a1ce-82fa02ad2118" />

### GET /HEALTH - Classic API health check
<img width="320" height="236" alt="image" src="https://github.com/user-attachments/assets/a4197e50-94f5-436d-b9a2-f1acc4bb6807" />

### GET /tasks/{task_id} - Gets task id
<img width="212" height="163" alt="image" src="https://github.com/user-attachments/assets/d6051ea2-0929-4d87-9370-a20fac85c27e" />

<img width="391" height="270" alt="image" src="https://github.com/user-attachments/assets/474ccdb1-cd95-4c17-adc3-991180d33905" />

### POST /tasks/ - Creates a task
<img width="333" height="232" alt="image" src="https://github.com/user-attachments/assets/e3afe595-8f9a-4c36-88c2-71a9df2197eb" />

<img width="413" height="272" alt="image" src="https://github.com/user-attachments/assets/6bb24c2e-9668-4b9f-bd1c-5adc43ee6b1c" />

### PUT /tasks/ - Updates a task
<img width="353" height="380" alt="image" src="https://github.com/user-attachments/assets/d1966a91-9bf9-410a-9bb9-3b22f0ddd7c0" />

<img width="419" height="270" alt="image" src="https://github.com/user-attachments/assets/a5816dd8-22d4-4cf0-969d-f4484094d775" />

### DELETE /tasks/ - Deletes a task
<img width="315" height="202" alt="image" src="https://github.com/user-attachments/assets/2c63e1dd-ef5f-4b74-95d0-21cb262182fd" />

<img width="316" height="146" alt="image" src="https://github.com/user-attachments/assets/5b12f716-d0ca-4c72-a545-e7401381bf95" />
