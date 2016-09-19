# [BEGIN IMPORTS]
from sec.data import *
from mainhandler import MainHandler
# [END IMPORTS]


# Handler for new comments
class AddCommentHandler (MainHandler):
# initilization of post for less code
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
                self.redirect('/blog/%s' % post_id)

        else:
            error = "Auth error"
            self.render('mainpage.html', error=error)


# Handler for comment edits not working yet

class EditCommentHandler(MainHandler):

    def init(self):
        # grabbing ID from url
        comment_id = self.request.get('comment_id')
        post_id = self.request.get('post_id')

        # finding specific data by id
        post = self.get_post(post_id)
        pcomment = CommentData.get_by_id(int(comment_id))

        username = self.get_user()
        return post_id, pcomment, username

    # render add auth
    def get(self):
        post, pcomment, username = self.init()
        if username == pcomment.author:
                self.render('editcomment.html',
                            post=post,
                            comment=pcomment.comment,
                            username=username,
                            error="Editing..")
        else:
            error = "Please Sign In or Log out..."
            self.render('mainpage.html', error=error)

    def post(self):
        post, pcomment, username = self.init()
        # add auth
        comment = self.request.get('comment')
        if comment.strip() == '':
            error = "You cant make a comment blank.."
            self.render('editcomment.html',
                        post=post,
                        comment=comment,
                        error=error)

        elif username == pcomment.author:
            pcomment.comment = comment
            pcomment.put()
            self.redirect('/')
        else:
            self.redirect('/')


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
