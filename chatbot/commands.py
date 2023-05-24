import click 

from chatbot import app, db
from chatbot.models import User, ChatMessage

"""command line to create/drop current database"""
@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop')
def initdb(drop):
    """Initialize the database"""
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database')

"""command line to create admin account"""
@app.cli.command()
@click.option('--username', prompt=True, help="Enter Username")
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='Enter your Password')
def admin(username, password):
    db.create_all()

    user = User.query.first()
    if user is not None:
        click.echo('Updating user...')
        user.username = username
        user.set_password(password)
    else:
        click.echo('Creating user...')
        user = User(username=username, name='Admin')
        user.set_password(password)
        db.session.add(user)

    db.session.commit()
    click.echo('Done.')

@app.cli.command()
def forge():
    """fake data"""
    db.create_all()

    messages = [
        {'conversation_id' : 'JSdfiwoenfsdfkj12102393', 'conversation_name' : '三人组', 'sender_name' : '老三', 'receiver_name' : '浪潮机器人', 'message': f"""@浪潮机器人 介绍一下你自己"""},
        {'conversation_id' : 'JSdfiwoenfsdfkj12102334', 'conversation_name' : '三人组', 'sender_name' : '浪潮机器人', 'receiver_name' : '老三', 'message': f"""好的"""},
        {'conversation_id' : 'JSdfiwoenfsdfkj12102395', 'conversation_name' : '三人组', 'sender_name' : '老三', 'receiver_name' : '浪潮机器人', 'message': f"""@浪潮机器人 介绍一下你自己"""},
        {'conversation_id' : 'JSdfiwoenfsdfkj12102396', 'conversation_name' : '三人组', 'sender_name' : '浪潮机器人', 'receiver_name' : '老三', 'message': f"""我不想"""}
    ]

    for m in messages:
        conversation = ChatMessage(conversation_id=m['conversation_id'], conversation_name=m['conversation_name'], sender_name=m['sender_name'], receiver_name=m['receiver_name'], message=m['message'])
        db.session.add(conversation)
    
    db.session.commit()
    click.echo('Done.')