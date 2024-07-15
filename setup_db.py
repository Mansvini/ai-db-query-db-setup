import psycopg
import os
from dotenv import load_dotenv

load_dotenv()

# Connect to PostgreSQL database
conn = psycopg.connect(
    host=os.getenv('DB_HOST'),
    dbname=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD')
)
cursor = conn.cursor()

# Create Events table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Events (
    event_id SERIAL PRIMARY KEY,
    event_logo_url TEXT,
    event_name TEXT,
    event_start_date DATE,
    event_end_date DATE,
    event_venue TEXT,
    event_country TEXT,
    event_description TEXT,
    event_url TEXT UNIQUE,
    event_industry TEXT
)
''')

# Create Companies table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Companies (
    company_id SERIAL PRIMARY KEY,
    company_name TEXT,
    company_phone TEXT,
    company_address TEXT,
    company_industry TEXT,
    company_overview TEXT,
    homepage_url TEXT,
    linkedin_company_url TEXT,
    homepage_base_url TEXT,
    company_logo_url_on_event_page TEXT,
    company_logo_url TEXT,
    company_logo_match_flag TEXT,
    company_logo_text TEXT,
    relation_to_event TEXT,
    company_revenue FLOAT,
    min_employees INT,
    max_employees INT,
    company_founding_year INT,
    event_url TEXT,
    FOREIGN KEY(event_url) REFERENCES Events(event_url)
)
''')

# Create People table
cursor.execute('''
CREATE TABLE IF NOT EXISTS People (
    person_id SERIAL PRIMARY KEY,
    first_name TEXT,
    middle_name TEXT,
    last_name TEXT,
    job_title TEXT,
    person_city TEXT,
    person_state TEXT,
    person_country TEXT,
    email_pattern TEXT,
    email TEXT,
    homepage_base_url TEXT,
    duration_in_current_job TEXT,
    duration_in_current_company TEXT
)
''')

# Commit and close connection
conn.commit()
cursor.close()
conn.close()