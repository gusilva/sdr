from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class Settings(Base):
    """
    Product setting class for db table.

    Attributes
    ----------
    __tablename__ : str
        setting table name.

    id : Integer
        setting id.

    settings_name : String
        setting name for the product.

    pam_source : String
        production asset management source.

    pam_destination : String
        production asset management destination.

    wsdl_source : String
        source url for webservice description language.

    wsdl_destination : String
        destination url for webservice description language.

    watch_folder : String
        watch folder path.

    status : Integer
        status of the setting. 0 - inactive, 1 - active

    Properties
    ----------
    serialize
        all necessary settings data.
    """

    __tablename__ = "settings"
    id = Column(Integer, primary_key=True)
    settings_name = Column(String(180), index=True)
    pam_source = Column(String(80))
    pam_destination = Column(String(80))
    wsdl_source = Column(String(500))
    wsdl_destination = Column(String(500))
    watch_folder = Column(String(1000))
    status = Column(Integer)

    @property
    def serialize(self) -> dict:
        """
        Class property that give the setting data.

        Returns
        -------
        dict 
            setting data.
        """
        return {
            "id": self.id,
            "settings_name": self.settings_name,
            "pam_source": self.pam_source,
            "pam_destination": self.pam_destination,
            "wsdl_source": self.wsdl_source,
            "wsdl_destination": self.wsdl_destination,
            "watch_folder": self.watch_folder,
        }


class Report(Base):
    """
    Daily report class for db table.

    Attributes
    ----------
    __tablename__ : str
        report table name.

    id : Integer
        report id.

    settings_id : Integer
        foreign key for the setting id.

    pam_source_count : Integer
        production asset management source count.

    pam_destination_count : Integer
        production asset management destination count.

    report_date : DateTime
        report creation date.
    """

    __tablename__ = "report"
    id = Column(Integer, primary_key=True)
    settings_id = Column(Integer, ForeignKey("settings.id"))
    pam_source_count = Column(Integer)
    pam_destination_count = Column(Integer)
    report_date = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)

class FolderTracking(Base):
    """
    Tracking folders table.

    Attributes
    ----------
    __tablename__ : str
        foldertracking table name.
    
    id : Integer
        folder tracking id.

    settings_id : Integer
        foreign key for the setting id.

    pam_source_missing_count : Integer
        production asset management source missing count.

    pam_destination_missing_count: Integer
        production asset management destination missing count.

    created_date : DateTime
        creation date.
    
    """
    __tablename__ = "foldertracking"
    id = Column(Integer, primary_key=True)
    settings_id = Column(Integer, ForeignKey("settings.id"))
    pam_source_missing_count = Column(Integer)
    pam_destination_missing_count = Column(Integer)
    created_date = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
