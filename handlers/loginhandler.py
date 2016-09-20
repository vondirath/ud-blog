# [BEGIN IMPORTS]
from sec.data import *
from sec.passauth import *
from mainhandler import MainHandler
from google.appengine.ext import db
# [END IMPORTS]


def user_exists(username):
    """ this will search database for an existing user"""
    username_exists = db.GqlQuery("SELECT * "
                                  "FROM UserData "
                                  "WHERE username = :exist",
                                  exist=username).get()
    return username_exists


def user_auth(username, password):
    user = db.GqlQuery("SELECT * "
                       "FROM UserData "
                       "WHERE username = :exist",
                       exist=username).get()
    if user:
        return check_pw(user.username,
                        password,
                        user.pw_hash)


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

        if user_exists(username):
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

        if user_exists(username):
            have_error = False
            if user_auth(username, password):
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
        self.redirect('/')
