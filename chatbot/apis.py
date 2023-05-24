from apiflask import APIFlask, Schema, abort
from apiflask.fields import Integer, String, Field, DateTime
from apiflask.validators import Length, OneOf

from chatbot import app, db
from chatbot.models import ChatDialog, ChatMessage

"""
app.security_schemes = {
    'ApiKeyAuth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-API-Key',
    }
}
"""

class BaseResponse(Schema):
    data = Field()
    message = String()
    code = Integer()

app.config['BASE_RESPONSE_SCHEMA'] = BaseResponse

class MessageIn(Schema):
    client_id = Integer(required=True, metadata={'description': 'unique id for each client device'})
    chat_name = String(required=True, validate=Length(1,30))
    sender_name = String(required=True)
    message = String(required=True)
    create_time = DateTime(required=False)

class MessageOut(Schema):
    id = Integer()
    message = String()

@app.post('/apichat')
@app.input(MessageIn(partial=True))
@app.output(MessageOut)
def get_reply(data):

    dialog = ChatDialog.search(client_id = data['client_id'], chat_name = data['chat_name'])
    if not dialog:
        dialog = ChatDialog.create(data)
    response = ChatMessage.aichat(dialog.id, data)

    return {
        'data': response,
        'message': 'success',
        'code': 200
    }