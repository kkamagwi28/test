import json, os, re, sys
import time
from channels.generic.websocket import WebsocketConsumer
from .views import gitcloner


class WSConsumer(WebsocketConsumer):

    def connect(self):
        self.accept()

        if hasattr(gitcloner, 'clone'):
            self.send(json.dumps({'message': gitcloner.clone}))
        if hasattr(gitcloner, 'clone_exeption'):
            self.send(json.dumps({'message': gitcloner.clone_exeption}))
        if hasattr(gitcloner, 'update'):
            self.send(json.dumps({'message': gitcloner.update}))
        if hasattr(gitcloner, 'updated'):
            self.send(json.dumps({'message': gitcloner.updated}))
        if hasattr(gitcloner, 'updated'):
            self.send(json.dumps({'message': gitcloner.updated}))
        if hasattr(gitcloner, 'done'):
            self.send(json.dumps({'message': gitcloner.done}))
