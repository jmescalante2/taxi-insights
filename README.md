# Running PostgreSQL and Apache Superset with Docker Compose

This guide will help you set up a data analysis environment with PostgreSQL as the database and Apache Superset as the analytics platform using Docker Compose.

## Prerequisites

- Docker and Docker Compose installed on your machine.

## Instructions

1. **Prepare Docker Compose File**: Ensure you have the `docker-compose.yml` file from this repository in your working directory.

2. **Launch Services**:
    - Open a terminal in the directory containing your `docker-compose.yml` file.
    - Run the following command to start all services:
      ```
      docker-compose up -d
      ```
    - This command will download the necessary Docker images, create containers, and start the services.

3. **Accessing Apache Superset**:
    - Once the services are up, you can access Apache Superset by navigating to `http://localhost:8088` in your web browser.
    - The first time you access Superset, you'll need to set up an admin account. Follow the on-screen instructions to complete the setup.

4. **Connecting Superset to PostgreSQL**:
    - In Superset, go to **Data > Databases > + DATABASE** and use the following SQLAlchemy URI to connect to the PostgreSQL database:
      ```
      postgresql+psycopg2://superset:superset@postgres/superset
      ```
    - Replace `superset:superset@postgres/superset` with your actual PostgreSQL credentials and hostname if different.

5. **Shutting Down**:
    - To stop and remove the containers, networks, and volumes associated with your Docker Compose setup, run:
      ```
      docker-compose down -v
      ```

## Customization

- You can modify the `docker-compose.yml` file to change service configurations, such as ports or volume paths.
- Ensure any changes in PostgreSQL credentials are reflected in both the `postgres` and `superset` service configurations.
