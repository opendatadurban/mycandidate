from ...app import db
import uuid

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from main.database.base_class import Base
from wtforms import SelectField, validators
from ...forms import Form


class PoliticalParty(Base):
    """
    Political Party Table
    """
    __tablename__ = 'political_party'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)
    abbreviation = Column(String(20))

    
    def __repr__(self):
        return f'<id {self.id}>'
    
    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'abbv': self.abbreviation,
        }

class Person(Base):
    """
    Person Table
    """
    __tablename__ = 'person'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    surname = Column(String(255))
    gender = Column(String(10), nullable=True)
    race = Column(String(50), nullable=True)
    party_id = Column(Integer, ForeignKey('political_party.id'))
    political_party = relationship('PoliticalParty', backref='persons')
    # metadata = Column(String(355), nullable=True)
    

    def __repr__(self):
        return f'<id {self.id}>'
    
    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'surname': self.surname,
            'gender': self.gender if self.gender else None,
            'race': self.race if self.race else None,
            'party': self.political_party.json() if self.political_party else None
        }
    
class Constituency(Base):
    """
    Constituency Table
    """
    __tablename__ = 'constituency'

    id = Column(Integer, primary_key=True)
    code = Column(String(20), nullable=True)
    name = Column(String(255), unique=True, nullable=True)

    def __repr__(self):
        return f'<id {self.id}>'
    
    def json(self):
        return {
            'id': self.id,
            'name': self.name if self.name else None,
            'code': self.code if self.code else None,
        }

class Province(Base):
    """
    Person Table
    """
    __tablename__ = 'province'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)
    code = Column(String(10))

    def __repr__(self):
        return f'<id {self.id}>'
    
    def json(self):
        return {
            'id': self.id,
            'name': self.name if self.name else None,
            'code': self.code if self.code else None,
        }

class Ward(Base):
    """
    Ward Table
    """
    __tablename__ = 'ward'

    id = Column(Integer, primary_key=True)
    province_id = Column(Integer, ForeignKey('province.id'))
    name = Column(String(255))
    code = Column(String(20), unique=True)
    province = relationship('Province', backref='wards')

    def __repr__(self):
        return f'<id {self.id}>'
    
    def json(self):
        return {
            'id': self.id,
            'name': self.name if self.name else None,
            'code': self.code if self.code else None,
            'province': self.province.json(),
        }

class Candidate(Base):
    """
    Candidate link table 
    """
    __tablename__ = 'candidates'

    id = Column(Integer, primary_key=True)
    candidate_type = Column(String(50))
    person_id = Column(Integer, ForeignKey('person.id'))
    party_id = Column(Integer, ForeignKey('political_party.id'))
    constituency_id = Column(Integer, ForeignKey('constituency.id'), nullable=True)
    ward_id = Column(Integer, ForeignKey('ward.id'), nullable=True)
    

    # Associations
    person = relationship('Person', backref='candidates')
    party = relationship('PoliticalParty', backref='candidates')
    constituency = relationship('Constituency', backref='candidates')
    ward = relationship('Ward', backref='candidates')

    def __repr__(self):
        return f'<id {self.id}>'
    
    def to_dict(self):
        return {
            'candidate_type': self.candidate_type if self.candidate_type else None,
            'person': self.person.json() if self.person else None,
            # 'political_party': self.party.json() if self.party else None,
            'ward': self.ward.json() if self.ward and self.ward.id == self.ward_id else None,
            'constituency': self.constituency.json() if self.constituency else None,
        }
    
def create_form(candidate_type):
    class CandidatesForm(Form):
        ds_id = SelectField('Country', [validators.DataRequired()])

        def __init__(self, *args, **kwargs):
            super(CandidatesForm, self).__init__(*args, **kwargs)
            retrieve_query = f"SELECT * FROM candidates WHERE candidate_type = '{candidate_type}'"
            result = db.session.execute(retrieve_query) 
            self.ds_id.choices = [(assurance.county_code, f'{assurance.county_code} - {assurance.county_name}')
                                  for assurance in result]
            self.ds_id.choices.insert(0, ("", ""))

        def validate(self):
            return super(CandidatesForm, self).validate()

        def populate_obj(self, obj):
            super(CandidatesForm, self).populate_obj(obj)
    return CandidatesForm()

def get_data():
    distinct_types_query = """
        SELECT DISTINCT candidate_type FROM candidates
    """
    distinct_types_result = db.session.execute(distinct_types_query)

    data = []
    for row in distinct_types_result:
        candidate_type = row[0]
        form = create_form(candidate_type)
        data.append({
            'form': form,
            'candidate_type': candidate_type
        })
    return data
