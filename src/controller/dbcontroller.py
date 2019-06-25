from src.model.model import Base, Settings, Report
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime


class Controller(object):
    """
    Controller class to interact with db model data.

    Methods
    -------
    getActiveProductSettings()
        retrive the product settings from settings table model.

    save(productid, pam_source_count, pam_destination_count)
        save report data to daily report db table.

    """

    def __init__(self, dbengine: create_engine) -> None:
        """
        Parameters
        ----------
        dbengine : create_engine
            create engine object from sqlalchemy.
            
        """
        Base.metadata.bind = dbengine
        DBSession = sessionmaker(bind=dbengine)
        self.session = DBSession()

    def getActiveProductSettings(self) -> None:
        """Get active settings from db settings table.

        Returns
        -------
        list
            all active settings.
            
        """
        products = self.session.query(Settings).filter_by(status=1).all()
        return [data.serialize for data in products]

    def save(
        self, productid: int, pam_source_count: int, pam_destination_count: int
    ) -> None:
        """Save daily report to report table.

        Parameters
        ----------
        productid : int
            product setting id.

        pam_source_count: int
            production asset management source count.

        pam_destination_count: int
            production asset management destination count.
            
        """
        dt = datetime.now()
        data = {
            "settings_id": productid,
            "pam_source_count": pam_source_count,
            "pam_destination_count": pam_destination_count,
            "report_date": dt,
        }

        report = Report(**data)
        self.session.add(report)
        self.session.commit()
