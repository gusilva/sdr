from src.model.model import Base, Settings, Report
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime

class Controller(object):
    """docstring for Controller"""
    def __init__(self, dbengine):
        Base.metadata.bind = dbengine
        DBSession = sessionmaker(bind=dbengine)
        self.session = DBSession()

    def getActiveProductSettings(self):
        products = self.session.query(Settings).filter_by(status=1).all()
        return [data.serialize for data in products]


    def save(self, productid, pam_source_count, pam_destination_count):
        dt = datetime.now()
        data = {
            "settings_id": productid,
            "pam_source_count": pam_source_count,
            "pam_destination_count": pam_destination_count,
            "report_date": dt
        }

        report = Report(**data)
        self.session.add(report)
        self.session.commit()
