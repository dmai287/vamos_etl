# VAMOS Data Processor

The VAMOS Data Processor is an ETL (Extract, Transform, Load) pipeline designed to merge multiple data sources into a single, cohesive dataset for the VAMOS Mobility App. Deployed on Heroku, this data processing tool powers the foundational data for VAMOS's analytical workflows, enabling streamlined Exploratory Data Analysis (EDA) and Machine Learning (ML) models.

## Purpose
The VAMOS Data Processor serves to:

- Standardize and merge diverse mobility, user engagement, and geolocation data.
- Clean and transform raw data to provide a unified, consistent dataset.
- Automate regular data updates by leveraging Heroku’s scalable cloud platform.

## Data Sources
The Data Processor integrates data from several sources, including:

- User Activity Logs: Tracks app interactions, session durations, and feature usage.
- Geolocation and Route Data: Includes GPS coordinates, routes, and transit stop locations.
- Transportation Mode Data: Covers usage metrics for public transit, cycling, walking, and carpooling.
- Demographic Data: Contains optional user demographics such as age, preferences, and locations.

## Processing Workflow
The VAMOS Data Processor follows these steps to transform and merge data:

1. Data Extraction:

- Extracts data from multiple sources, including CSV files, databases, and APIs.
- Leverages Heroku’s cloud capabilities for seamless, scheduled data extraction.

2. Data Cleaning:

- Removes duplicates, handles missing values, and standardizes data formats (e.g., timestamps, coordinate systems).
- Ensures consistent field formats for smooth data integration.

3. Data Transformation and Integration:

- Joins datasets using key identifiers (e.g., user ID, route ID) to create a consolidated view.
- Adds calculated fields (e.g., session duration, distance traveled) for enriched insights.
- Prepares data for compatibility with EDA and ML models.

4. Data Output:

- Produces a single, merged dataset in a structured format (e.g., Parquet, CSV) for downstream analysis.
- Deploys an automated schedule on Heroku to keep the dataset up-to-date.

## Deployment on Heroku
Deployed on Heroku, the VAMOS Data Processor benefits from:

- Automated Task Scheduling: Uses Heroku Scheduler to refresh and update data at regular intervals, ensuring analysis reflects current app usage and mobility trends.
- Scalability: Easily adapts to the increasing data volume as VAMOS expands its user base and data sources.
- Cost-Effective Cloud Solution: Heroku's cloud infrastructure offers a lightweight, scalable environment, optimized for handling ETL tasks and integrating with the VAMOS app’s ecosystem.

## Key Features
- Consistent Data Quality: Merges data from various sources into a standardized format for accuracy and reliability in analysis.
- Automated Refreshes: Ensures timely data updates via Heroku Scheduler, so the latest trends and metrics are always available.
Scalable Infrastructure: Supports growing data needs, with Heroku providing flexibility and ease of maintenance.
