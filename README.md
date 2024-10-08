
# FastAPI Application

This is a FastAPI application designed to manage posts and users. The application uses SQLAlchemy for ORM, Pydantic for data validation, and JWT for authentication.

## Table of Contents
- [Installation](#installation)
- [Configuration](#configuration)
- [Database Migration](#database-migration)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/atabakhooshangi/lucid.git
cd lucid
```

### 2. Create and Activate a Virtual Environment


```bash
poetry config virtualenvs.in-project true  # this will make poetry add the env folder to the directory of your toml file.
poetry install
poetry shell
```


## Configuration

### 1. Environment Variables

Create a `.env` file in the root directory of the project by copying the sample environment file.

```bash
cp sample.env .env
```

### 2. Update the `.env` File

Open the `.env` file and update the values as needed. Ensure the following variables are set correctly:

```env
MYSQL_SERVER=your_mysql_server
MYSQL_PORT=your_mysql_port
MYSQL_DB=your_mysql_db
MYSQL_USER=your_mysql_user
MYSQL_PASSWORD=your_mysql_password
USER_RSA_PRIVATE_KEY=your_rsa_private_key
USER_RSA_PUBLIC_KEY=your_rsa_public_key
BACKEND_CORS_ORIGINS=your_cors_origins
SERVER_HOST=your_server_host
SERVER_PORT=your_server_port
RELOAD=your_reload_setting
PAYLOAD_MAX_SIZE=your_payload_max_size
CACHE_TIME=your_cache_time
USER_RSA_PRIVATE_KEY=your_keys
USER_RSA_PUBLIC_KEY=your_keys
```

## Database Migration

### 1. Initialize the Database

Run the following command to create the database tables:

```bash
cd src
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

## Running the Application

### 1. Start the Application

Use the following command to start the FastAPI application:

```bash
python main.py
```

### 2. Access the Application

Open your browser and navigate to `http://{your-host}:{your-port}` to access the application.

### 3. API Documentation

You can access the automatically generated API documentation by navigating to `http://{your-host}:{your-port}/docs`.

## Additional Information

### Project Structure

```
src/
├── api/
│   ├── api_router.py
│   ├── deps.py
│   └── endpoints/
│       ├── post.py
│       └── user.py
├── config/
│   ├── settings.py
├── crud/
│   ├── base.py
│   ├── crud_post.py
│   └── crud_user.py
├── db/
│   ├── session.py
├── exceptions/
│   ├── base_exception.py
│   ├── exception_result.py
│   └── post_exception.py
│   └── user_exception.py
├── extras/
│   ├── response_model.py
│   └── security.py
├── models/
│   ├── base.py
│   ├── post.py
│   └── user.py
├── schemas/
│   ├── base.py
│   ├── post.py
│   └── user.py
└── main.py
```

## Contributing

Feel free to open issues or submit pull requests for improvements or bug fixes.

## License

This project is licensed under the MIT License.
