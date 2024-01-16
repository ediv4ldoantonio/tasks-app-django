# Tasks API

This project is a Tasks API built with Django Rest Framework (DRF), providing a robust and secure platform for managing tasks and to-do lists. The API is designed to handle CRUD (Create, Read, Update, Delete) operations on tasks, ensuring efficient task management.

## Table of Contents
- [Key Features](#key-features)
- [Tools & Services](#tools--services)
- [Running In a Virtual Env](#running-in-a-virtual-env)
- [Run Tests](#run-tests)
- [Access Docs](#access-docs)
- [License](#license)

## Key Features

### Authentication:

The API is equipped with authentication mechanisms to ensure secure access.
Users are required to authenticate using a token-based authentication system, safeguarding the API from unauthorized access.

### Task Operations:

- **Create:** Users can add new tasks to their to-do list.
- **Read:** Retrieve a list of tasks, as well as individual task details.
- **Update:** Modify existing tasks, allowing users to update task descriptions, due dates, or status.
- **Delete:** Remove tasks that are no longer needed.

### User Management:

Users can register and create accounts to personalize their to-do lists.
Account details and authentication tokens are securely managed.

## Tools & Services
- Django & DRF: for building the APIs
- MySQL: Relational DB

## Running In a Virtual Env
1. Create a virtual environment using:

    ```
    mkvirtualenv <env_name>
    ```

2. Ensure you have installed `virtualenv` on your system and install dev dependencies using:

    ```
    pip install -r app/requirements/dev.txt
    ```

3. Navigate to the app directory and run migrations:

    ```
    python manage.py makemigrations

    python manage.py migrate
    ```

4. Run the server:

    ```
    python manage.py runserver
    ```

## Run Tests
Navigate to the app directory and run descriptive tests using:

```
pytest -rP -vv
```


## Access Docs
Access the API documentation at:

```
http://localhost:8000/api/v1/doc
```


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
