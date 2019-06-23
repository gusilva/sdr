from src.service.wsapiservice import WSApi
from src.service.folderabs import FolderABS
from src.service.exceptions import WSApiException
from unittest.mock import patch
from unittest import mock
from pytest import fixture, raises, mark


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
    wsapi.setClient("http://10.228.112.104/services/Assets?wsdl")
    assert mock_zeep.call_count == 1


def test_set_client_exception(wsapi):
    with raises(WSApiException) as apiexec:
        assert wsapi.setClient("http://localhost/services/Assets?wsdl")
    assert (
        "WebService unavailable. Check http://localhost/services/Assets?wsdl configuration."
        == str(apiexec.value)
    )


# @patch('src.service.wsapiservice.WSApi')
@mark.skip
@patch("src.service.wsapiservice.WSApi.webServiceClient")
@patch("src.service.wsapiservice.Client")
def test_web_service_client(mock_wsapi_client, mock_webservice, wsapi):
    # TODO - Need to make this mock works
    import pdb

    pdb.set_trace()
    # mock_wsapi_client.service.GetChildren.side_effect = [2]
    wsapi.setClient("http://localhost/services/Assets?wsdl")
    wsapi.webServiceClient("/Project")
    assert mock_wsapi_client.call_count == 1
    assert mock_wsapi_client.service.GetChildren.call_count == 1


def test_watch_forder_uri(wsapi):
    wsapi.setWatchFolderUrl(
        "Projects/ORFAOS DA TERRA/GLOOBOX/EXTERNA/INGEST/MATERIAL SR/"
    )
    result = {
        "InterplayURI": "interplay://INTERPLAY-6/Projects/ORFAOS DA TERRA/GLOOBOX/EXTERNA/INGEST/MATERIAL SR/",
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
    assert wsapi.endpoint == result


@patch("src.service.wsapiservice.WSApi.webServiceClient")
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
    mock_wsapi.assert_called_with(
        "Projects/ORFAOS DA TERRA/GLOOBOX/EXTERNA/Folder has no folders or files/"
    )
    assert files == []
    assert folders == []
