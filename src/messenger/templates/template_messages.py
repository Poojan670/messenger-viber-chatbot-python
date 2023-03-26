from src.models.models import LanguageEnum
from src.messenger import bank_list


def back_to_main_menu_template():
    return {
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


def back_to_process_menu_template(language):
    if language == LanguageEnum.english:
        bank_title = "Banks"
        agent_title = "Talk to an agent"
        chat_title = "Chat with me"
    else:
        bank_title = "बैंकहरू"
        agent_title = "एजेन्टसँग कुरा गर्नुहोस्"
        chat_title = "मसँग कुराकानी गर्नुहोस्"

    return {
        "text": "What can I do to help you today?",
        "quick_replies": [
            {
                "content_type": "text",
                "title": f"{bank_title}",
                "payload": "LOOKUP_BANKS",
            },
            {
                "content_type": "text",
                "title": f"{agent_title}",
                "payload": "TALK_AGENT",
            },
            {
                "content_type": "text",
                "title": f"{chat_title}",
                "payload": "BOT_CHAT",
            },
        ]
    }


def lookup_banks_categories_template():
    return {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "button",
                "text": "Select the bank category",
                "buttons": [
                    {
                        "type": "postback",
                        "title": "Government Banks",
                        "payload": "GOVERNMENT_BANKS",
                    },
                    {
                        "type": "postback",
                        "title": "Private Banks",
                        "payload": "PRIVATE_BANKS",
                    },
                    {
                        "type": "postback",
                        "title": "Development Banks",
                        "payload": "DEVELOPMENT_BANKS",
                    },
                ]
            }
        }
    }


def government_banks_post_choices(bank_name, num):
    return {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "button",
                "text": f"Select what you want to know about {bank_name}?",
                "buttons": [
                    {
                        "type": "postback",
                        "title": "Bank Info",
                        "payload": f"GOVERNMENT_BANK_INFO_{num}",
                    },
                    {
                        "type": "postback",
                        "title": "Mobile Banking",
                        "payload": f"GOVERNMENT_MOBILE_BANKING_{num}",
                    },
                    {
                        "type": "postback",
                        "title": "branches",
                        "payload": f"GOVERNMENT_BRANCHES_{num}",
                    },
                ]
            }
        }
    }


def private_banks_post_choices(bank_name, num):
    return {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "button",
                "text": f"Select what you want to know about {bank_name}?",
                "buttons": [
                    {
                        "type": "postback",
                        "title": "Bank Info",
                        "payload": f"PRIVATE_BANK_INFO_{num}",
                    },
                    {
                        "type": "postback",
                        "title": "Mobile Banking",
                        "payload": f"PRIVATE_MOBILE_BANKING_{num}",
                    },
                    {
                        "type": "postback",
                        "title": "branches",
                        "payload": f"PRIVATE_BRANCHES_{num}",
                    },
                ]
            }
        }
    }


def language_template(language):
    if language == LanguageEnum.english:
        english_title = "English"
        nepali_title = "Nepali"
        text = "Please select your language of choice"
    else:
        english_title = "अंग्रेजी"
        nepali_title = "नेपाली"
        text = "कृपया आफ्नो मनपर्ने भाषा चयन गर्नुहोस्"

    return {
        "text": f"{text}",
        "quick_replies": [
            {
                "content_type": "text",
                "title": f"{english_title}",
                "payload": "ENGLISH_LANGUAGE"
            },
            {
                "content_type": "text",
                "title": f"{nepali_title}",
                "payload": "NEPALI_LANGUAGE"
            }
        ]
    }


def government_banks_select():
    data = []
    government_banks = bank_list.government_banks
    for bank in government_banks:
        data.append({
            "title": bank['title'],
            "subtitle": bank['description'],
            "image_url": bank['image'],
            "default_action": {
                "type": "web_url",
                "url": bank['process'],
                "webview_height_ratio": "tall",
            },
            "buttons": [
                {
                    "type": "web_url",
                    "url": bank['process'],
                    "title": "Tutorial"
                }, {
                    "type": "postback",
                    "title": "Select",
                    "payload": f"GOVERNMENT_BANK_{bank['id']}"
                }
            ]
        })

    return {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": data
            }
        }
    }


def private_banks_select():
    data = []
    private_banks = bank_list.private_banks
    for bank in private_banks:
        data.append({
            "title": bank['title'],
            "subtitle": bank['description'],
            "image_url": bank['image'],
            "default_action": {
                "type": "web_url",
                "url": bank['process'],
                "webview_height_ratio": "tall",
            },
            "buttons": [
                {
                    "type": "web_url",
                    "url": bank['process'],
                    "title": "Tutorial"
                }, {
                    "type": "postback",
                    "title": "Select",
                    "payload": f"PRIVATE_BANK_{bank['id']}"
                }
            ]
        })

    return {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": data
            }
        }
    }


def banks_select_choices(num):
    return {
        "text": "Is your choice correct ?",
        "quick_replies": [
            {
                "content_type": "text",
                "title": "Yes",
                "payload": f"GOVERNMENT_BANK_SELECT_YES_{num}"
            },
            {
                "content_type": "text",
                "title": "No",
                "payload": "GOVERNMENT_BANK_SELECT_NO"
            }
        ]
    }


def private_banks_select_choices(num):
    return {
        "text": "Is your choice correct ?",
        "quick_replies": [
            {
                "content_type": "text",
                "title": "Yes",
                "payload": f"PRIVATE_BANK_SELECT_YES_{num}"
            },
            {
                "content_type": "text",
                "title": "No",
                "payload": "PRIVATE_BANK_SELECT_NO"
            }
        ]
    }
