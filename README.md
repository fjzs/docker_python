# A web application for an optimization service using OptOps (DevOps + Operations Research) strategies.

[![Unit Tests](https://github.com/fjzs/docker_python/actions/workflows/ci.yml/badge.svg)](https://github.com/fjzs/docker_python/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)
![Solver](https://img.shields.io/badge/Solver-MIP%20Enabled-success)
![Last Image Published](https://img.shields.io/github/last-commit/fjzs/docker_python)

The purpose of this project is to implement an end-to-end optimization service using OptOps (DevOps + OR) with software engineering best practices.

## Technologies used:
- FastAPI: a modern, fast (high-performance) web framework for building APIs with Python.
- Docker: a platform for developing, shipping, and running applications in containers, which allows for consistent environments across development and production.
- GitHub Actions: a CI/CD technology that allows you to automate your build, test, and deployment pipeline directly from your GitHub repository.
- Render: a cloud platform that provides hosting for web applications, databases, and other services, making it easy to deploy and manage applications in the cloud.

## Software development approach:
- Test-Driven Development (TDD): a software development process where you write tests before writing the actual code. This approach helps ensure that the code is well-designed, maintainable, and meets the requirements.
- Software Design Principles: I followed basic principles like SOLID and DRY, but also incorporated the philosophy within the book `A Philosophy of Software Design` by 
  John Ousterhout, which emphasizes simplicity and modularity in software design. (https://www.amazon.com/Philosophy-Software-Design-2nd/dp/173210221X).
- Software Architecture: I used an MVC design pattern to separate the concerns of the application, making it easier to maintain and extend in the future.
- I used agentic development to accelerate the development process, leveraging the capabilities of AI agents like Copilot and Claude to assist with code generation, refactoring, and testing.
- I used a file to provide context to the agent (testing best practices, software design principles and more).

# Installation instructions
1. Clone the repository:
   ```
   git clone
    ```
2. Navigate to the project directory.
3. Create a virtual environment with python 3.11 and activate it:
   ```
   python3.11 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install the required dependencies:
    ```
    pip install -r requirements.txt
    ```
5. Run the tests:
    ```
    pytest
    ```
6. Start the web application locally (this method will reload the app on any code changes):
    ```
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    ```
7. Open your web browser and navigate to `http://localhost:8000` to access the application.

# Running the application with Docker (locally)
1. Build the Docker image (or skip this step if your image is already built locally):
   ```
   docker build -t optimization-api .
   ```
2. Run the Docker container:
   ```
   docker run -d -p 8000:8000 optimization-api
   ```
3. Open your web browser and navigate to `http://localhost:8000` to access the application.

# Continuous Integration (CI)
This project uses GitHub Actions for continuous integration. It has a workflow that runs on every push, and it includes the following high-level steps:
1. **Checkout code**: The workflow checks out the code from the repository.
2. **Build Docker image**: It builds the Docker image for the application.
3. **Run tests**: It runs all the tests (unit and integration) directly from the image to ensure that the application works as expected.
4. **Publish Docker image**: If the tests pass, the workflow publishes the Docker image to a predefined container registry. In particular, this is https://github.com/fjzs/docker_python/pkgs/container/optimization-api.
5. **Tagging**: The workflow finally tags the recently uploaded image as the `latest`.

# Continuous Deployment (CD)
- This project uses Render as the hosting platform for the application. Currently, from the Render site I manually trigger the deployment of the latest image published.
- From the Render dashboard I can see the logs of the application.
- Other observability tools could be added, but as of now those are out of scope for this project.

# Using the web application
The web application can be accessed (give it ~10 seconds to Render to lift the app) on this URL: https://franciscooptimizationapi.onrender.com/