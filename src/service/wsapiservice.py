from zeep import Client
from zeep.xsd import Element, String, ComplexType
from zeep.transports import Transport
from src.service.folderabs import FolderABS
from src.service.exceptions import WSApiException
from typing import Tuple


class WSApi(FolderABS):
    """
    A class to get information from interplay webservice.

    Methods
    -------
    getCredentials(usr, pwd)
        Create a xsd element object for authentication.

    setClient(wsdl)
        Sets the wsdl url address of the interplay webservice.

    setWatchFolderUrl(folder_to_watch)
        Sets the folder of the interplay that will be used as root
        folder to retrieve the informations.

    listFolder(path)
        Lists all folders and files of a given path.
    """

    def __init__(self, interplay: str, product: str, apiusr: str, apipwd: str) -> None:
        """
        Parameters
        ----------
        interplay : str
            Interplay name as configured in Interplay WebService settings

        product : str
            Product name. Used to be the novel name.

        apiusr : str
            User name to access interplay. Should have minimum read access.

        apipwd : str
            Password for the user to access interplay.
        """
        self.interplay = f"interplay://{interplay}"
        self.product = product
        self.header_auth = self.getCredentials(apiusr, apipwd)

    def getCredentials(self, usr: str, pwd: str) -> Element:
        """Create a xsd element object.

        It is the header necessary for the webservice credentials

        Parameters
        ----------
        usr: str
            Webservice user name

        pwd: str
            Webservice password

        Returns
        -------
        Element
            header xsd object for api credential.
        """
        element = "{http://avid.com/interplay/ws/assets/types}"
        creds = [
            Element(f"{element}Username", String()),
            Element(f"{element}Password", String()),
        ]
        header = Element(f"{element}UserCredentials", ComplexType(creds))
        return header(Username=usr, Password=pwd)

    def setClient(self, wsdl: str) -> None:
        """Sets the wsdl url address of the interplay webservice.

        Parameters
        ----------
        wsdl : str
            Interplay WeService URL.

        Raises
        ------
        WSApiException
            If not able to connect to interplay webservice.
        """
        try:
            transport = Transport(timeout=3)
            self.client = Client(wsdl=wsdl, transport=transport)
        except Exception as e:
            err = f"WebService unavailable. Check {wsdl} configuration."
            raise WSApiException(err)

    def setWatchFolderUrl(self, folder_to_watch: str) -> None:
        """Sets the folder of the interplay

        The folder will be used as root folder to retrieve the info.

        Parameters
        ----------
        folder_to_watch : str
            Folder path of the interplay.
        """
        self.watchfolder = folder_to_watch
        self.endpoint = {
            "InterplayURI": f"{self.interplay}/{folder_to_watch}",
            "IncludeFolders": True,
            "IncludeFiles": True,
            "IncludeMOBs": True,
            "ReturnAttributes": {
                "Attribute": [
                    {"Name": "Display Name", "Group": "USER"},
                    {"Name": "Type", "Group": "SYSTEM"},
                ]
            },
        }

    def webServiceClient(self, path: str) -> dict:
        """Requests webservice data from GetChildren.

        Parameters
        ----------
        path: str
            Folder that will be used to retrieve the info.

        Returns
        -------
        dict
            API json response.
        """
        self.setWatchFolderUrl(path)
        client_response = self.client.service.GetChildren(
            **self.endpoint, _soapheaders=[self.header_auth]
        )["Results"]
        return client_response

    def listFolder(self, path: str) -> Tuple[list, list]:
        """Lists all folders and files of a given path.

        Parameters
        ----------
        path: str
            Folder that will be used to retrieve the info.

        Returns
        -------
        folder : list
            All folders of the given path.

        files: list
            All files of the given path.
        """
        result = self.webServiceClient(path)
        folder = []
        files = []
        if result is None:
            return folder, files
        for i in result["AssetDescription"]:
            _type = i["Attributes"]["Attribute"].pop()
            if _type["_value_1"] == "folder":
                location = i["Attributes"]["Attribute"][-1]["_value_1"]
                folder.append(f"{self.watchfolder}/{location}")
            else:
                files.append(i["Attributes"]["Attribute"][-1]["_value_1"])
        return folder, files
