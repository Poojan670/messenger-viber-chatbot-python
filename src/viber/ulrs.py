from fastapi import APIRouter, Request, HTTPException
from fastapi.logger import logger
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages import TextMessage
from viberbot.api.viber_requests import ViberMessageRequest, ViberSubscribedRequest, ViberFailedRequest, \
    ViberConversationStartedRequest

from src.core.config import settings

router = APIRouter()

bot_configuration = BotConfiguration(
    name=settings.VIBER_BOT_NAME,
    avatar='https://avatars.githubusercontent.com/u/53387833?v=4',
    auth_token=settings.VIBER_AUTH_TOKEN
)
viber = Api(bot_configuration)


@router.post("/viber-app/setup")
def setup_webhook():
    viber.unset_webhook()
    viber.set_webhook(settings.WEBHOOK_SERVER_URL)
    return "Webhook setup successfully"


@router.post('/viber-app/')
async def incoming(request: Request):
    data = await request.body()
    logger.debug("received request. post data: {0}".format(data))
    # every viber message is signed, you can verify the signature using this method
    if not viber.verify_signature(data, request.headers.get('X-Viber-Content-Signature')):
        return HTTPException(403, detail={"msg": "Signature didn't match"})

    # this library supplies a simple way to receive a request object
    viber_request = viber.parse_request(data)

    if isinstance(viber_request, ViberMessageRequest):
        message = viber_request.message
        # lets echo back
        viber.send_messages(viber_request.sender.id, [
            message
        ])
    elif isinstance(viber_request, ViberSubscribedRequest):
        viber.send_messages(viber_request.user.id, [
            TextMessage(text="thanks for subscribing!")
        ])

    elif isinstance(viber_request, ViberConversationStartedRequest):
        viber.send_messages(viber_request.user.id, [
            TextMessage(text="Thank you for starting conversation with me")
        ])
    elif isinstance(viber_request, ViberFailedRequest):
        logger.warn("client failed receiving message. failure: {0}".format(viber_request))

    return 'ok'
