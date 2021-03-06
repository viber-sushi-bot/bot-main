"""Additional functions for Viber bot."""
import os
from functools import partial
from dotenv import load_dotenv
from geopy.geocoders import Nominatim
from viberbot.api.messages.data_types.location import Location
from .resources.media_map import MEDIA_MAP


def dotenv_definer():
    load_dotenv('.env')


def get_address(location: Location) -> str:
    """Transcripting location coordinates to real address."""
    geolocator = Nominatim(user_agent="SushiPizzaBot")
    coordinates_transcriptor = partial(geolocator.reverse, language="ru")
    lat, lon = location.latitude, location.longitude
    return str(coordinates_transcriptor(f"{lat}, {lon}"))


def rich_message_consctructor(category: str) -> dict:
    """Pasting infromation from list of items to rich message template."""
    templates = []
    for vowel in MEDIA_MAP[category]:
        buttons = []
        for item in vowel:
            buttons.append(
                {
                    "Columns": 6,
                    "Rows": 6,
                    "ActionType": "reply",
                    "ActionBody": f"order_{item[1]}_{item[2]}",
                    "Image": item[0],
                    "Text": item[1],
                    "TextOpacity": 0,
                }
            )
        templates.append(
            {
                "Type": "rich_media",
                "ButtonsGroupColumns": 6,
                "ButtonsGroupRows": 6,
                "BgColor": "#FFFFFF",
                "Buttons": buttons
            }
        )
    return templates


def keyboard_consctructor(items: list) -> dict:
    """Pasting infromation from list of items to keyboard menu template."""
    keyboard = {
        "DefaultHeight": False,
        "BgColor": "#FFFFFF",
        "Type": "keyboard",
        "Buttons": [{
                "Columns": 3,
                "Rows": 1,
                "BgColor": "#97be2f",
                "BgLoop": True,
                "ActionType": "reply",
                "ActionBody": item[0],
                "ReplyType": "message",
                "Text": item[1]
        } for item in items]
    }
    return keyboard


def keyboard_delete(data):
    keyboard = {
        "DefaultHeight": False,
        "BgColor": "#FFFFFF",
        "Type": "keyboard",
        "Buttons": [{
                "Columns": 3,
                "Rows": 1,
                "BgColor": "#97be2f",
                "BgLoop": True,
                "ActionType": "reply",
                "ActionBody": f"delete_{item[0]}",
                "ReplyType": "message",
                "Text": '?????? ' + item[0]
        } for item in data]
    }
    if len(data) % 2 == 0:
        MENU_BUTTON = {
            "Columns": 6,
            "Rows": 1,
            "BgColor": "#97be2f",
            "BgLoop": True,
            "ActionType": "reply",
            "ActionBody": "menu",
            "ReplyType": "message",
            "Text": "????????"
        }
    else:
        MENU_BUTTON = {
            "Columns": 3,
            "Rows": 1,
            "BgColor": "#97be2f",
            "BgLoop": True,
            "ActionType": "reply",
            "ActionBody": "menu",
            "ReplyType": "message",
            "Text": "????????"
        }
    keyboard['Buttons'].append(MENU_BUTTON)
    return keyboard
