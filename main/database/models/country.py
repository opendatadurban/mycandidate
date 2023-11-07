from ...app import db

from sqlalchemy import Column, Integer, String
from wtforms import SelectField, validators
from ...forms import Form
from main.database.base_class import Base

class Candidate(Base):
    """
    A single data point (yearly value) of an indicator
    """
    __tablename__ = 'candidate'

    id = Column(Integer, autoincrement=True, primary_key=True)
    province = Column(String)
    constituency = Column(String)
    name = Column(String)
    sex = Column(String)
    party = Column(String)

    def __repr__(self):
        return f'<id {self.id}>'

class CandidateForm(Form):
    ds_id = SelectField('Constituency Name', [validators.DataRequired()])

    def __init__(self, *args, **kwargs):
        super(CandidateForm, self).__init__(*args, **kwargs)
        assurances = [
            (assurance.constituency,assurance.constituency)
            for assurance in Candidate.query.distinct(Candidate.constituency)
        ]
        assurances.insert(0, ("",""))
        self.ds_id.choices = assurances

    def validate(self):
        return super(CandidateForm, self).validate()

    def populate_obj(self, obj):
        super(CandidateForm, self).populate_obj(obj)

class WardCandidate(db.Model):
    """
    A Ward Candidate
    """
    __tablename__ = 'ward_candidate'

    id = Column(Integer, autoincrement=True, primary_key=True)
    province = Column(String)
    local_authority = Column(String)
    name = Column(String)
    sex = Column(String)
    party = Column(String)
    status = Column(String)
    ward_no = Column(Integer)

    def __repr__(self):
        return f'<id {self.id}>'

class WardCandidateForm(Form):
    ds_id = SelectField('Local Authority Name', [validators.DataRequired()])

    def __init__(self, *args, **kwargs):
        super(WardCandidateForm, self).__init__(*args, **kwargs)
        assurances = [
            (assurance.local_authority,assurance.local_authority)
            for assurance in WardCandidate.query.distinct(WardCandidate.local_authority)
        ]
        assurances.insert(0, ("",""))
        self.ds_id.choices = assurances

    def validate(self):
        return super(WardCandidateForm, self).validate()