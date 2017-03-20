from flask import Flask, request, session
from flask_socketio import SocketIO, Namespace, emit, disconnect

from models import Chat


class MyNamespace(Namespace):
    def on_my_event(self, message):
        emit('my_response', {'data': message['data']})
        try:
            current_user = session['username']
        except KeyError:
            current_user = 'anonymous'
        submit_db = Chat(current_user, message['data'])
        Chat.insert(submit_db)

    def on_connect(self):
        emit('my_response', {'data': 'Connected!'})
        print('Client connected', request.sid)

    def on_disconnect(self):
        print('Client disconnected', request.sid)
