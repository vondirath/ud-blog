# [BEGIN IMPORTS]
from sec.data import *
from mainhandler import MainHandler
# [END IMPORTS]


# Handler for new posts
class NewPostHandler (MainHandler):
    """This is the handler for a new post it uses the mainhandler render to create a page"""
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
            # makes sure spaces are not entered as comments
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
    """initializes a post view where a bulk of the edit and comment features are located"""
    def init(self, keyid):
        username = self.get_user()
        post = self.get_post(keyid)
        return username, post

    def get(self, keyid):
        username, post = self.init(keyid)
        if post:
            if username:
                comments = CommentData.by_postkey(keyid)
                score = self.request.get('score')
                error = ''
                self.render('viewpost.html',
                            post=post,
                            username=username,
                            comments=comments,
                            score=score,
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
    """ 
    takes post info and compares users for authorization
    will make sure posts injected content is included    
    """
    def init(self):
        username = self.get_user()
        keyid = self.request.get('post_id')
        post = self.get_post(keyid)
        return post, keyid, username

    def get(self):
        post, keyid, username = self.init()
        if username == post.author:
                self.render('editpost.html',
                            subject=post.subject,
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
    """will take page in and make sure someone is not trying 
    to access a post they are not authorized to modify"""
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
