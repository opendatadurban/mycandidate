from ..app import db
from sqlalchemy import Column, Integer, String
from wtforms import SelectField, validators
from ..forms import Form

class Config(db.Model):
    """
    For site settings
    """
    __tablename__ = 'site_settings'

    id = Column(Integer, autoincrement=True, primary_key=True)
    title = Column(String)
    title_short = Column(String)
    navbar_logo = Column(String)
    favicon_logo = Column(String)
    primary_color = Column(String)
    secondary_color = Column(String)

    def __repr__(self):
        return f'<id {self.id}>'