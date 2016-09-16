"""
Data files for blog
"""
from google.appengine.ext import db


class PostData(db.Model):
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    author = db.StringProperty(required=True)
    date = db.DateTimeProperty(auto_now_add=True)
    modified = db.DateTimeProperty(auto_now=True)
    commentsnb = db.IntegerProperty(default=0)
    edited = db.BooleanProperty(default = False)
    addscore = db.IntegerProperty(default=0)
    delscore = db.IntegerProperty(default=0)


class CommentData(db.Model):
    postkey = db.IntegerProperty(required=True)
    author = db.StringProperty(required=True)
    comment = db.TextProperty(required=True)
    date = db.DateTimeProperty(auto_now_add=True)

    @classmethod
    def by_postkey(self, id):
        k = CommentData.all().filter(
            'postkey =', int(id)).order('-date').fetch(100)
        return k


class UserData(db.Model):
    username = db.StringProperty(required=True)
    pw_hash = db.StringProperty(required=True)
    email = db.StringProperty()
    score = db.IntegerProperty(default=0)


    @classmethod
    def by_id(self, uid):
        return UserData.get_by_id(uid)


    @classmethod
    def by_name(self, name):
        data = UserData.all().filter('Username =', name).fetch(1)
        return data