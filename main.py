# [START IMPORTS]

# for templating
import os
import jinja2

# for google appengine
import webapp2
from google.appengine.ext import db

# local imports
from sec.passauth import *
from sec.data import *

# To link template to app
TEMPLATE_MASTER = os.path.join(os.path.dirname(__file__), 'templates')
# to set jinja environment making sure autoescape set to true
JINJA_ENV = jinja2.Environment(
                    loader=jinja2.FileSystemLoader(TEMPLATE_MASTER),
                    autoescape=True)

# [END IMPORTS]


def render_str(template, **params):
    t = JINJA_ENV.get_template(template)
    return t.render(params)

def user_exists(username):
        username_exists = db.GqlQuery(
                                      "SELECT * "
                                      "FROM UserData "
                                      "WHERE username = :exist",
                                      exist=username).get()
# Main Handler for all pages extends index.html handles rendering pages
class MainHandler (webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

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
        self.write(render_str(template,
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

    def user_exists(self, username):
        username_exists = db.GqlQuery("SELECT * "
                                      "FROM UserData "
                                      "WHERE username = :exist",
                                      exist=username).get()
        return username_exists

    def user_auth(self, username, password):
        user = db.GqlQuery("SELECT * "
                           "FROM UserData "
                           "WHERE username = :exist",
                           exist=username).get()
        if user:
            return check_pw(user.username,
                            password,
                            user.pw_hash)


"""
This section is for page views
"""


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



"""
This section is related to user auth
"""

# handler for registering
class RegisterHandler (MainHandler):

    def get(self):
        if self.get_user():
            error = "You are logged in"
            self.render('mainpage.html', error=error)
        else:
            self.render('signup-form.html')

# regex check for signup
    def valid_username(self, username):
        return username and USER_RE.match(username)

    def valid_password(self, password):
        return password and PASS_RE.match(password)

    def valid_email(self, email):
        return not email or EMAIL_RE.match(email)

    def post(self):
        have_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

# dictionary to store username and email if error
        params = dict(username=username, email=email)

        if self.user_exists(username):
            params['error_username'] = 'User Exists'
            have_error = True

        elif not self.valid_username(username):
            params['error_username'] = "That's not a valid username."
            have_error = True

        if not self.valid_password(password):
            params['error_password'] = "That wasn't a valid password."
            have_error = True

        elif password != verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if not self.valid_email(email):
            params['error_email'] = "That's not a valid email."
            have_error = True

        if have_error is True:
            self.render('signup-form.html', **params)
        else:
            hpass = make_pw_hash(username, password)
            u = UserData(username=username, pw_hash=hpass)
            u.put()
            key = str(u.key().id())
            cookie = encode_cookie(key)
            self.response.headers.add_header(
                                             'Set-Cookie',
                                             'id=%s; Path=/' % cookie)
            self.redirect('/')


# handler for logging in
class LoginHandler (MainHandler):

    def get(self):
        if self.get_user():
            error = "Logged in"
            self.render('mainpage.html', error=error)
        else:
            self.render('login-form.html')

    def post(self):
        have_error = True
        username = self.request.get('username')
        password = self.request.get('password')
        check_name = UserData.by_name(username)
        params = dict(username=username)

        if self.user_exists(username):
            have_error = False
            if self.user_auth(username, password):
                have_error = False
            else:
                have_error = True
                params['error_password'] = 'Invalid Password'
        else:
            have_error = True
            params['error_username'] = 'User does not exist'

        if have_error:
            # deletes cookie if failed login
            self.response.headers.add_header('Set-Cookie', 'id=; Path=/')
            self.render('login-form.html', **params)

        else:
            user = db.GqlQuery("SELECT * "
                               "FROM UserData "
                               "WHERE username = :exist",
                               exist=username).get()
            user_id = str(user.key().id())
            cookie = encode_cookie(user_id)
            self.response.headers.add_header(
                                             'Set-Cookie',
                                             'id=%s; Path=/' % cookie)
            self.redirect('/')


# Handler for logging out
class LogoutHandler(MainHandler):

    def get(self):
        self.response.headers.add_header('Set-Cookie', 'id=; Path=/')
        error = "Logged Out"
        self.render('mainpage.html', error=error)

"""
This section is related to creating or modifying posts
"""


# Handler for new posts
class NewPostHandler (MainHandler):

    def get(self):
        mode = self.request.get('mode')
        username = self.get_user()
        if username:
            self.render('postform.html', username=username)
        else:
            error = "Please Login"
            self.render('mainpage.html', error=error)

    def post(self):
        username = self.get_user()
        if username:
            subject = self.request.get('subject')
            content = self.request.get('content')
            mode = self.request.get('mode')
        else:
            error = "Please Login"
            self.render('mainpage.html', error=error)
        if subject and content:
            # makes sure spaces are not entered as comments...
            if subject.strip() == '' or content.strip() == '':
                mode = 'newpost'
                post_error = "Comments cannot be blank"
                self.render('postform.html',
                            subject=subject,
                            content=content,
                            post_error=post_error,
                            mode=mode)
            else:
                p = PostData(
                             subject=subject,
                             content=content,
                             author=username)
                p.put()
                key = p.key().id()
                self.redirect('/blog/%s' % str(key))
        else:
            mode = "newpost"
            post_error = "You are missing something"
            self.render('postform.html',
                        subject=subject,
                        content=content,
                        post_error=post_error,
                        mode=mode)


# handler for a single post
class ViewPostHandler (MainHandler):

    def init(self, keyid):
        username = self.get_user()
        post = self.get_post(keyid)
        return username, post

    def get(self, keyid):
        username, post = self.init(keyid)
        if post:
            if username:
                comments = CommentData.by_postkey(keyid)
                score_status = self.request.get('score_status')
                error = ''
                self.render('viewpost.html',
                            post=post,
                            username=username,
                            comments=comments,
                            score_status=score_status,
                            error=error)
            else:
                error = "Please Sign In"
                self.render('signup-form.html', error=error)
        else:
            error = "Please Sign In"
            error = "Post does not exist.."
            self.render('mainpage.html', error=error)

    def post(self, keyid):
        username, post = self.init(keyid)
        if username:
            self.redirect('/blog/edit?post_id=' + str(post.key().id()))

        else:
            error = "Please Sign In"
            self.render('signup-form.html', error=error)


# Handler for post edits
class EditPostHandler (MainHandler):

    def init(self):
        username = self.get_user()
        keyid = self.request.get('post_id')
        post = self.get_post(keyid)
        return post, keyid, username

    def get(self):
        post, keyid, username = self.init()
        if username == post.author:
                self.render('editpost.html',
                            subject=cject,
                            content=post.content,
                            username=username)
        else:
            error = "Please Sign In or Log out..."
            self.render('mainpage.html', error=error)

    def post(self):
        post, keyid, username = self.init()

        if username:
            if post.author == username:
                subject = self.request.get('subject')
                content = self.request.get('content')
                if subject.strip() == '' or content.strip() == '':
                    mode = 'newpost'
                    post_error = "You are missing something..."
                    self.render('postform.html',
                                subject=subject,
                                content=content,
                                post_error=post_error,
                                mode=mode)
                else:
                    post.subject = subject
                    post.content = content
                    post.edited = True
                    post.put()
                    self.redirect('/blog/' + str(keyid))
            else:
                error = "Please Log in..."
                self.redirect('/blog', error=error)
        else:
            error = "Please Log in..."
            self.redirect('/blog', error=error)


# Handler for Deleting posts
class DeletePostHandler (MainHandler):
    # redirects if someone else tries to access delete
    def get(self, post_id):
        error = "Not authorized"
        self.render('mainpage.html', error=error)

    def post(self, post_id):
        post = self.get_post(post_id)
        username = self.get_user()
        key = db.Key.from_path('PostData', int(post_id))

        # redirects if not authorized for post
        if self.get_user() == post.author:

            # deletes post and any comments associated with the post
            db.delete(CommentData.by_postkey(str(post_id)))
            db.delete(key)
            self.redirect('/')

        else:
            error = "You are not authorized.."
            self.redirect('/blog/login', error=error)


"""
This section is related to creating or modifying comments
"""


# Handler for new comments
class AddCommentHandler (MainHandler):
    def init(self):
        post_id = self.request.get('post_id')
        post = self.get_post(post_id)
        username = self.get_user()
        return post_id, post, username

    def get(self):
        post_id, post, username = self.init()
        # auth for valid post
        if post:

            # auth for valid login
            if username:
                self.render("commentform.html",
                            post=post,
                            username=username)

            else:
                error = "Please Log In..."
                self.render("mainpage.html", error=error)

        else:
            error = "There is no post to comment on.."
            self.render('mainpage.html', error=error)

    def post(self):
        post_id, post, username = self.init()
        mode = self.request.get('mode')
        if username:
            comment = self.request.get('comment')
        else:
            error = "Please Log In..."
            self.render('mainpage.html', error=error)

        if mode == 'newcomment':

            # checks and makes sure comment input is not empty
            if comment.strip() == '':
                mode = 'newpost'
                error = "You are missing something..."
                self.render('commentform.html', post=post, error=error)

            else:
                comment = CommentData(postkey=int(post_id),
                                      author=username,
                                      comment=comment)
                comment.put()
                post = self.get_post(post_id)
                post.commentsnb += 1
                post.put()
                self.redirect('/blog/%s' % post_id)

        else:
            error = "Auth error"
            self.render('mainpage.html', error=error)


# Handler for comment edits not working yet

class EditCommentHandler(MainHandler):
    def get(self, comment_id):
        username = self.get_user()
        comment = self.get_comment(comment_id)
        if username == comment.author:
                self.render('editcomment.html',
                            comment=comment.comment,
                            username=username)
        else:
            error = "Please Sign In or Log out..."
            self.render('mainpage.html', error=error)
# is copying posts not editing
    def post(self, comment_id):
        comment = self.get_comment(comment_id)
        username = self.get_user()
        key = db.Key.from_path('CommentData', int(comment_id))
        if self.get_user() == comment.author:
            if comment.comment.strip() == '':
                error = "You cant make a comment blank.."
                self.render('commentform.html', post=post, comment=comment)
            else:
                comment = CommentData(author=comment.author,
                                      comment=comment.comment,
                                      postkey=comment.postkey)
                comment.put()
                self.redirect('/')
        else:
            error = "Not authorized to edit this comment"
            self.render('.mainpage.html', error = error)

# Handler for deleting comments
class DeleteCommentHandler (MainHandler):

    def get(self):
        error = "Not authorized"
        self.render('mainpage.html', error=error)

    def post(self, comment_id):
        comment = self.get_comment(comment_id)
        username = self.get_user()
        key = db.Key.from_path('CommentData', int(comment_id))
        if self.get_user() == comment.author:
            db.delete(key)
            self.redirect('/')
        else:
            error = "You are not authorized.."
            self.redirect('/blog/login', error=error)

app = webapp2.WSGIApplication([('/',
                                ErrorHandler),
                               ('/blog',
                               MainPageHandler),
                               ('/blog/newpost',
                               NewPostHandler),
                               ('/blog/([0-9]+)',
                               ViewPostHandler),
                               ('/blog/edit',
                               EditPostHandler),
                               ('/blog/delete-([0-9]+)',
                               DeletePostHandler),
                               ('/blog/comment',
                               AddCommentHandler),
                               ('/blog/editcomment',
                               EditCommentHandler),
                               ('/blog/deletecomment-([0-9]+)',
                               DeleteCommentHandler),
                               ('/blog/register',
                               RegisterHandler),
                               ('/blog/login',
                               LoginHandler),
                               ('/blog/logout',
                               LogoutHandler)
                               ], debug=True)
