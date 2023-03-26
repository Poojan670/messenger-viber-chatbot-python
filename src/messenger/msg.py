import requests

from src.messenger.helper import get_user_info, send_message
from src.core.config import settings
from src.models.models import LanguageEnum
from src.messenger import bank_list
from src.core.config import API, THREAD_CONTROL_API
from src.messenger.templates import template_messages


async def template_message(sender_id):
    response = {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": [
                    {
                        "title": "Welcome!",
                        "image_url": "https://f1soft.com/img/logo-200.png",
                        "subtitle": "We have the right advice for everyone.",
                        "default_action": {
                            "type": "web_url",
                            "url": "https://f1soft.com/",
                            "webview_height_ratio": "tall",
                        },
                        "buttons": [
                            {
                                "type": "web_url",
                                "url": "https://f1soft.com/",
                                "title": "View Website"
                            }, {
                                "type": "postback",
                                "title": "Start Chatting",
                                "payload": "start_chatting_payload"
                            }
                        ]
                    },
                    {
                        "title": "Welcome!",
                        "image_url": "https://f1soft.com/img/f1soft_contact.jpg",
                        "subtitle": "We have the right tools for everyone.",
                        "default_action": {
                            "type": "web_url",
                            "url": "https://f1soft.com/",
                            "webview_height_ratio": "tall",
                        },
                        "buttons": [
                            {
                                "type": "web_url",
                                "url": "https://f1soft.com/",
                                "title": "View Website"
                            }, {
                                "type": "postback",
                                "title": "Start Chatting",
                                "payload": "DEVELOPER_DEFINED_PAYLOAD"
                            }
                        ]
                    }
                ]
            }
        }
    }
    await send_message(sender_id, response)


async def button_response(sender_id):
    response = {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "button",
                "text": "What do you want to do next?",
                "buttons": [
                    {
                        "type": "web_url",
                        "url": "https://www.messenger.com",
                        "title": "Visit Messenger"
                    },
                    {
                        "type": "web_url",
                        "url": "https://www.youtube.com",
                        "title": "Visit Youtube"
                    },
                ]
            }
        }
    }
    await send_message(sender_id, response)


async def quick_message(sender_id):
    request_body = {
        "recipient": {
            "id": sender_id
        },
        "messaging_type": "RESPONSE",
        "message": {
            "text": "Pick a color:",
            "quick_replies": [
                {
                    "content_type": "text",
                    "title": "Red",
                    "payload": "RED_COLOR_POSTBACK",
                    "image_url": "https://w7.pngwing.com/pngs/614/895/png-transparent-circle-red-logo-red-circle-logo"
                                 "-sphere-alpha-compositing.png "
                }, {
                    "content_type": "text",
                    "title": "Green",
                    "payload": "GREEN_COLOR_POSTBACK",
                    "image_url": "https://w7.pngwing.com/pngs/51/802/png-transparent-circle-green-circle-color-grass"
                                 "-sphere.png "
                }
            ]
        }
    }
    response = requests.post(API, json=request_body).json()
    return response


async def red_color_postback(sender_id):
    await send_message(sender_id, {"text": "You picked Red Color, Great"})


async def green_color_postback(sender_id):
    await send_message(sender_id, {"text": "You picked Green Color, Great"})


async def image_message(sender_id):
    import random
    resolution = random.randint(720, 1920)
    response = {
        "attachment": {
            "type": "image",
            "payload": {
                "url": f"https://picsum.photos/{resolution}"
            }
        }
    }
    await send_message(sender_id, response)


async def hi_message(sender_id):
    user_info = await get_user_info(sender_id)
    await send_message(sender_id, {
        "text": f"Hello, {user_info['first_name']}"
    })


async def send_echo_message(sender_id, payload):
    # if payload['message'].get('text'):
    await send_message(sender_id, {"text": payload})
    #     messaging = event['messaging']
    #     for x in messaging:
    #         if x.get('message'):
    #             recipient_id = x['sender']['id']
    #             if x['message'].get('text'):
    #                 message = x['message']['text']
    #                 bot.send_text_message(recipient_id, message)
    #             if x['message'].get('attachments'):
    #                 for att in x['message'].get('attachments'):
    #                     bot.send_attachment_url(recipient_id, att['type'], att['payload']['url'])
    #         else:
    #             pass


async def send_message_to_new_user(sender_id: str):
    user_info = await get_user_info(sender_id)
    response1 = {
        "text": f"Hi {user_info['first_name']} ! Welcome to {settings.MESSENGER_BOT_NAME}, where, you will get all queries "
                f"answered"
    }

    response2 = {
        "attachment": {
            "type": "image",
            "payload": {
                "url": "https://f1soft.com/img/logo-200.png"
            }
        }
    }

    response3 = {
        "text": "At any time, use the menu below to navigate through the features."
    }

    response4 = {
        "text": "What can I do to help you today?",
        "quick_replies": [
            {
                "content_type": "text",
                "title": "Languages",
                "payload": "LANGUAGES",
            },
            {
                "content_type": "text",
                "title": "Banks",
                "payload": "LOOKUP_BANKS",
            },
            {
                "content_type": "text",
                "title": "Talk to an agent",
                "payload": "TALK_AGENT",
            },
            {
                "content_type": "text",
                "title": "Chat with me",
                "payload": "BOT_CHAT",
            },
        ]
    }

    await send_message(sender_id, response1)
    await send_message(sender_id, response2)
    await send_message(sender_id, response3)
    await send_message(sender_id, response4)


async def pass_thread_control(sender_id, param):
    target_app_id = ""
    metadata = ""

    if param == "page_inbox":
        target_app_id = settings.SECONDARY_RECEIVER_ID
        metadata = "Pass thread control to inbox chat"

    if param == "primary":
        target_app_id = settings.PRIMARY_RECEIVER_ID
        metadata = "Pass thread control to the bot, primary app"

    request_body = {
        "recipient": {
            "id": sender_id
        },
        "target_app_id": target_app_id,
        "metadata": metadata
    }

    requests.post(THREAD_CONTROL_API, json=request_body).json()


async def request_agent_talk(sender_id, language):
    if language == LanguageEnum.english:
        response = {
            "text": "Ok, Someone real will be with you in a few minutes"
        }
    else:
        response = {
            "text": "ठीक छ, कोही वास्तविक केही मिनेटमा तपाईंसँग हुनेछ"
        }
    await send_message(sender_id, response)

    """
    Switch this conversation to page inbox
    """
    await pass_thread_control(sender_id, "page_inbox")


async def back_to_main_menu(sender_id):
    response = template_messages.back_to_main_menu_template()
    await send_message(sender_id, response)


async def back_to_process_menu(sender_id, language):
    response = template_messages.back_to_process_menu_template(language)
    await send_message(sender_id, response)


async def take_thread_control(sender_id):
    request_body = {
        "recipient": {
            "id": sender_id
        },
        "metadata": "Pass this conversation from page inbox to the bot - primary app"
    }

    try:
        requests.post(THREAD_CONTROL_API, request_body)
    except Exception as e:
        try:
            await send_message(sender_id, {"text": "The chatbot default is back !!"})
            await back_to_main_menu(sender_id)
            print("Message sent")
        except Exception as e:
            print("Unable to send message while thread control")


async def lookup_banks(sender_id):
    response = template_messages.lookup_banks_categories_template()
    await send_message(sender_id, response)


async def list_government_banks(sender_id, repeat):
    if not repeat:
        await send_message(sender_id, {"text": "There are {} governmental banks in Nepal"
                           .format(len(bank_list.government_banks))})
    await send_message(sender_id, template_messages.government_banks_select())


async def list_private_banks(sender_id, repeat):
    if not repeat:
        await send_message(sender_id, {"text": "There are {} private banks in Nepal"
                           .format(23)})
    await send_message(sender_id, template_messages.private_banks_select())


async def selected_government_bank(sender_id, payload):
    bank_name = bank_list.government_banks[int(payload[-1]) - 1]['title']
    await send_message(sender_id, {"text": "You have selected {}".format(bank_name)})
    await send_message(sender_id, template_messages.banks_select_choices(payload[-1]))


async def selected_private_bank(sender_id, payload):
    bank_name = bank_list.private_banks[int(payload[-1]) - 1]['title']
    await send_message(sender_id, {"text": "You have selected {}".format(bank_name)})
    await send_message(sender_id, template_messages.private_banks_select_choices(payload[-1]))


async def government_post_operation(sender_id, payload):
    bank_name = bank_list.government_banks[int(payload[-1]) - 1]['title']
    await send_message(sender_id, template_messages.government_banks_post_choices(bank_name, payload[-1]))


async def private_post_operation(sender_id, payload):
    bank_name = bank_list.private_banks[int(payload[-1]) - 1]['title']
    await send_message(sender_id, template_messages.private_banks_post_choices(bank_name, payload[-1]))


async def describe_bank(sender_id, payload, choices):
    choices_operation = {
        "GOVERNMENT": government_post_operation(sender_id, payload),
        "PRIVATE": private_post_operation(sender_id, payload)
    }
    await choices_operation.get(choices, None)


async def chat_with_bot(sender_id):
    await send_message(sender_id, {"text": "What do you want to talk about?"})


async def whats_up_message(sender_id):
    user_info = await get_user_info(sender_id)
    await send_message(sender_id, {"text": f"I am fine {user_info['first_name']}, What about you?"})


async def government_bank_info(sender_id, payload):
    bank_desc = bank_list.government_banks[int(payload[-1]) - 1]['description']
    await send_message(sender_id, {"text": bank_desc})
    await government_post_operation(sender_id, payload)


async def private_bank_info(sender_id, payload):
    bank_desc = bank_list.private_banks[int(payload[-1]) - 1]['description']
    await send_message(sender_id, {"text": bank_desc})
    await private_post_operation(sender_id, payload)


async def government_mobile_banking(sender_id, payload):
    bank = bank_list.government_banks[int(payload[-1]) - 1]
    if bank['mobile_banking']["android"]:
        await send_message(sender_id, {"text": f"Mobile Banking is available for {bank['title']}"})
        await government_post_operation(sender_id, payload)
    else:
        await send_message(sender_id, {"text": f"Mobile Banking is not available for {bank['title']}"})
        await government_post_operation(sender_id, payload)


async def private_mobile_banking(sender_id, payload):
    bank = bank_list.private_banks[int(payload[-1]) - 1]
    if bank['mobile_banking']["android"]:
        await send_message(sender_id, {"text": f"Mobile Banking is available for {bank['title']}"})
        await private_post_operation(sender_id, payload)
    else:
        await send_message(sender_id, {"text": f"Mobile Banking is not available for {bank['title']}"})
        await private_post_operation(sender_id, payload)


async def government_branches(sender_id, payload):
    await send_message(sender_id, {"text": "Working on it!!!!!!!!!!!"})
