import pytest
import requests.exceptions

from flojoy import Image, DataFrame, Grayscale

FLOJOY_LOCAL_FILE_SYSTEM_ASSETS_URL = "https://raw.githubusercontent.com/flojoy-ai/nodes/22908c9fbee6b923b10d36091be31c05c9b74e03/LOADERS/LOCAL_FILE_SYSTEM/LOCAL_FILE/assets"  # noqa: E501



@pytest.mark.parametrize(
    "file_url",
    [
        "not_valid",
        "/not/a/valid/url",
        "ftp://not_existing.url",
        "htp://misstyped.url",
    ],
)
def test_REMOTE_FILE_not_valid(file_url):
    import REMOTE_FILE

    with pytest.raises(ValueError):
        REMOTE_FILE.REMOTE_FILE(file_url=file_url, file_type="Image")
