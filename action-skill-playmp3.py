#!/usr/bin/env python3.7

from snipsTools import SnipsConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import io
import subprocess

CONFIG_INI = "config.ini"

MQTT_IP_ADDR: str = "localhost"
MQTT_PORT: int = 1883
MQTT_ADDR: str = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))
def play_mp3(path):
    subprocess.Popen(['mpg123', '-q', path]).wait()

class playMP3(object):

    def __init__(self):
        try:
            self.config = SnipsConfigParser.read_configuration_file(CONFIG_INI)
        except Exception:
            self.config = None

        self.start_blocking()

    def execplaymp3_callback(self, hermes, intent_message):

        if intent_message.slots.playmp3:
            intent=intent_message.slots.playmp3.first().value
            if intent == "four what" or intent == "for what" or intent == "fo what":
                play_mp3('/media/turndownforwhat.mp3')
                hermes.publish_end_session(intent_message.session_id, "")
            elif intent == "goodbye" or intent == "good bye" or intent == "good by":
                play_mp3('/media/byenow.mp3')
                hermes.publish_end_session(intent_message.session_id, "")
            elif intent == "congratulate" or intent == "congratulations":
                play_mp3('/media/ohgoodforyou.mp3')
                hermes.publish_end_session(intent_message.session_id, "")

    def master_intent_callback(self,hermes, intent_message):
        coming_intent = intent_message.intent.intent_name
        if coming_intent == 'hooray4me:playmp3':
            self.execplaymp3_callback(hermes, intent_message)

    def start_blocking(self):
        with Hermes(MQTT_ADDR) as h:
            h.subscribe_intents(self.master_intent_callback).start()

if __name__ == "__main__":
    playMP3()
