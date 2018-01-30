#!/usr/bin/env python
# -*- coding: utf-8 -*-



import sys
import logging
import getpass
from optparse import OptionParser
from flask import Flask

import sleekxmpp


app = Flask(__name__)

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

    def __init__(self, jid, password, room, nick):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)

        self.room = room
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

    def get_number_of_occupants(self):
        querying_jid = '{}/{}'.format(self.room, self.nick)
        result = self.plugin['xep_0030'].get_info(
            jid=self.room,
            node=None,
            cached=True,
            ifrom=querying_jid,
            block=True,
            timeout=10
        )
        fields = result.xml.find(
                '{http://jabber.org/protocol/disco#info}query').find(
                '{jabber:x:data}x').findall(
                '{jabber:x:data}field')

        for field in fields:
            if field.get('var') == 'muc#roominfo_occupants':
                return field.find('{jabber:x:data}value').text
        return 'unknown'


def initBOT(jid, password, room, nick):
    # Set up the MUCBot and register plugins. Note that while plugins may
    # have interdependencies, the order in which you register them does
    # not matter.
    xmpp_client = MUCBot(jid, password, room, nick)
    xmpp_client.register_plugin('xep_0030') # Service Discovery
    return xmpp_client


if __name__ == '__main__':
    # Set up the command line arguments.
    optp = OptionParser()

    # Output verbosity options.
    optp.add_option('-q', '--quiet', help='set logging to ERROR',
                    action='store_const', dest='loglevel',
                    const=logging.ERROR, default=logging.INFO)
    optp.add_option('-d', '--debug', help='set logging to DEBUG',
                    action='store_const', dest='loglevel',
                    const=logging.DEBUG, default=logging.INFO)
    optp.add_option('-v', '--verbose', help='set logging to COMM',
                    action='store_const', dest='loglevel',
                    const=5, default=logging.INFO)

    # room-occupants-query-bot
    # aRie9boh

    # JID and password options.
    optp.add_option("-j", "--jid", dest="jid",
                    help="JID to use")
    optp.add_option("-p", "--password", dest="password",
                    help="password to use")
    optp.add_option("-r", "--room", dest="room",
                    help="MUC room to join")
    optp.add_option("-n", "--nick", dest="nick",
                    help="MUC nickname")

    opts, args = optp.parse_args()

    # Set up logging.
    logging.basicConfig(level=opts.loglevel,
                        format='%(levelname)-8s %(message)s')

    if opts.jid is None:
        opts.jid = raw_input("Username: ")
    if opts.password is None:
        opts.password = getpass.getpass("Password: ")
    if opts.room is None:
        opts.room = raw_input("MUC room: ")
    if opts.nick is None:
        opts.nick = raw_input("MUC nickname: ")

    xmpp_client = initBOT(opts.jid, opts.password, opts.room, opts.nick)
    # Connect to the XMPP server and start processing XMPP stanzas.
    if xmpp_client.connect():
        xmpp_client.process(block=True)
        print("Done")
    else:
        print("Unable to connect.")

# TODO: enable caching for SleekXMPP
# TODO: figure out how to make sure get_number_of_occupants is only called after initialization
# TODO: figure out how to disconnect/cleanup nicely

bot = initBOT('room-occupants-query-bot@conversejs.org', 'aRie9boh', 'discuss@conference.conversejs.org', 'botticelli')
bot.connect()
bot.process(block=False)

@app.route("/")
def hello():
    return bot.get_number_of_occupants()
