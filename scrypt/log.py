import logging, json, pickle
from logging.handlers import SocketHandler

# subprocess


logger = logging.getLogger('logger')
logger.setLevel(logging.INFO)

handler = SocketHandler("ws://localhost", 8828)
handler.setLevel(logging.INFO)

logger.addHandler(handler)
logger.info({'push': 'logger info text'})

logger.removeHandler(handler)
handler.close()

