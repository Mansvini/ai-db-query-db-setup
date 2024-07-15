# Database Repository

## Table of Contents
1. [Overview](#overview)
2. [Database Schema](#database-schema)
   - [Events Table](#events-table)
   - [Companies Table](#companies-table)
   - [People Table](#people-table)
3. [Installation](#installation)
   - [Prerequisites](#prerequisites)
   - [Steps](#steps)
4. [Challenges](#challenges)
5. [Improvements](#improvements)
6. [Conclusion](#conclusion)

## Overview

This repository contains the schema and scripts for creating and populating a PostgreSQL database to store information about events, companies, and people. The database schema is designed to facilitate easy querying and analysis of this data.

## Database Schema

### Events Table
| Column              | Type    | Description                                      |
|---------------------|---------|--------------------------------------------------|
| event_id            | SERIAL  | Primary key                                      |
| event_logo_url      | TEXT    | URL of the event logo                            |
| event_name          | TEXT    | Name of the event                                |
| event_start_date    | DATE    | Start date of the event                          |
| event_end_date      | DATE    | End date of the event                            |
| event_venue         | TEXT    | Venue of the event                               |
| event_country       | TEXT    | Country where the event is held                  |
| event_description   | TEXT    | Description of the event                         |
| event_url           | TEXT    | Unique URL of the event                          |
| event_industry      | TEXT    | Industry tags for the event                      |

### Companies Table
| Column                           | Type    | Description                                      |
|----------------------------------|---------|--------------------------------------------------|
| company_id                       | SERIAL  | Primary key                                      |
| company_name                     | TEXT    | Name of the company                              |
| company_phone                    | TEXT    | Phone number of the company                      |
| company_address                  | TEXT    | Address of the company                           |
| company_industry                 | TEXT    | Industry the company operates in                 |
| company_overview                 | TEXT    | Overview of the company                          |
| homepage_url                     | TEXT    | Homepage URL of the company                      |
| linkedin_company_url             | TEXT    | LinkedIn URL of the company                      |
| homepage_base_url                | TEXT    | Base URL of the company homepage                 |
| company_logo_url_on_event_page   | TEXT    | URL of the company logo on the event page        |
| company_logo_url                 | TEXT    | URL of the company logo                          |
| company_logo_match_flag          | TEXT    | Flag indicating if the logos match               |
| company_logo_text                | TEXT    | Text associated with the company logo            |
| relation_to_event                | TEXT    | Relation of the company to the event             |
| company_revenue                  | FLOAT   | Revenue of the company                           |
| min_employees                    | INT     | Minimum number of employees                      |
| max_employees                    | INT     | Maximum number of employees                      |
| company_founding_year            | INT     | Year the company was founded                     |
| event_url                        | TEXT    | Event URL, foreign key referencing Events table  |

### People Table
| Column                    | Type    | Description                                    |
|---------------------------|---------|------------------------------------------------|
| person_id                 | SERIAL  | Primary key                                    |
| first_name                | TEXT    | First name of the person                       |
| middle_name               | TEXT    | Middle name of the person                      |
| last_name                 | TEXT    | Last name of the person                        |
| job_title                 | TEXT    | Job title of the person                        |
| person_city               | TEXT    | City where the person is located               |
| person_state              | TEXT    | State where the person is located              |
| person_country            | TEXT    | Country where the person is located            |
| email_pattern             | TEXT    | Pattern used to generate the person's email    |
| email                     | TEXT    | Email address of the person                    |
| homepage_base_url         | TEXT    | Base URL of the person's homepage              |
| duration_in_current_job   | TEXT    | Duration the person has been in their current job |
| duration_in_current_company | TEXT | Duration the person has been with the company  |

## Installation

### Prerequisites

- Python 3.6 or later
- PostgreSQL
- pip

### Steps

1. **Clone the repository:**
   ```sh
   git clone https://github.com/Mansvini/ai-db-query-db-setup.git
   cd ai-db-query-db-setup
   ```

2. **Set up a Python virtual environment:**
   ```sh
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install the required Python packages:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Set up the PostgreSQL database:**

   a. **Install PostgreSQL (if not already installed):**
      - Follow the installation instructions for your operating system from the [PostgreSQL website](https://www.postgresql.org/download/).

   b. **Start PostgreSQL (if not already running)**

   b. **Create a new database and user:**
      ```sh
      sudo -u postgres psql
      ```

      In the PostgreSQL console, run the following commands:
      ```sql
      CREATE DATABASE mydatabase;
      CREATE USER myuser WITH PASSWORD 'mypassword';
      ALTER ROLE myuser SET client_encoding TO 'utf8';
      ALTER ROLE myuser SET default_transaction_isolation TO 'read committed';
      ALTER ROLE myuser SET timezone TO 'UTC';
      GRANT ALL PRIVILEGES ON DATABASE mydatabase TO myuser;
      \q
      ```

      OR
      Follow the instructions to create a database for your installer.

   c. **Update the `.env` file with your PostgreSQL database credentials:**
      ```ini
      DB_HOST=localhost
      DB_NAME=mydatabase
      DB_USER=myuser
      DB_PASSWORD=mypassword
      OPENAI_API_KEY=your_openai_api_key
      ```

5. **Run the schema creation script:**
   ```sh
   python setup_db.py
   ```

6. **Load the data into the database:**
   ```sh
   python load_data.py
   ```

## Challenges

1. **Various Console Bugs**:
   - Encountered data type incompatibility issues while loading data into PostgreSQL.

2. **Data Redundancy**:
   - Addressing redundant data entries and ensuring data normalization.

3. **Non-Unique `homepage_base_url`**:
   - Dealing with non-unique `homepage_base_url` values in the companies data.

4. **Unclean Data**:
   - Handling missing or incomplete data fields and standardizing formats.

5. **Adding Email Addresses**:
   - Generating email addresses based on patterns and available data.

6. **Adding Event Industries**:
   - Using OpenAI to tag events with relevant industries.

7. **Standardizing Column Data**:
   - Ensuring data is in a standardized format to facilitate SQL queries using `>` or `=`.

8. **Understanding Different Patterns of Data**:
   - Recognizing and standardizing various unclean data patterns.
   - Matching and linking data between different CSV files.

9. **Identifying Relationships Between Data**:
   - Establishing correct foreign key relationships and ensuring data integrity.

## Improvements to Database Design

If given more time to work on the database design, I would focus on several key areas to enhance the functionality, performance, and maintainability of the database. Here are some improvements that could be made:

1. **Further Normalization**:
   - Further normalize the schema to reduce redundancy, especially for repeating data.
   - **Industry Table**: Create a separate `Industry` table to store industry names and use foreign keys to link to the `Events` and `Companies` tables. This reduces redundancy and ensures consistency.
   - **Location Table**: Introduce a `Location` table to store unique locations (countries, states, cities) and reference this table in the `Events` and `People` tables.

2. **Enhanced Validation and Constraints**:
   - **Data Validation**: Implement more comprehensive validation and constraints to ensure data integrity (e.g., CHECK constraints for valid dates, revenue ranges).
   - **Unique Constraints**: Ensure unique constraints on columns like `email` and `homepage_base_url` to prevent duplicate entries.

3. **Indexing**:
   - **Performance Optimization**: Add indexes on frequently queried columns, such as `event_industry`, `company_name`, and `email`, to improve query performance.
   - **Composite Indexes**: Create composite indexes for queries that involve multiple columns, such as `(event_start_date, event_end_date)`.

4. **Enhanced Relationships and Foreign Keys**:
   - **Referential Integrity**: Ensure all foreign key constraints are in place.
   - **Relationship Tables**: Introduce many-to-many relationship tables, such as `EventCompanies` to link events with multiple companies.

5. **Data Enrichment and Standardization**:
   - **Geocoding**: Use geocoding to add latitude and longitude coordinates for event and company locations to facilitate spatial queries.
   - **Standardized Employee Ranges**: Define standardized ranges for employees to enable easier filtering and reporting.

6. **Logging**:
   - Implement logging mechanisms to capture query performance metrics and identify slow queries for optimization.

7. **Full-Text Search**: 
   - Implement full-text search capabilities for columns like `event_description` and `company_overview` to enable more powerful search functionality.

8. **ER Diagrams**: 
   - Create and maintain Entity-Relationship (ER) diagrams to visualize the database schema and relationships.

9. **Read Replicas**: 
   - Set up read replicas for the PostgreSQL database to handle read-heavy workloads and improve performance.

10. **Automation and Testing**:
   - Automate data cleaning and validation processes, and include thorough testing to handle edge cases and ensure robustness.

11. **Use LLM to optimise data columns**:
   - Standardize and enrich the `company_industry`, `duration_in_current_job`, `event_country` and `duration_in_current_company` columns for more accurate and efficient querying.

By implementing these improvements, the database would be better structured, more efficient, and easier to maintain, leading to better performance and scalability for future needs.

## Conclusion

This database schema and the accompanying scripts provide a solid foundation for managing event, company, and people data. With further refinements and enhancements, the database can become even more robust and efficient for large-scale data analysis and querying.
