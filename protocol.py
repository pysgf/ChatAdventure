"this is the simple network protocol we will use"

import re

HELLO = "HELLO {name} {key}\n"
HELLO_RE = re.compile("^HELLO (?P<name>\w+) (?P<key>\w+)\n$")

BYE = "BYE {key}\n"
BYE_RE = re.compile("^BYE (?P<key>\w+)\n$")

MESSAGE = "SAY {key} {message}\n"
MESSAGE_RE = re.compile("^SAY (?P<key>\w+) (?P<message>\w+)\n$")

