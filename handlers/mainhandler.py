# [BEGIN IMPORTS]
import os
import jinja2
import webapp2
from sec.passauth import *
from sec.data import UserData, CommentData, PostData
from google.appengine.ext import db
# [END IMPORTS]


# To link template to app
TEMPLATE_MASTER = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                               'templates')


# to set jinja environment making sure autoescape set to true
JINJA_ENV = jinja2.Environment(
                    loader=jinja2.FileSystemLoader(TEMPLATE_MASTER),
                    autoescape=True)


class MainHandler (webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = JINJA_ENV.get_template(template)
        return t.render(params)

    def user_exists(username):
            username_exists = db.GqlQuery(
                                          "SELECT * "
                                          "FROM UserData "
                                          "WHERE username = :exist",
                                          exist=username).get()

# Main Template render
    def render(self, template, **kw):
        if self.get_user():
            user = self.get_user()
            nav = [
                    ('/', 'Home'),
                    ('/blog/logout', 'Logout'),
                    ('/blog/newpost', 'New Post')
                ]
        else:
            user = ''
            nav = [('/', 'Home'),
                   ('/blog/login', 'Login'),
                   ('/blog/register', 'Sign Up')]
        footer = [('zocial-facebook social-button',
                  'https://www.facebook.com/Inthepurestform',
                   'Facebook'),
                  ('zocial-twitter social-button',
                  'https://twitter.com/',
                   'Twitter'),
                  ('zocial-github social-button',
                  'https://github.com',
                   'Github'),
                  ('zocial-pinterest social-button',
                  'https://www.pinterest.com/',
                   'Pinterest'),
                  ('zocial-linkedin social-button',
                  'https://www.linkedin.com/',
                   'LinkedIn')]
        self.write(self.render_str(template,
                                   user=user,
                                   nav=nav,
                                   footer=footer, **kw))

    def get_user(self):
        cookie = self.request.cookies.get('id')
        if cookie and check_cookie(cookie):
            cookie = int(cookie.split('|')[0])
            x = UserData.get_by_id(cookie).username
            return x

    def get_post(self, keyid):
        key = db.Key.from_path('PostData', int(keyid))
        postkey = db.get(key)
        return postkey

    def get_comment(self, keyid):
        key = db.Key.from_path('CommentData', int(keyid))
        commentkey = db.get(key)
        return commentkey


# Handler for main view
class MainPageHandler (MainHandler):

    # loading main page
    def get(self):
        posts = db.GqlQuery("SELECT * "
                            "FROM PostData "
                            "ORDER BY date DESC")

        comments = db.GqlQuery("SELECT * "
                               "FROM CommentData "
                               "ORDER BY date DESC")

        self.render('mainpage.html', posts=posts, comments=comments)


# handler related to errors
class ErrorHandler(MainHandler):

    def get(self):
        self.redirect('/blog')
