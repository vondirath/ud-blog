"""
Password and Authentication
"""

# [BEGIN IMPORTS]
import random
import string
import hashlib
import hmac
import re
from string import letters
# [END IMPORTS]

# secure code
COOKIE_SEC = "4785074604081152"


def make_salt(length=5):
    """this creates salt for a hashed password using imported random"""
    return ''.join(random.choice(letters) for x in xrange(length))


def make_pw_hash(name, password, salt=None):
    """creates the hash using sha256 """
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + password + salt).hexdigest()
    return '%s|%s' % (salt, h)


def check_pw(name, password, h):
    salt = h.split('|')[0]
    return h == make_pw_hash(name, password, salt)


def hash_cookie(id):
    return hmac.new(COOKIE_SEC, id).hexdigest()


def encode_cookie(id):
    return "%s|%s" % (id, hash_cookie(id))


def check_cookie(cookieval):
    temp = cookieval.split('|')[0]
    return cookieval == encode_cookie(temp)


# regex matching
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
