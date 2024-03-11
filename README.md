# FastApi_DockerCompose

## Project Overview

This is a FastAPI project that utilizes Docker Compose for seamless deployment. The project follows a structured approach centered around the concept of "projects". Each project is characterized by a name, description, status, and an associated PDF file. The project leverages PostgreSQL as its database and Docker Compose to efficiently manage services, including volumes for storing the PDF files.

## Reqiuirement
[Docker](https://www.docker.com/products/docker-desktop/) needs to be installed

## Project Structure

- `main.py`: This is the main entry point of the application. It defines the FastAPI app and all the endpoints.
- `crud.py`: This file contains the CRUD operations for the "projects".
- `database.py`: This file sets up the database connection.
- `models.py`: This file defines the SQLAlchemy models.
- `schemas.py`: This file defines the Pydantic models.

## Endpoints

- `POST /projects/`: Create a new project. The name, description, status, and PDF file are sent as form data.
- `GET /projects/`: Get a list of all projects.
- `GET /projects/{project_id}`: Get the details of a specific project.
- `GET /projects/{project_id}/pdf`: Download the PDF file of a specific project.
- `PUT /projects/{project_id}`: Update the details of a specific project. The name, description, status, and PDF file can be updated.
- `DELETE /projects/{project_id}`: Delete a specific project.

## Running the Project
Before running the project, you need to set up the following environment variables:

- `DB_USERNAME`: The username of the database.
- `DB_PASSWORD`: The password of the database.


To run the project, use Docker Compose:

```
docker-compose up
```
Then fast api swagger ui can be accessed at ```localhost:8000/docs```


