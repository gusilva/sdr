from src.controller.dbcontroller import Controller
from sqlalchemy import create_engine
from src.service.structwalker import StructWalker
from src.service.wsapiservice import WSApi


class CliService(object):
    """
    A command line wrapper for sdr monitoring.

    Methods
    -------
    run()
        Get settings from db and run transverse command.
    """

    def __init__(
        self,
        ws_usr: str,
        ws_pwd: str,
        db_ip: str,
        db_table: str,
        db_usr: str,
        db_pwd: str,
    ) -> None:
        """
        Parameters
        ----------
        ws_usr : str
            Webservice username.

        ws_pwd: str
            Webservice password for the username.

        db_ip: str
            Ip address of the mysql db.

        db_table: str
            Table name.

        db_usr: str
            Db username for remote connection.

        db_pwd: str
            Db user password.
        """
        db_settings = f"mysql+pymysql://{db_usr}:{db_pwd}@{db_ip}/{db_table}"
        engine = create_engine(db_settings)
        self.controller = Controller(engine)
        self.ws_usr = ws_usr
        self.ws_pwd = ws_pwd

    def run(self) -> None:
        """Run the recursion through folder tree for each setting.

        It walks through folder tree systems.
        """
        settings = self.controller.getActiveProductSettings()
        for setting in settings:
            wsapi_pam_source = WSApi(
                setting["pam_source"],
                setting["settings_name"],
                self.ws_usr,
                self.ws_pwd,
            )
            wsapi_pam_source.setClient(setting["wsdl_source"])

            wsapi_pam_destination = WSApi(
                setting["pam_destination"],
                setting["settings_name"],
                self.ws_usr,
                self.ws_pwd,
            )
            wsapi_pam_destination.setClient(setting["wsdl_destination"])

            walker_pam_source = StructWalker(wsapi_pam_source)
            print(f'start {setting["settings_name"]} on {setting["pam_source"]}')
            walker_pam_source.transverse(
                setting["watch_folder"], walker_pam_source.tree
            )

            walker_pam_destination = StructWalker(wsapi_pam_destination)
            print(f'start {setting["settings_name"]} on {setting["pam_destination"]}')
            walker_pam_destination.transverse(
                setting["watch_folder"], walker_pam_destination.tree
            )

            print("saving")
            self.controller.save(
                setting["id"],
                walker_pam_source.tree.__dict__["leaves"],
                walker_pam_destination.tree.__dict__["leaves"],
            )
