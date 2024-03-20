from ...app import db
from sqlalchemy import Column, Integer, String
from wtforms import SelectField, validators
from ...forms import Form
from main.database.base_class import Base

class Config(Base):
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
    data_schemas = Column(String)
    partner_name = Column(String)
    partner_website = Column(String)
    google_analytics_key = Column(String)
    gtag_script = Column(String)
    organization_name = Column(String)
    organization_link = Column(String)

    def __repr__(self):
        return f'<id {self.id}>'
    
    def json(self):
        return {
            'id': self.id,
            'title': self.title,
            'short_title': self.title_short,
            'navbar_logo': self.navbar_logo,
            'favicon_logo': self.favicon_logo,
            'primary_color': self.primary_color,
            'secondary_color': self.secondary_color,
            'partner_name': self.partner_name,
            'partner_website': self.partner_website,
            'google_analytics_key': self.google_analytics_key,
            'gtag_script': self.gtag_script,
            'organization_name': self.organization_name,
            'organization_link': self.organization_link,
        }