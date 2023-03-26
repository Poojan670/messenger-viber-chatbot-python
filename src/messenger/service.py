from src.db.base import get_db
from src.models.models import LanguageEnum
from src.messenger import msg
from src.messenger.deps import Language


async def message_service(sender_id: str, message, language: LanguageEnum, db) -> None:

    if message and 'quick_reply' in message:

        if 'payload' in message['quick_reply']:
            payload = message['quick_reply']['payload']

            if "GOVERNMENT_BANK_SELECT_YES_" in payload:
                await msg.describe_bank(sender_id, payload, "GOVERNMENT")
            elif "GOVERNMENT_BANK_SELECT_NO" in payload:
                await msg.list_government_banks(sender_id, True)
            elif "PRIVATE_BANK_SELECT_YES_" in payload:
                await msg.describe_bank(sender_id, payload, "PRIVATE")
            elif "PRIVATE_BANK_SELECT_NO" in payload:
                await msg.list_private_banks(sender_id, True)

            message_operation = {
                "LANGUAGES": Language(sender_id, language, get_db()).send_language_choices(),
                "TALK_AGENT": msg.request_agent_talk(sender_id, language),
                "LOOKUP_BANKS": msg.lookup_banks(sender_id),
                "RED_COLOR_POSTBACK": msg.red_color_postback(sender_id),
                "GREEN_COLOR_POSTBACK": msg.green_color_postback(sender_id),
                "ENGLISH_LANGUAGE": Language(sender_id, LanguageEnum.english, db).select_english_language(),
                "NEPALI_LANGUAGE": Language(sender_id, LanguageEnum.nepali, db).select_nepali_language(),
                "BOT_CHAT": msg.chat_with_bot(sender_id)
            }

            await message_operation.get(payload, "BOT_CHAT")

    if 'text' in message:
        payload = message['text'].lower()

        message_operation = {
            "template": msg.template_message(sender_id),
            "button": msg.button_response(sender_id),
            "quick": msg.quick_message(sender_id),
            "hi": msg.hi_message(sender_id),
            "show me an image": msg.image_message(sender_id),
            "what's up?": msg.whats_up_message(sender_id),
            "echo": msg.send_echo_message(sender_id, payload)
        }

        await message_operation.get(payload, "echo")


async def postback_service(sender_id: str, postback, language: LanguageEnum, db) -> None:
    payload = postback['payload']
    if payload == "GET_STARTED":
        await msg.send_message_to_new_user(sender_id)
    elif payload == "TALK_AGENT":
        await msg.request_agent_talk(sender_id, language)
    elif payload == "BACK_TO_MAIN_MENU":
        await msg.back_to_main_menu(sender_id)
    elif payload == "BACK_TO_LANGUAGES":
        await Language(sender_id, language, get_db()).back_to_language_choices()

    elif payload == "GOVERNMENT_BANKS":
        await msg.list_government_banks(sender_id, False)
    elif payload == "PRIVATE_BANKS":
        await msg.list_private_banks(sender_id, False)

    elif "GOVERNMENT_BANK_INFO_" in payload:
        await msg.government_bank_info(sender_id, payload)
    elif "GOVERNMENT_MOBILE_BANKING_" in payload:
        await msg.government_mobile_banking(sender_id, payload)
    elif "GOVERNMENT_BRANCHES_" in payload:
        await msg.government_branches(sender_id, payload)

    elif "PRIVATE_BANK_INFO_" in payload:
        await msg.private_bank_info(sender_id, payload)
    elif "PRIVATE_MOBILE_BANKING_" in payload:
        await msg.private_mobile_banking(sender_id, payload)
    elif "PRIVATE_BRANCHES_" in payload:
        await msg.government_branches(sender_id, payload)

    elif "GOVERNMENT_BANK_" in payload:
        await msg.selected_government_bank(sender_id, payload)
    elif "PRIVATE_BANK_" in payload:
        await msg.selected_private_bank(sender_id, payload)

    else:
        print("no cases found! ! ")
