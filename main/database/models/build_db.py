from . import *  # noqa
from ...app import app
import pandas as pd

CHUNK_SIZE = 3500
records = []

def seed_site_settings(db, excel_file_path):
    xls = pd.ExcelFile(f'{excel_file_path}')
    df = pd.read_excel(xls, 'site_settings')
    for index, row in df.iterrows():
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
                )
            
                # Dynamically handle additional columns
                for column in df.columns:
                    if column not in ["title", "title_short", "navbar_logo", "favicon_link", "primary_color", "secondary_color"]:
                        setattr(config, column, row[column])

                db.session.add(config)
    try:
        db.session.commit()
    except Exception as e:
        print(e)    

def seed_political_party(db, excel_file_path):
    xls = pd.ExcelFile(f'{excel_file_path}')
    df = pd.read_excel(xls, 'candidate_final')
    records = []

    for index, row in df[df['party_name'].notna()].iterrows():
        if row["party_name"]:
            # Check if it exists
            instance = db.session.query(PoliticalParty).filter(
                                PoliticalParty.name == row["party_name"]).filter(
                                    PoliticalParty.abbreviation == row["party_code"]
                                ).first()
            
            # Flag to track if a matching province is found in records
            found_matching_party = False
            
            # Check if it exists in queryset
            if instance is not None:
                found_matching_party = True
                print("existing")
                break

            # Check if it exists in records
            for prov in records:
                if prov.name == row["party_name"] or prov.abbreviation == row["party_code"]:
                    found_matching_party = True
                    print("true")
                    break

            if not found_matching_party:
                political_party = PoliticalParty(
                    name=row["party_name"],
                    abbreviation=row["party_code"]
                )

                records.append(political_party)

        if len(records) >= CHUNK_SIZE:
            db.session.bulk_save_objects(records)
            db.session.commit()
            records.clear()
            print(F"Bulk Save")
    
    # Commit any remaining records
    if records:
        try:
            db.session.bulk_save_objects(records)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print("DB exception: ", e)
            raise

def seed_people(db, excel_file_path):
    xls = pd.ExcelFile(f'{excel_file_path}')
    df = pd.read_excel(xls, 'candidate_final')
    records = []
   
    for index, row in df[df['full_name'].notna()].iterrows():
        if row["full_name"]:
            print("new person")
            # Create a new Person instance
            person = Person(
                name=row["full_name"],
                surname=row["surname"],
                gender=row["gender"],
                race=row["race"],
            )

            # Get province and if exists link appropriately
            political_party = db.session.query(PoliticalParty).filter(PoliticalParty.name == row["party_name"]).first()
            print("Party", political_party)
            if political_party:
                person.party_id = political_party.id

            # Append the Person instance to the records list
            records.append(person)

            if len(records) >= CHUNK_SIZE:
                try:
                    db.session.bulk_save_objects(records)
                    db.session.commit()
                    records.clear()
                    print("Bulk Save")
                except Exception as e:
                    db.session.rollback()
                    print("DB exception: ", e)
                    raise

    # Commit any remaining records
    if records:
        try:
            db.session.bulk_save_objects(records)
            db.session.commit()
            print("Final Bulk Save")
        except Exception as e:
            db.session.rollback()
            print("DB exception: ", e)
            raise

def seed_constituency(db, excel_file_path):
    xls = pd.ExcelFile(f'{excel_file_path}')
    df = pd.read_excel(xls, 'candidate_final')
    records = []

    for index, row in df[df['constituency_name'].notna()].iterrows():
        if row["constituency_name"] is not None:
            print("working in here", row["constituency_name"])
            
            # Check if it exists
            existing_constituency = db.session.query(Constituency).filter(
                                    Constituency.name == row["constituency_name"]).filter(
                                        Constituency.code == row["constituency_code"]
                                    ).first()

            # Flag to track if a matching province is found in records
            found_matching_constituency = False
            
            # Check if it exists in queryset
            if existing_constituency is not None:
                found_matching_constituency = True
                print("existing")
                break

            # Check if it exists in records
            for prov in records:
                if prov.name == row["constituency_name"] or prov.code == row["constituency_code"]:
                    found_matching_constituency = True
                    print("true")
                    break

            if not found_matching_constituency:
                constituency = Constituency(
                    name=row["constituency_name"],
                    code=row["constituency_name"]
                )
            
                records.append(constituency)

            if len(records) >= CHUNK_SIZE:
                db.session.bulk_save_objects(records)
                db.session.commit()
                records.clear()
                print(F"Bulk Save")
    
    # Commit any remaining records
    if records:
        try:
            db.session.bulk_save_objects(records)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print("DB exception: ", e)
            raise


def seed_province(db, excel_file_path):
    xls = pd.ExcelFile(f'{excel_file_path}')
    df = pd.read_excel(xls, 'candidate_final')
    records = []

    for index, row in df[df['province'].notna()].iterrows():
        if row["province"]:
            # Check if it exists
            existing_province = db.session.query(Province).filter(
                                    Province.name == row["province"]).filter(
                                        Province.code == row["province_code"]
                                    ).first()

            # Flag to track if a matching province is found in records
            found_matching_province = False
            
            # Check if it exists in queryset
            if existing_province is not None:
                found_matching_province = True
                print("existing")
                break

            # Check if it exists in records
            for prov in records:
                if prov.name == row["province"] or prov.code == row["province_code"]:
                    found_matching_province = True
                    print("true")
                    break

            if not found_matching_province:
                province = Province(
                    name=row["province"],
                    code=row["province_code"]
                )

                records.append(province)

            if len(records) >= CHUNK_SIZE:
                db.session.bulk_save_objects(records)
                db.session.commit()
                records.clear()
                print(F"Bulk Save")
    
    # Commit any remaining records
    if records:
        try:
            db.session.bulk_save_objects(records)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print("DB exception: ", e)
            raise


def seed_ward(db, excel_file_path):
    xls = pd.ExcelFile(f'{excel_file_path}')
    df = pd.read_excel(xls, 'candidate_final')
    records = []
   
    for index, row in df[df['ward_name'].notna()].iterrows():
        if row["ward_name"]:
            # Check if it exists
            existing_ward = db.session.query(Ward).filter(
                                    Ward.name == row["ward_name"]).filter(
                                        Ward.code == str(row["ward_code"])
                                    ).first()

            # Flag to track if a matching ward is found in records
            found_matching_ward = False
            
            # Check if it exists in queryset
            if existing_ward is not None:
                found_matching_ward = True
                print("existing")
                # break

            # Check if it exists in records array
            for ward in records:
                if ward.name == row["ward_name"] and ward.code == str(row["ward_code"]):
                    found_matching_ward = True
                    print("true")
                    break

            if not found_matching_ward:
                ward = Ward(
                    name=row["ward_name"],
                    code=str(row["ward_code"])
                )

                # Get province and if exists link appropriately
                instance = db.session.query(Province).filter(Province.name == row["province"]).first()
                if instance:
                    ward.province_id = instance.id
                
                records.append(ward)
                
            if len(records) >= CHUNK_SIZE:
                db.session.bulk_save_objects(records)
                db.session.commit()
                records.clear()
                print(F"Bulk Save")
    
    # Commit any remaining records
    if records:
        try:
            db.session.bulk_save_objects(records)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print("DB exception: ", e)
            raise

def seed_candidates(db, excel_file_path):
    xls = pd.ExcelFile(f'{excel_file_path}')
    df = pd.read_excel(xls, 'candidate_final')
    records = []
   
    for index, row in df[df['candidate_type'].notna()].iterrows():
        # Check for the specific field and use that to locate all candidates
        if row["candidate_type"] and row["full_name"] and row["party_name"] and row["ward_name"]:
            candidate = Candidate()
            if pd.notna(row["full_name"]):
                person_instance = db.session.query(Person).filter(Person.name == row["full_name"]).first()
                if person_instance:
                    candidate.person_id = person_instance.id
                    candidate.party_id = person_instance.party_id

            # if pd.notna(row["party_name"]):
            #     political_party = db.session.query(PoliticalParty).filter(PoliticalParty.name == row["party_name"]).first()
            #     if political_party:
            #         candidate.party_id = political_party.id

            if pd.notna(row["ward_name"]):
                ward_instance = db.session.query(Ward).filter(Ward.name == row["ward_name"]).filter(Ward.code == str(row["ward_code"])).first()
                if ward_instance:
                    candidate.ward_id = ward_instance.id

            if pd.notna(row["constituency_name"]):
                constituency_instance = db.session.query(Constituency).filter(Constituency.name == row["constituency_name"]).first()
                if constituency_instance:
                    candidate.constituency = constituency_instance.id

            candidate.candidate_type = row["candidate_type"]

            records.append(candidate)
            if len(records) >= CHUNK_SIZE:
                db.session.bulk_save_objects(records)
                db.session.commit()
                records.clear()
                print(F"Bulk Save")
    
    # Commit any remaining records
    if records:
        try:
            db.session.bulk_save_objects(records)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print("DB exception: ", e)
            raise
                


