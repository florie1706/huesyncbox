"""Test the Philips Hue Play HDMI Sync Box class."""

import asyncio

import aiohuesyncbox
import pytest
from custom_components.huesyncbox import huesyncbox
from pytest_homeassistant_custom_component.common import patch

from .helpers import mock_api

# from pytest_homeassistant_custom_component.common import (
#     MockConfigEntry,
# )


# TODO: move device registry code from huesyncbox class to async_setup_entry in  __init__.py
# async def test_huesyncbox_setup(hass, mock_api):
#     """Test a successful setup."""
#     entry = MockConfigEntry()
#     entry.data = {"host": "1.2.3.4", "unique_id": "mock-unique-id", "access_token": "mock-access-token", "port": 1234, "path": "mock-path"}

#     syncbox = huesyncbox.HueSyncBox(hass, entry)

#     with patch("aiohuesyncbox.HueSyncBox", return_value=mock_api):
#         assert await syncbox.async_setup() is True

#     assert syncbox.api is mock_api
#     assert mock_api.initialize.call_count == 1


async def test_register_authentication_required(hass, mock_api):
    """Test exception if we cannot connect."""
    with patch.object(
        mock_api, "register", side_effect=asyncio.TimeoutError
    ), pytest.raises(huesyncbox.AuthenticationRequired):
        await huesyncbox.async_register_aiohuesyncbox(hass, mock_api)

    with patch.object(
        mock_api, "register", side_effect=aiohuesyncbox.Unauthorized
    ), pytest.raises(huesyncbox.AuthenticationRequired):
        await huesyncbox.async_register_aiohuesyncbox(hass, mock_api)


async def test_register_cannot_connect(hass, mock_api):
    """Test cannot connect exception."""
    with patch.object(
        mock_api, "register", side_effect=aiohuesyncbox.RequestError
    ), pytest.raises(huesyncbox.CannotConnect):
        await huesyncbox.async_register_aiohuesyncbox(hass, mock_api)

    with patch.object(
        mock_api, "register", side_effect=aiohuesyncbox.AiohuesyncboxException
    ), pytest.raises(huesyncbox.CannotConnect):
        await huesyncbox.async_register_aiohuesyncbox(hass, mock_api)
