from src.service.wsapiservice import WSApi
from src.service.folderabs import FolderABS
from src.service.exceptions import WSApiException
from unittest.mock import patch
from unittest import mock
from pytest import fixture, raises, mark
from datetime import datetime


@fixture(scope="session")
def wsapi():
    api = WSApi("INTERPLAY-6", "ORFAOS DA TERRA", "userapi", "passapi")
    assert isinstance(api, FolderABS)
    return api


def test_get_credentials():
    api = WSApi("INTERPLAY-6", "ORFAOS DA TERRA", "userapi", "passapi")
    creds = api.getCredentials("user_api", "pass_api")
    assert creds["Username"] == "user_api"
    assert creds["Password"] == "pass_api"


def test_listfolders(wsapi):
    assert wsapi.interplay == "interplay://INTERPLAY-6"
    assert wsapi.product == "ORFAOS DA TERRA"
    assert wsapi.header_auth["Username"] == "userapi"
    assert wsapi.header_auth["Password"] == "passapi"


@patch("src.service.wsapiservice.Client")
def test_set_client(mock_zeep, wsapi):
    wsapi.setClient("http://localhost/services/Assets?wsdl")
    assert mock_zeep.call_count == 1


def test_set_client_exception(wsapi):
    with raises(WSApiException) as apiexec:
        assert wsapi.setClient("http://localhost/services/Assets?wsdl")
    assert (
        "WebService unavailable. Check http://localhost/services/Assets?wsdl configuration."
        == str(apiexec.value)
    )

@patch("src.service.wsapiservice.WSApi.webServiceGetChildren")
def test_list_folders(mock_wsapi, wsapi):
    from tests.wsresultmock import mock_result

    mock_wsapi.return_value = mock_result
    wsapi.watchfolder = "Projects/ORFAOS DA TERRA/GLOOBOX/EXTERNA"
    folders, files = wsapi.listFolder("Projects/ORFAOS DA TERRA/GLOOBOX/EXTERNA")
    mock_wsapi.assert_called_with("Projects/ORFAOS DA TERRA/GLOOBOX/EXTERNA")
    assert folders == [
        "Projects/ORFAOS DA TERRA/GLOOBOX/EXTERNA/V_F55_SR_SQ_R121_190408_UP10 (LIBERADO) OK FLA",
        "Projects/ORFAOS DA TERRA/GLOOBOX/EXTERNA/V_F55_XAVC_R122_190408_UP10 (LIBERADO) OK FLA",
    ]
    assert files == ["R123C006_190408DY", "R123C005_190408PO", "R123C004_190408RN"]

    mock_wsapi.return_value = None
    wsapi.watchfolder = (
        "Projects/ORFAOS DA TERRA/GLOOBOX/EXTERNA/Folder has no folders or files/"
    )
    folders, files = wsapi.listFolder(
        "Projects/ORFAOS DA TERRA/GLOOBOX/EXTERNA/Folder has no folders or files/"
    )
    mock_wsapi.assert_called_with("Projects/ORFAOS DA TERRA/GLOOBOX/EXTERNA/Folder has no folders or files/")
    assert files == []
    assert folders == []

@mark.skip
def test_web_service_get_attributes():
    uri = "interplay://INTERPLAY-6/Projects/ORFAOS DA TERRA/GLOOBOX/EXTERNA/INGEST/MATERIAL SR/04-2019"
    api = WSApi("INTERPLAY-6", "ORFAOS DA TERRA", "ipws_user", "ipws_pass")
    api.setClient("http://localhost/services/Assets?wsdl")
    result = api.webServiceGetAttributes(uri)

@mark.skip
def test_get_asset_modified_date():
    path = "Projects/ORFAOS DA TERRA/GLOOBOX/EXTERNA/INGEST/MATERIAL SR/04-2019"
    api = WSApi("INTERPLAY-6", "ORFAOS DA TERRA", "ipws_user", "ipws_pass")
    api.setClient("http://localhost/services/Assets?wsdl")
    result = api.getAssetDate(path)
    assert isinstance(result, datetime)
    assert str(result) == "2019-04-08 22:25:39.785000-03:00"
