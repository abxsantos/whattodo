import json

from unittest import mock
from unittest.mock import mock_open
from unittest.mock import patch

import pytest

from whattodo.file_storage import read_from_json
from whattodo.file_storage import store_to_json


@pytest.mark.smoke
def test_store_to_json():
    open_mock = mock_open()
    with patch("whattodo.file_storage.open", open_mock, create=True):
        data = "test_data"
        store_to_json(data=data)
    open_mock.assert_called_with("whattodo_data.json", "w+", encoding="utf-8")
    open_mock.return_value.write.assert_called_once_with(json.dumps(data))


@mock.patch("builtins.open", create=True)
def test_read_from_json(mock_open):
    data = "test_data"
    mock_open.side_effect = [mock.mock_open(read_data=json.dumps(data)).return_value]
    result = read_from_json()
    assert result == data
