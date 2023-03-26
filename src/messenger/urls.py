import uuid

from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session

from src.messenger.helper import setup_profile_helper
from src.core.config import settings
from src.db.base import get_db
from src.models.models import UserInfo, LanguageEnum
from src.messenger.msg import take_thread_control
from src.messenger.service import postback_service, message_service

router = APIRouter()


@router.get("/")
async def verify_facebook(request: Request):
    if request.path_params.get("hub.mode") == "subscribe" and request.path_params.get("hub.challenge"):
        if not request.path_params.get("hub.verify_token") == "<Your Verify token>":
            return "Verification token missmatch", 403
        return request.path_params['hub.challenge'], 200
    return "Hello world", 200

    # if (request.query_params.get("hub.mode") or request.query_params.get("hub.challenge") or request.query_params.get(
    #         "hub.verify_token")) is None:
    #     print("Missing required parameters")
    #     raise HTTPException(403, detail="Missing Required Parameters")
    # if request.query_params.get("hub.mode") == "subscribe" and (request.query_params.get("hub.challenge") is not None):
    #     if not request.query_params.get("hub.verify_token") == f"{settings.CALLBACK_VERIFY_TOKEN}":
    #         print("Verification token missmatch")
    #         raise HTTPException(403, detail="Verification token missmatch")
    #     print("Successfully verified")
    #     print(request.query_params['hub.challenge'])
    #     return request.query_params['hub.challenge']
    # print("Error in verifying token")
    # raise HTTPException(400, detail="Error in verifying token")


@router.post("/")
async def fb_web_hook(request: Request, db: Session = Depends(get_db)):
    body = await request.json()
    try:
        if body['object'] == "page":
            for data in body['entry']:

                if 'standby' in data:
                    webhook_standby = data['standby'][0]
                    if webhook_standby is not None and 'message' in webhook_standby:
                        if webhook_standby['message']['text'] == "back" or webhook_standby['message']['text'] == "exit":
                            await take_thread_control(webhook_standby['sender_id'])
                    return

                webhook_event = data['messaging'][0]
                print(webhook_event)

                """
                Fetch The Sender Id
                """
                sender_id = webhook_event['sender']['id']

                print(f"Sender ID is : {sender_id}")

                user = db.query(UserInfo).filter(UserInfo.user_id == sender_id).first()
                if not user:
                    user = UserInfo(id=str(uuid.uuid4()),
                                    user_id=sender_id,
                                    language=LanguageEnum.english)

                    db.add(user)
                    db.commit()
                    db.refresh(user)

                if 'message' in webhook_event:
                    await message_service(sender_id, webhook_event['message'], user.language, db)
                elif 'postback' in webhook_event:
                    await postback_service(sender_id, webhook_event['postback'], user.language, db)
    except Exception as e:
        print("Exception due to : " + str(e))
    return "Event Received"


@router.post("/messenger-app/setup")
async def setup_persistent_menu():
    response = await setup_profile_helper()
    return response
