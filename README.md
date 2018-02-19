# XMPP Chat Badge

Creates a badge linking to an XMPP chat room, like so:

[![inVerse](https://inverse.chat/badge.svg?room=discuss@conference.conversejs.org)](https://inverse.chat/#converse/room?jid=discuss@conference.conversejs.org)

## Installation

    git clone git@github.com:jcbrand/xmpp-chat-badge.git
    virtualenv -p python3 xmpp-chat-badge
    cd xmpp-chat-badge
    pip install -r requirements.txt
    cp config.ini.default config.ini
    # Edit config.ini to add the login details for the bot
    make serve
