#  Mini-Jira API

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=flat&logo=sqlite&logoColor=white)

A lightweight, RESTful API for task management inspired by Jira, built with **FastAPI**. This project demonstrates full CRUD operations, secure authentication with JWT tokens, robust data validation, and complete containerization using Docker.

---

##  Tech Stack

* **Backend Framework:** FastAPI
* **Database:** SQLAlchemy (ORM) + SQLite (Easily scalable to PostgreSQL)
* **Data Validation:** Pydantic
* **Security & Auth:** JWT (JSON Web Tokens), Passlib (Bcrypt for password hashing)
* **Containerization:** Docker & Docker Compose

---

##  Key Features

###  User System & Security
* **Secure Registration:** Passwords are never stored in plain text; they are securely hashed using Bcrypt.
* **JWT Authentication:** Secure login system that generates an Access Token (JWT) for session management.
* **Protected Routes:** All task-related endpoints require a valid Bearer token. 

###  Task Management (CRUD)
* **Create:** Logged-in users can create new tasks.
* **Read:** Users can retrieve a list containing *only* their own tasks (Data Isolation).
* **Update:** Ability to partially update tasks (e.g., toggling `completed: true` or changing the description) via `PATCH`.
* **Delete:** Secure deletion of owned tasks.

---

##  Project Structure

```text
mini-jira-api/
├── app/
│   ├── __init__.py
│   ├── main.py         # Application entry point & API Routes
│   ├── models.py       # SQLAlchemy Database Models
│   ├── schemas.py      # Pydantic Schemas (Input/Output validation)
│   ├── database.py     # Database engine & session configuration
│   └── auth.py         # Security logic (Hashing, JWT generation)
├── .env                # Environment variables (Ignored by Git)
├── .gitignore          # Git ignore rules
├── docker-compose.yml  # Docker services configuration
├── Dockerfile          # Image build instructions for the API
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```
##  How to Run Locally

* **Prerequisites**
  * You need Docker and Docker Compose installed on your machine.

**Step 1: Clone the repository**
```bash
git clone [https://github.com/Satanescu/mini-jira-api.git](https://github.com/Satanescu/mini-jira-api.git)
cd mini-jira-api 
```
**Step 2: Environment setup (.env)**
Create a file named .env in the root directory and add the following variables:

```ini, TOML

SECRET_KEY=your_very_long_and_secret_string_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

```

**Step 2: Environment setup (.env)**
Open your terminal and run the following command:

```bash
docker-compose up --build
```

##  API Documentation (Swagger UI)

FastAPI automatically generates interactive documentation. Once the app is running, open your browser and navigate to:

 **[http://localhost:8000/docs](http://localhost:8000/docs)**

From here, you can test all endpoints live:

1. Create a user at `POST /users/`.
2. Click the green **Authorize** button at the top (or use `POST /token`) and log in.
3. Test the `/tasks/` routes with your token automatically saved in the session.