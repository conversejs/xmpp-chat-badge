#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from flask import Flask
from flask import abort
from flask import make_response
from flask import render_template
from flask import request
import sleekxmpp

app = Flask(__name__)
app.config.from_envvar("XMPP_CHAT_BADGE_CONFIG")


# Python versions before 3.0 do not use UTF-8 encoding
# by default. To ensure that Unicode is handled properly
# throughout SleekXMPP, we will set the default encoding
# ourselves to UTF-8.
if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf8')
else:
    raw_input = input


class MUCBot(sleekxmpp.ClientXMPP):
    """ """

    def __init__(self, jid, password, nick):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)
        self.nick = nick
        # The session_start event will be triggered when
        # the bot establishes its connection with the server
        # and the XML streams are ready for use. We want to
        # listen for this event so that we we can initialize
        # our roster.
        self.add_event_handler("session_start", self.start)


    def start(self, event):
        """
        Process the session_start event.

        Typical actions for the session_start event are
        requesting the roster and broadcasting an initial
        presence stanza.

        Arguments:
            event -- An empty dictionary. The session_start
                     event does not provide any additional
                     data.
        """
        self.get_roster()
        self.send_presence()

    def get_number_of_occupants(self, room):
        querying_jid = '{}/{}'.format(room, self.nick)
        try:
            result = self.plugin['xep_0030'].get_info(
                jid=room,
                node=None,
                cached=True,
                ifrom=querying_jid,
                block=True,
                timeout=10
            )
        except sleekxmpp.exceptions.IqError:
            return None

        fields = result.xml.find(
                '{http://jabber.org/protocol/disco#info}query').find(
                '{jabber:x:data}x').findall(
                '{jabber:x:data}field')

        for field in fields:
            if field.get('var') == 'muc#roominfo_occupants':
                return field.find('{jabber:x:data}value').text
        return None


def initBOT(jid, password, nick):
    # Set up the MUCBot and register plugins. Note that while plugins may
    # have interdependencies, the order in which you register them does
    # not matter.
    xmpp_client = MUCBot(jid, password, nick)
    xmpp_client.register_plugin('xep_0030') # Service Discovery
    return xmpp_client


bot = initBOT(app.config['JID'], app.config['PASSWORD'], app.config['NICK'])
bot.connect()
bot.process(block=False)

@app.route("/badge.svg")
def hello():
    room = request.args.get('room')
    if room is None:
        return abort(400)
    number = bot.get_number_of_occupants(room)
    svg = render_template('badge.svg', number=number)
    response = make_response(svg)
    response.content_type = 'image/svg+xml'
    response.cache_control.max_age = 60
    return response
