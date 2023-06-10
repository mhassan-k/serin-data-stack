# Modern data tech stack 
with Postgres, DBT, and Airflow

Provide an overview of the project, its purpose, and any relevant background information.

<!-- GETTING STARTED -->
## Getting Started


### Prerequisites

Make sure you have docker installed on local machine.
* Docker
* DockerCompose
  
### Files Usage

- `requirements.txt`: a text file lsiting the projet's dependancies.
- `README.md`: Markdown text with a brief explanation of the project and the repository structure.
- `Dockerfile`: build users can create an automated build that executes several command-line instructions in a container.
- `docker-compose.yaml`: Integrates the various docker containers and run them in a single environment.

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/mhassan-k/serin-data-stack
   ```
2. browse airflow folder 
    ```sh
    docker-compose build
    docker-compose up
   ```
3. Run
   ```sh
    docker-compose build
    docker-compose up
   ```
4. Open Airflow web browser
   ```JS
   Navigate to `http://localhost:8000/` on the browser
   activate and trigger dbt_dag
   activate and trigger migrate
    ```

# Troubleshooting
Provide troubleshooting tips or solutions to common problems that users may encounter.

# Changelog
Document the version history of the project, along with the changes, additions, and fixes implemented in each version.


# Conclusion
Wrap up the README with any final thoughts, instructions, or calls to action.

