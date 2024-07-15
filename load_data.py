import psycopg
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
import os
import re

load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Connect to PostgreSQL database
conn = psycopg.connect(
    host=os.getenv('DB_HOST'),
    dbname=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD')
)
cursor = conn.cursor()

# Load CSV files
people_info = pd.read_csv('./data/people_info.csv')
event_info = pd.read_csv('./data/events_info.csv')
company_info = pd.read_csv('./data/company_info.csv')

# Ensure date columns are correctly formatted
event_info['event_start_date'] = pd.to_datetime(event_info['event_start_date']).dt.date
event_info['event_end_date'] = pd.to_datetime(event_info['event_end_date']).dt.date

# # Replace empty strings with None
people_info.replace('', None, inplace=True)
event_info.replace('', None, inplace=True)
company_info.replace('', None, inplace=True)

# Drop duplicate rows
people_info.drop_duplicates(inplace=True)
event_info.drop_duplicates(inplace=True)
company_info.drop_duplicates(inplace=True)

# Function to generate email based on the pattern
def generate_email(row):
    if pd.isnull(row['email_pattern']):
        return None
    
    first_name = row['first_name'].lower() if pd.notnull(row['first_name']) else ''
    last_name = row['last_name'].lower() if pd.notnull(row['last_name']) else ''
    first_initial = first_name[0] if first_name else ''
    last_initial = last_name[0] if last_name else ''
    domain = row['homepage_base_url']
    
    email = row['email_pattern']
    email = email.replace('[first]', first_name)
    email = email.replace('[last]', last_name)
    email = email.replace('[first_initial]', first_initial)
    email = email.replace('[last_initial]', last_initial)
    email += f"@{domain}"

    return email


# Apply the email generation function to people_info
people_info['email'] = people_info.apply(generate_email, axis=1)

# Define potential industries
industries = [
    "Oil & Gas", "Technology", "Finance", "Pharmaceuticals", "Retail", "Automotive",
    "Healthcare", "Education", "Manufacturing", "Real Estate", "Energy", "Telecommunications"
]

# Function to tag event with industries using OpenAI
def tag_event_industry(event_name, event_description):
    prompt = (
        f"Tag the following event with appropriate industries from this list: {industries}. "
        f"Event name: {event_name}. Event description: {event_description}. "
        "Include any other relevant industries as you see fit. Provide only industry tags as output, separated by commas, and no other words."
    )
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an expert in categorizing events based on their descriptions."},
            {"role": "user", "content": prompt}
        ],
    )
    industry_list = response.choices[0].message.content.strip().strip('.')
    return industry_list

# Tag each event with industries
event_info['event_industry'] = event_info.apply(
    lambda row: tag_event_industry(row['event_name'], row['event_description']),
    axis=1
)

# Function to standardize company revenue
def standardize_revenue(revenue):
    if pd.isnull(revenue):
        return None
    
    revenue = str(revenue).lower().replace('$', '').replace(',', '').strip()
    
    if 'billion' in revenue:
        return float(re.findall(r'\d*\.?\d+', revenue)[0]) * 1e9
    elif 'million' in revenue:
        return float(re.findall(r'\d*\.?\d+', revenue)[0]) * 1e6
    elif 'thousand' in revenue:
        return float(re.findall(r'\d*\.?\d+', revenue)[0]) * 1e3
    else:
        return float(re.findall(r'\d*\.?\d+', revenue)[0])

# Apply the revenue standardization function to company_info
company_info['company_revenue'] = company_info['company_revenue'].apply(standardize_revenue)

# Function to standardize number of employees
def standardize_employees(employees):
    if pd.isnull(employees):
        return None, None
    
    employees = str(employees).lower().replace(',', '').strip()
    
    try:
        if '0-1' in employees:
            return 0, 1
        elif '1-10' in employees: 
            return 1, 10
        elif '2-10' in employees:
            return 2, 10
        elif '11-50' in employees:
            return 11, 50
        elif '51-200' in employees:
            return 51, 200
        elif '201-500' in employees:
            return 201, 500
        elif '501-1000' in employees:
            return 501, 1000
        elif '1001-5000' in employees:
            return 1001, 5000
        elif '5001-10000' in employees:
            return 5001, 10000
        elif '10001+' in employees:
            return 10001, None
        else:
            numbers = [float(num) for num in re.findall(r'\d+\.\d+|\d+', employees)]
            numbers = [int(num) for num in numbers if num.is_integer()]
            if len(numbers) == 2:
                return numbers[0], numbers[1]
            elif len(numbers) == 1:
                return numbers[0], numbers[0]
            else:
                return None, None
    except (IndexError, ValueError) as e:
        print(f"Error processing employees: {employees}, error: {e}")
        return None, None

# Apply the employees standardization function to company_info
company_info[['min_employees', 'max_employees']] = company_info['n_employees'].apply(
    lambda x: pd.Series(standardize_employees(x))
)

# Remove the n_employees column as it is no longer needed
company_info.drop(columns=['n_employees'], inplace=True)

# Function to insert data into PostgreSQL
def insert_data(df, table_name):
    for index, row in df.iterrows():
        cols = ', '.join(list(row.index))
        vals = ', '.join(["%s"] * len(row))
        sql = f"INSERT INTO {table_name} ({cols}) VALUES ({vals})"
        try:
            cursor.execute(sql, tuple(None if pd.isna(v) else v for v in row))
        except Exception as e:
            print(f"Error inserting data into {table_name}: {e}")

# Insert data into Events table
insert_data(event_info, 'Events')

# Insert data into Companies table
insert_data(company_info, 'Companies')

# Insert data into People table
insert_data(people_info, 'People')

# Commit and close connection
conn.commit()
cursor.close()
conn.close()