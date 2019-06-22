from src.service.cliservice import CliService
from src.service.wsapiservice import WSApi
from unittest.mock import patch
from unittest import mock
from pytest import fixture, raises, mark


@fixture(scope="session")
def cli():
    pass
    # api = CliService('ws_usr', 'ws_pwd', '127.0.0.1', 'sdr_table', 'db_usr_name', 'db_usr_pwd')
    # assert isinstance(api, FolderABS)
    # return api


def test_init():
    # settings = [
    #     {
    #         "id": 1,
    #         "settings_name": "DIAS FELIZES",
    #         "pam_source": "INTERPLAY-13",
    #         "pam_destination": "RJ2-JB-VIE",
    #         "wsdl_source": "http://10.228.112.104/services/Assets?wsdl",
    #         "wsdl_destination": "http://10.228.112.104/services/Assets?wsdl",
    #         "watch_folder": "Projects/DIAS FELIZES/GLOOBOX/EXTERNA",
    #     },
    #     {
    #         "id": 2,
    #         "settings_name": "VERAO 90",
    #         "pam_source": "INTERPLAY-6",
    #         "pam_destination": "RJ2-JB-VIE",
    #         "wsdl_source": "http://10.228.112.104/services/Assets?wsdl",
    #         "wsdl_destination": "http://10.228.112.104/services/Assets?wsdl",
    #         "watch_folder": "Projects/VERAO 90/GLOOBOX/EXTERNA",
    #     },
    #     {
    #         "id": 3,
    #         "settings_name": "ORFAOS DA TERRA",
    #         "pam_source": "INTERPLAY-6",
    #         "pam_destination": "RJ2-JB-VIE",
    #         "wsdl_source": "http://10.228.112.104/services/Assets?wsdl",
    #         "wsdl_destination": "http://10.228.112.104/services/Assets?wsdl",
    #         "watch_folder": "Projects/ORFAOS DA TERRA/GLOOBOX/EXTERNA",
    #     },
    #     {
    #         "id": 4,
    #         "settings_name": "MALHACAO",
    #         "pam_source": "INTERPLAY-11",
    #         "pam_destination": "RJ2-JB-VIE",
    #         "wsdl_source": "http://10.228.112.104/services/Assets?wsdl",
    #         "wsdl_destination": "http://10.228.112.104/services/Assets?wsdl",
    #         "watch_folder": "Projects/MALHACAO TFDA 2019/GLOOBOX/EXTERNA",
    #     },
    # ]
    pass


def test_run():
    pass
