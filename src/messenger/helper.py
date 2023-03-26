import requests
from fastapi import APIRouter

from src.core.config import settings
from src.core.config import API, SETUP_PROFILE_API

router = APIRouter()


async def send_message(sender_id: str, response):
    await mark_read_message(sender_id)
    await sending_message_bubble(sender_id)
    request_body = {
        "recipient": {
            "id": sender_id
        },
        "message": response
    }
    requests.post(API, json=request_body).json()
    await sending_turn_off(sender_id)


async def sending_message_bubble(sender_id: str):
    return requests.post(API, json={
        "recipient": {
            "id": sender_id
        },
        "sender_action": "typing_on"
    }).json()


async def sending_turn_off(sender_id: str):
    return requests.post(API, json={
        "recipient": {
            "id": sender_id
        },
        "sender_action": "typing_off"
    }).json()


async def mark_read_message(sender_id: str):
    return requests.post(API, json={
        "recipient": {
            "id": sender_id
        },
        "sender_action": "mark_seen"
    }).json()


async def get_user_info(sender_id: str):
    return requests.get(
        'https://graph.facebook.com/{}?fields=first_name,last_name,profile_pic&access_token={}'.format(
            sender_id, settings.FB_PAGE_TOKEN)).json()


async def setup_profile_helper():
    request_body = {
        "get_started": {
            "payload": "GET_STARTED"
        },
        "persistent_menu": [
            {
                "locale": "default",
                "composer_input_disabled": False,
                "call_to_actions": [
                    {
                        "type": "postback",
                        "title": "Talk to an agent",
                        "payload": "TALK_AGENT"
                    },
                    {
                        "type": "postback",
                        "title": "Return to main menu",
                        "payload": "BACK_TO_MAIN_MENU"
                    },
                    {
                        "type": "web_url",
                        "title": "View our website",
                        "url": "https://usemobilebanking.com/",
                        "webview_height_ratio": "full"
                    },
                ]
            }
        ],
        "whitelisted_domains": [
            "https://google.com",
            "https://usemobilebanking.com/"
        ],
        "greeting": [
            {
                "locale": "default",
                "text": "Hello! Thank you taking interest in us !"
            },
            {
                "locale": "en_US",
                "text": "Hello! Thank you taking interest in us !"
                        "This is demo fb page associated with using Mobile Banking and general stuffs,"
                        "Please visit our site: https://usemobilebanking.com/ for further details "
            }
        ]
    }
    return requests.post(SETUP_PROFILE_API, json=request_body).json()
