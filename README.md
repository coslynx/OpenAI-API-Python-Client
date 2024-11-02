<div class="hero-icon" align="center">
  <img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-markdown-open.svg" width="100" />
</div>

<h1 align="center">
OpenAI-API-Python-Client
</h1>
<h4 align="center">A Python backend API wrapper that simplifies integration of OpenAI's powerful NLP capabilities.</h4>
<h4 align="center">Developed with the software and tools below.</h4>
<div class="badges" align="center">
  <img src="https://img.shields.io/badge/Language-Python-blue" alt="Programming Language">
  <img src="https://img.shields.io/badge/Framework-FastAPI-red" alt="Web Framework">
  <img src="https://img.shields.io/badge/Database-PostgreSQL-blue" alt="Database">
  <img src="https://img.shields.io/badge/API-OpenAI-black" alt="API Integration">
</div>
<div class="badges" align="center">
  <img src="https://img.shields.io/github/last-commit/coslynx/OpenAI-API-Python-Client?style=flat-square&color=5D6D7E" alt="git-last-commit" />
  <img src="https://img.shields.io/github/commit-activity/m/coslynx/OpenAI-API-Python-Client?style=flat-square&color=5D6D7E" alt="GitHub commit activity" />
  <img src="https://img.shields.io/github/languages/top/coslynx/OpenAI-API-Python-Client?style=flat-square&color=5D6D7E" alt="GitHub top language" />
</div>

## 📑 Table of Contents
- 📍 Overview
- 📦 Features
- 📂 Structure
- 💻 Installation
- 🏗️ Usage
- 🌐 Hosting
- 📄 License
- 👏 Authors

## 📍 Overview

This repository provides a Minimum Viable Product (MVP) called "OpenAI-API-Python-Client". It offers a user-friendly Python backend API wrapper that simplifies the integration of OpenAI's powerful NLP capabilities into various projects. This MVP differentiates itself by focusing on simplicity and efficiency, making it ideal for developers of all skill levels.

## 📦 Features

|    | Feature            | Description                                                                                                        |
|----|--------------------|--------------------------------------------------------------------------------------------------------------------|
| ⚙️ | **Architecture**   | Utilizes a microservices architecture, with the API wrapper running as a standalone service. This provides flexibility and allows for independent scaling of components. |
| 📄 | **Documentation**  |  Provides detailed documentation, including API usage instructions, code examples, and tutorials. This streamlines onboarding and enables users to quickly learn and leverage the API. |
| 🔗 | **Dependencies**   | Leverages various libraries such as `fastapi`, `uvicorn`, `pydantic`, `openai`, `sqlalchemy`, `psycopg2-binary`, `alembic`, `pyjwt`, `requests`, `logging`, and `prometheus_client` for essential functionalities. |
| 🧩 | **Modularity**     |  The codebase is organized into modules for user management, API interaction, data validation, database interactions, and utility functions, promoting code reusability and maintainability. |
| 🧪 | **Testing**        | Includes a comprehensive testing framework, including unit tests, integration tests, and end-to-end tests. This ensures the quality, stability, and reliability of the codebase. |
| ⚡️  | **Performance**    |  Employs optimization techniques such as caching API responses, optimizing database queries, and asynchronous processing to ensure efficient operation. |
| 🔐 | **Security**       |  Implements security measures to protect user data and API keys, including secure storage of API keys, data encryption, and rate limiting. |
| 🔀 | **Version Control**|  Uses Git for version control and employs a Gitflow branching model for a structured and collaborative development process. |
| 🔌 | **Integrations**   | Integrates with popular cloud platforms like AWS or Azure for hosting the database and server infrastructure. |
| 📶 | **Scalability**    |  Designed for scalability, leveraging cloud-based solutions for automatic scaling and resource management. |

## 📂 Structure

```text
openai-api-client/
├── api
│   ├── routes
│   │   ├── user.py
│   │   └── openai.py
│   └── schemas
│       ├── user.py
│       └── openai.py
├── dependencies
│   ├── auth.py
│   ├── database.py
│   ├── openai.py
│   └── utils.py
├── models
│   ├── base.py
│   ├── user.py
│   └── api_usage.py
├── services
│   ├── user.py
│   └── openai.py
├── startup.sh
├── commands.json
├── tests
│   ├── conftest.py
│   ├── unit
│   │   ├── test_openai.py
│   │   └── test_user.py
│   └── integration
│       ├── test_openai_routes.py
│       └── test_user_routes.py
├── migrations
│   └── versions
│       └── ...
│           └── ...
│               └── alembic_version.py
├── README.md
├── .env.example
├── .env
├── gunicorn.conf.py
├── Procfile
├── .gitignore
└── .flake8
```

## 💻 Installation

### 🔧 Prerequisites

- Python 3.9 or higher
- PostgreSQL 14+
- `pip` (Python package manager)
- `alembic` (Database migration tool)

### 🚀 Setup Instructions

1. **Clone the repository:**

   ```bash
   git clone https://github.com/coslynx/OpenAI-API-Python-Client.git
   cd OpenAI-API-Python-Client
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up the database:**

   -  Create a PostgreSQL database and user if you don't already have one.
   -  Update the `DATABASE_URL` in your `.env` file with your database connection string.
   -  Run database migrations:

     ```bash
     alembic upgrade head
     ```

4. **Configure environment variables:**

   -  Create a `.env` file based on the `.env.example` file.
   -  Replace placeholder values with your actual API keys and database credentials.

## 🏗️ Usage

### 🏃‍♂️ Running the MVP

1. **Start the application server:**

   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

### ⚙️ Configuration

-  **`.env` file:** Contains environment variables like `OPENAI_API_KEY`, `DATABASE_URL`, and `SECRET_KEY`. 
-  **`gunicorn.conf.py`:**  Configures the `gunicorn` web server for deployment.

### 📚 Examples

**User Registration:**

```bash
curl -X POST http://localhost:8000/api/v1/users/register \
     -H "Content-Type: application/json" \
     -d '{"username": "your_username", "email": "your_email@example.com", "password": "your_password"}'
```

**User Login:**

```bash
curl -X POST http://localhost:8000/api/v1/users/login \
     -H "Content-Type: application/json" \
     -d '{"email": "your_email@example.com", "password": "your_password"}'
```

**Text Completion:**

```bash
curl -X POST http://localhost:8000/api/v1/openai/complete \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer your_access_token" \
     -d '{"text": "The quick brown fox jumps over the", "model": "text-davinci-003", "temperature": 0.7, "max_tokens": 256}'
```

## 🌐 Hosting

### 🚀 Deployment Instructions

**Deploying to Heroku:**

1. **Install the Heroku CLI:**

   ```bash
   pip install -g heroku
   ```

2. **Log in to Heroku:**

   ```bash
   heroku login
   ```

3. **Create a new Heroku app:**

   ```bash
   heroku create openai-api-python-client-production
   ```

4. **Set up environment variables:**

   ```bash
   heroku config:set OPENAI_API_KEY=your_openai_api_key
   heroku config:set DATABASE_URL=your_database_url
   heroku config:set SECRET_KEY=your_secret_key
   ```

5. **Deploy the code:**

   ```bash
   git push heroku main
   ```

6. **Run database migrations:**

   ```bash
   heroku run alembic upgrade head
   ```

### 🔑 Environment Variables

-  `OPENAI_API_KEY`: Your OpenAI API key.
-  `DATABASE_URL`: Your PostgreSQL database connection string.
-  `SECRET_KEY`: A secret key for JWT authentication.

## 📜 API Documentation

### 🔍 Endpoints

- **POST `/api/v1/users/register`:** Register a new user.
    - **Request Body:**

        ```json
        {
          "username": "your_username",
          "email": "your_email@example.com",
          "password": "your_password"
        }
        ```

    - **Response Body:**

        ```json
        {
          "id": 1,
          "username": "your_username",
          "email": "your_email@example.com",
          "api_key": "your_api_key"
        }
        ```

- **POST `/api/v1/users/login`:** Login an existing user and obtain an access token.
    - **Request Body:**

        ```json
        {
          "email": "your_email@example.com",
          "password": "your_password"
        }
        ```

    - **Response Body:**

        ```json
        {
          "access_token": "your_access_token",
          "token_type": "bearer"
        }
        ```

- **GET `/api/v1/users/me`:** Get the current user's information.
    - **Authorization:** Bearer your_access_token
    - **Response Body:**

        ```json
        {
          "id": 1,
          "username": "your_username",
          "email": "your_email@example.com",
          "api_key": "your_api_key"
        }
        ```

- **POST `/api/v1/openai/complete`:** Complete a given text using OpenAI's text completion API.
    - **Authorization:** Bearer your_access_token
    - **Request Body:**

        ```json
        {
          "text": "The quick brown fox jumps over the",
          "model": "text-davinci-003",
          "temperature": 0.7,
          "max_tokens": 256
        }
        ```

    - **Response Body:**

        ```json
        {
          "response": "lazy dog."
        }
        ```

- **POST `/api/v1/openai/translate`:** Translate a given text using OpenAI's translation API.
    - **Authorization:** Bearer your_access_token
    - **Request Body:**

        ```json
        {
          "text": "Hello world",
          "source_language": "en",
          "target_language": "fr"
        }
        ```

    - **Response Body:**

        ```json
        {
          "response": "Bonjour le monde"
        }
        ```

- **POST `/api/v1/openai/summarize`:** Summarize a given text using OpenAI's summarization API.
    - **Authorization:** Bearer your_access_token
    - **Request Body:**

        ```json
        {
          "text": "The quick brown fox jumps over the lazy dog.",
          "model": "text-davinci-003"
        }
        ```

    - **Response Body:**

        ```json
        {
          "response": "A brown fox jumps over a lazy dog."
        }
        ```

### 🔒 Authentication

-  Register a new user or login to receive a JWT access token.
-  Include the access token in the `Authorization` header for all protected routes using the format: `Authorization: Bearer your_access_token`

## 📜 License & Attribution

### 📄 License

This Minimum Viable Product (MVP) is licensed under the [GNU AGPLv3](https://choosealicense.com/licenses/agpl-3.0/) license.

### 🤖 AI-Generated MVP

This MVP was entirely generated using artificial intelligence through [CosLynx.com](https://coslynx.com).

No human was directly involved in the coding process of the repository: OpenAI-API-Python-Client

### 📞 Contact

For any questions or concerns regarding this AI-generated MVP, please contact CosLynx at:
- Website: [CosLynx.com](https://coslynx.com)
- Twitter: [@CosLynxAI](https://x.com/CosLynxAI)

<p align="center">
  <h1 align="center">🌐 CosLynx.com</h1>
</p>
<p align="center">
  <em>Create Your Custom MVP in Minutes With CosLynxAI!</em>
</p>
<div class="badges" align="center">
  <img src="https://img.shields.io/badge/Developers-Drix10,_Kais_Radwan-red" alt="">
  <img src="https://img.shields.io/badge/Website-CosLynx.com-blue" alt="">
  <img src="https://img.shields.io/badge/Backed_by-Google,_Microsoft_&_Amazon_for_Startups-red" alt="">
  <img src="https://img.shields.io/badge/Finalist-Backdrop_Build_v4,_v6-black" alt="">
</div>