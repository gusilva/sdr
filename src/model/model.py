from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.sql import func
import datetime

Base = declarative_base()

class Settings(Base):
    """
    A command line wrapper for sdr monitoring.

    Attributes
    ----------
    __tablename__ : str
        table name.

    id : Integer
        setting id.

    settings_name : String
        setting name for the product.

    db_table: str
        Table name.

    db_usr: str
        Db username for remote connection.

    db_pwd: str
        Db user password.

    Methods
    -------
    run()
        Get settings from db and run transverse command.
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
    def serialize(self):
        return {
            "id": self.id,
            "settings_name": self.settings_name,
            "pam_source": self.pam_source,
            "pam_destination": self.pam_destination,
            "wsdl_source": self.wsdl_source,
            "wsdl_destination": self.wsdl_destination,
            "watch_folder": self.watch_folder
        }
    

class Report(Base):
    __tablename__ = "report"
    id = Column(Integer, primary_key=True)
    settings_id = Column(Integer, ForeignKey('settings.id'))
    pam_source_count = Column(Integer)
    pam_destination_count = Column(Integer)
    report_date = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)

    