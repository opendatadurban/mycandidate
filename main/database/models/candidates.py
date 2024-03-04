from ...app import db
import uuid

from sqlalchemy import Column, Integer, String, ForeignKey, text
from sqlalchemy.orm import relationship
from main.database.base_class import Base
from wtforms import SelectField, validators
from ...forms import Form
    
def create_form(candidate_type, code, name):
    class CandidatesForm(Form):
        ds_id = SelectField('Ward', [validators.DataRequired()])

        def __init__(self, *args, **kwargs):
            super(CandidatesForm, self).__init__(*args, **kwargs)
            query = text(f"SELECT DISTINCT {code}, {name} FROM candidates WHERE candidate_type = :candidate_type")
            assurances = db.session.execute(query, {'candidate_type': candidate_type}).fetchall()
            self.ds_id.choices = [(assurance[0], f'{assurance[1]} - {assurance[0]}')
                                  for assurance in assurances]
            self.ds_id.choices.insert(0, ("", ""))

        def validate(self):
            return super(CandidatesForm, self).validate()

        def populate_obj(self, obj):
            super(CandidatesForm, self).populate_obj(obj)
    return CandidatesForm()

def get_data():
    distinct_types_query = """
        SELECT DISTINCT candidate_type, locator FROM candidates
    """
    distinct_types_result = db.session.execute(distinct_types_query)

    data = []
    for row in distinct_types_result:
        most_common_values = row[1].strip("{}").split(',')
        candidate_type = row[0]
        code = most_common_values[0]
        name = most_common_values[1]
        form = create_form(candidate_type, code, name)
        data.append({
            'form': form,
            'candidate_type': candidate_type
        })
    return data
