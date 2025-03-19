from flask import *
from models import *
from main import db
from flask_login import login_required

wp_1 = Blueprint("WP1_Blue",__name__)

@login_required
@wp_1.route("conversation/<id>/<sender_id>",method = ['GET','POST'])
def conversation_page(id,sender_id):
    """
    Input: id, the id of this conversation
    A conversation page shows
    :REMEMBER: This is the perspective of the sender, which means you are the sender.
    :return: Page that shows the conversation.
    """
    sender_messages = []
    receiver_messages = []
    conversation = db.session.query(Conversation).filter(Conversation.id == id).one()
    messages = db.session.query(Message).filter(Message.conversation_id == id).all()
    for message in messages:
        if(message.sender_id == sender_id):
            sender_messages.append(message)
        else:
            receiver_messages.append(message)
    return render_template("conversation.html",sender_messages = sender_messages,receiver_messages = receiver_messages,
                           conversation = conversation)

@login_required
@wp_1.route("creat_conversation/<sender_id>/<receiver_id>",method = ['GET','POST'])
def creat_conversation_page(sender_id,receiver_id):
    """
    Creat a conversation between two users
    if there already a conversation between them
    System will arise a notation and warn them.
    :param sender_id:
    :param receiver_id:
    :return: redirect to the "all conversation"  page
    """
    conversation = db.session.query(Conversation).filter(Conversation.customer_id == sender_id and Conversation.staff_id == receiver_id).one()
    if(conversation == None):
        conversation = db.session.query(Conversation).filter(Conversation.staff_id == sender_id and Conversation.customer_id == receiver_id).one()
        if(conversation!=None):
            return flash("This conversation already exists!")
        else:
            conversation = Conversation(participant_a_id = sender_id,participant_b_id  = receiver_id)
            # put this new conversation into the db
            db.session.add(conversation)
            db.session.commit()
    else:
        return flash("This conversation already exists!")

    return redirect("my_conversations")

@login_required
@wp_1.route("my_conversations/<sender_id>/",method = ['GET','POST'])
def my_conversations(sender_id):
    """
    This page shows the conversations of a staff
    :REMEMBER: Only STAFF could have this page,
    Normal CUSTOMERS will not have this permissions.
    :param sender_id:
    :return: The page of conversations.
    """
    conversation_list = db.session.query(Conversation).filter(Conversation.staff_id == sender_id).all()

    return render_template("my_conversations.html",conversation_list = conversation_list)

@login_required
@wp_1.route("send_message/<sender_id>/<receiver_id>",method = ['GET','POST'])
def send_message(sender_id,receiver_id):
    """
    send a message from the sender to the receiver
    :param sender_id:
    :param receiver_id:
    :return: Redirect to the original page of the conversation
    """
    if request.method == 'POST':
        content = request.form.get("content")
        message = Message(sender_id = sender_id,receiver_id = receiver_id,content = content)
        db.session.add(message)
        db.session.commit()

