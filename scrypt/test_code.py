# import json
# import time
# from channels.generic.websocket import WebsocketConsumer
# from asgiref.sync import async_to_sync
#
#
# class WSConsumer(WebsocketConsumer):
#
#     def connect(self):
#         self.channel_layer.group_add("push", self.channel_name)
#         self.accept()
#         self.send(json.dumps({'message': str(self.scope)}))
#         time.sleep(5)
#         self.send(json.dumps({'message': 'str(self.scope)'}))
#
#     def disconnect(self, close_code):
#         self.channel_layer.group_discard("push", self.channel_name)
#
#     def receive(self, text_data):
#         print('td', text_data)
#         async_to_sync(self.channel_layer.group_send)(
#             "push",
#             {
#                 "type": "logger.info",
#                 "text": text_data,
#             },
#         )
#
#     def send_text(self, event):
#         self.send(text_data=event["text"])
