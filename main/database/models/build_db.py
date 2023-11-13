from . import *  # noqa
from ...app import app
import pandas as pd
CHUNK_SIZE = 3500
records = []

def seed_temp_indicators(db, excel_file_path):
    xls = pd.ExcelFile(f'{excel_file_path}')
    df = pd.read_excel(xls, 'Local')
    for index, row in df.iterrows():
        if row["Name"]:
            candidate = Candidate()
            name = row["Name"]
            candidate.name = name
            candidate.province = row["Province"]
            candidate.sex = row["Sex"]
            candidate.party = row["Party"]
            candidate.constituency = row["Constituency"]
            

            # Dynamically handle additional columns
            for column in df.columns:
                if column not in ["Name", "Province", "Constituency", "Party", "Sex"]:
                    setattr(candidate, column, row[column])
            records.append(candidate)

            if len(records) > CHUNK_SIZE:
                db.session.bulk_save_objects(records)
                db.session.commit()
                records.clear()
                print("Bulk Save")

    # Commit any remaining records
    if records:
        try:
            db.session.bulk_save_objects(records)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print("DB exception: ", e)
            raise


def seed_site_settings(db, excel_file_path):
    xls = pd.ExcelFile(f'{excel_file_path}')
    df = pd.read_excel(xls, 'site_settings')
    for index, row in df.iterrows():
        if row["title"]:
            config = Config()
            config.title = row["title"]
            config.title_short = row["title_short"]
            config.navbar_logo = row["navbar_logo"]
            config.favicon_logo = row["favicon_link"]
            config.primary_color = row["primary_colour"]
            config.secondary_color = row["secondary_colour"]
            
            # Dynamically handle additional columns
            for column in df.columns:
                if column not in ["title", "title_short", "navbar_logo", "favicon_link", "primary_color", "secondary_color"]:
                    setattr(config, column, row[column])

            db.session.add(config)
    try:
        db.session.commit()
    except Exception as e:
        print(e)    


# def seed_candidates_prov(db):
#     xls = pd.ExcelFile(f'{app.root_path}/data/Analysis Nomination Court Results.xlsx')
#     df = pd.read_excel(xls, 'Provincial')
#     for index, row in df.iterrows():
#         if row["NAME"]:
#             candidate = WardCandidate()
#             name = row["NAME"]
#             candidate.name = name
#             candidate.province = row["PROVINCE"]
#             candidate.ward_no = row["WARD"]
#             candidate.status = row["STATUS"]
#             candidate.sex = row["GENDER"]
#             candidate.party = row["PARTY"]
#             candidate.local_authority = row["LOCAL AUTHORITY"]
#             records.append(candidate)
#             if len(records) > CHUNK_SIZE:
#                 db.session.bulk_save_objects(records)
#                 db.session.commit()
#                 records.clear()
#                 print(F"Bulk Save")
#     try:
#         db.session.bulk_save_objects(records)
#         db.session.commit()
#     except Exception as e:
#         print(e)
