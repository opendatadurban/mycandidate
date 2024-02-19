import csv
import json
from . import *  # noqa
from ...app import app
import pandas as pd
import os

CHUNK_SIZE = 3500
records = []

def seed_site_settings(db, excel_file_path):
    xls = pd.ExcelFile(f'{excel_file_path}')
    df = pd.read_excel(xls, 'site_settings')
    for index, row in df[df['title'].notna()].iterrows():
        if row["title"]:
            # Check if it exists
            instance = db.session.query(Config).filter(
                                Config.title == row["title"]).filter(
                                    Config.navbar_logo == row["navbar_logo"]
                                ).first()

            # Flag to track if a matching province is found in records
            found_matching_config = False
            
            # Check if it exists in queryset
            if instance is not None:
                found_matching_config = True
                print("existing")
                break

            if not found_matching_config:
                config = Config(
                    title=row["title"],
                    title_short=row["title_short"],
                    navbar_logo=row["navbar_logo"],
                    favicon_logo=row["favicon_link"],
                    primary_color=row["primary_colour"],
                    secondary_color=row["secondary_colour"],
                    data_schemas=row["data_schemas"],
                    partner_name=row["partner_name"] if row["partner_name"] else None,
                    partner_website=row["partner_website"] if row["partner_website"] else None,	
                    google_analytics_key=row["google_analytics_key"] if row["google_analytics_key"] else None,	
                    gtag_script=row["gTag_script"] if row["gTag_script"] else None
                )
            
                # Dynamically handle additional columns
                for column in df.columns:
                    if column not in ["title", "title_short", "navbar_logo", "favicon_link", "primary_colour", "secondary_colour"]:
                        setattr(config, column, row[column])
                        # print(column, row[column])
                db.session.add(config)
    try:
        db.session.commit()
    except Exception as e:
        print(e)    


def seed_data_tables(db, excel_file_path):
    xls = pd.ExcelFile(f'{excel_file_path}')
    df = pd.read_excel(xls, 'site_settings')
    for index, row in df[df['title'].notna()].iterrows():
        if row["title"]:
            # Check if it exists
            instance = db.session.query(Config).filter(
                                Config.title == row["title"]).filter(
                                    Config.navbar_logo == row["navbar_logo"]
                                ).first()
            
            data_schemas = json.loads(instance.data_schemas)
            print(data_schemas)
            for table_name, csv_filename in data_schemas.items():
                print("Table: ", table_name)
                file_root = f'{app.root_path}/data/{csv_filename}'
                csv_df = pd.read_csv(file_root, quotechar='"')
                
                cleaned_columns = [col.replace(' ', '_') for col in csv_df.columns]

                # Generate the CREATE TABLE query
                create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join([col + ' TEXT' for col in cleaned_columns])})"
                db.session.execute(create_table_query)
                
                # Insert data into the created table
                for _, row_data in csv_df.iterrows():
                    row_data_adjusted = {col.replace(' ', '_'): val for col, val in row_data.to_dict().items()}
                    insert_query = f"INSERT INTO {table_name} VALUES ({', '.join([':' + col.replace(' ', '_') for col in cleaned_columns])})"

                    # print(row_data_adjusted)
                    db.session.execute(insert_query, row_data_adjusted)
    try:
        db.session.commit()
        print("Session commit to db")
    except Exception as e:
        db.session.rollback()
        print("DB exception: ", e)
        raise
    finally:
        db.session.close()


"""
County Code,County Name,Constituency Code,Constituency Name,Surname,Other Names,Party Code,Political Party Name,Abbrv - national_assembly
Surname,Other Names,County Code,County Name,Constituency Code,Constituency Name,Ward Code,Ward Name,Party Code,Political Party Name,Abbrv - ward
County Code,County Name,Surname,Other Names,Party Code,Political Party Name,Abbrv - senate
County Code,County Name,Surname,Other Names,Party Code,Political Party Name,Abbrv - county_govenor
County Code,County Name,Surname,Other Names,Party Code,Political Party Name,Abbrv - women

{
"ward": "county_code",
"county_name": "county_code",
"senate": "county_code",
"national_assembly": "county_code",
"county_govenor": "county_code"
}
"""

def seed_data_candidates(db, excel_file_path):
    xls = pd.ExcelFile(f'{excel_file_path}')
    df = pd.read_excel(xls, 'site_settings')
    records = []
    
    for index, row in df[df['title'].notna()].iterrows():
        if row["title"]:
            # Check if it exists
            instance = db.session.query(Config).filter(
                Config.title == row["title"]).filter(
                Config.navbar_logo == row["navbar_logo"]
            ).first()

            data_schemas = json.loads(row["data_schemas"])
            print(data_schemas)
            for table_name, csv_filename in data_schemas.items():
                print("Table: ", table_name)
                # Dictionary to map table names to candidate types
                table_to_candidate_type = {
                    table_name: table_name,
                    table_name: table_name,
                    table_name: table_name,
                    table_name: table_name,
                    table_name: table_name
                }
                file_root = f'{app.root_path}/data/{csv_filename}'
                csv_df = pd.read_csv(file_root, quotechar='"')

                cleaned_columns = [col.replace(' ', '_') for col in csv_df.columns]

                # Insert data into the created table
                for _, row_data in csv_df.iterrows():
                    row_data_adjusted = {col.replace(' ', '_'): val for col, val in row_data.to_dict().items()}
                    row_data_adjusted['candidate_type'] = table_to_candidate_type.get(table_name, 'unknown')

                    record_dict = {f"{table_name}-{col}": f"EXCLUDED.{col}" for col in row_data_adjusted.keys() if col in cleaned_columns}
                    records.append(record_dict)
                    # Generate the INSERT INTO candidates query with ON CONFLICT clause
                    # insert_query = f"""
                    #     INSERT INTO candidates ({', '.join(row_data_adjusted.keys())})
                    #     VALUES ({', '.join([':' + col for col in row_data_adjusted.keys()])})
                    #     ON CONFLICT (Surname, Other_Names) DO UPDATE SET 
                    #         {', '.join([f"{col} = EXCLUDED.{col}" for col in row_data_adjusted.keys() if col not in ['Surname', 'Other_Names']])};
                    # """

                    # Generate the INSERT INTO candidates query with duplicates
                    # insert_query = f"""
                    #         INSERT INTO candidates ({', '.join(row_data_adjusted.keys())}) 
                    #         VALUES ({', '.join([':' + col for col in row_data_adjusted.keys()])})
                    #         """
                    # db.session.execute(insert_query, row_data_adjusted)

    try:
        db.session.commit()
        with open('extract.json', 'w') as file:
            json.dump(records, file)
        print("Session commit to db")
    except Exception as e:
        db.session.rollback()
        print("DB exception: ", e)
        raise
    finally:
        db.session.close()
