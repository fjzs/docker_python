# OptOps: python web application for an optimization problem
The purpose of this project is to practice OptOps, particularly CI/CD, and to create a simple web application that solves an optimization problem. 
The application is built using:
- FastAPI: a modern, fast (high-performance) web framework for building APIs with Python.
- Docker: a platform for developing, shipping, and running applications in containers, which allows for consistent environments across development and production.
- Render: a cloud platform that provides hosting for web applications, databases, and other services, making it easy to deploy and manage applications in the cloud.
- GitHub Actions: a CI/CD platform that allows you to automate your build, test, and deployment pipeline directly from your GitHub repository.

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

# End points
- List here the end points of the app

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

# Continuous Integration and Deployment (CI/CD)
This project uses GitHub Actions for continuous integration and deployment.
- All docker images are published here: `https://github.com/fjzs/docker_python/pkgs/container/optimization-api`
