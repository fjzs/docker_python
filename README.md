# OptOps: python web application - solving the knapsack problem
This is a project that implements a web application to solve the knapsack problem using Python.
The purpose of this project is to practice OptOps.

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
6. Start the web application:
    ```
    python app/main.py
    ```
7. Open your web browser and navigate to `http://localhost:8000` to access

# End points
- List here the end points of the app

# Running the application with Docker
- Build the Docker image:
   ```
   docker build -t optimization-api .
   ```
- Run the Docker container:
   ```
   docker run -d -p 8000:8000 optimization-api
   ```
- Open your web browser and navigate to `http://localhost:8000` to access the application.

# Continuous Integration and Deployment (CI/CD)
This project uses GitHub Actions for continuous integration and deployment.
- All docker images are published here: `https://github.com/fjzs/docker_python/pkgs/container/optimization-api`
