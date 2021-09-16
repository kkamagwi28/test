import json, os, re, sys
import time
from channels.generic.websocket import WebsocketConsumer
from .views import gitcloner


class WSConsumer(WebsocketConsumer):

    def connect(self):
        self.accept()

        if hasattr(gitcloner, 'clone_info'):
            self.send(json.dumps({'message': gitcloner.clone_info}))
        if hasattr(gitcloner, 'push_info'):
            self.send(json.dumps({'message': gitcloner.push_info}))
        if hasattr(gitcloner, 'update_info'):
            self.send(json.dumps({'message': gitcloner.update_info}))
