# [START IMPORTS]
import webapp2
from google.appengine.ext import db
from handlers.loginhandler import (RegisterHandler,
LoginHandler, LogoutHandler )
from handlers.mainhandler import (MainHandler,
MainPageHandler, ErrorHandler)
from handlers.votehandler import (UpVoteHandler,
DownVoteHandler)
from handlers.posthandler import (NewPostHandler,
ViewPostHandler, EditPostHandler, DeletePostHandler)
from handlers.commenthandler import (AddCommentHandler,
EditCommentHandler, DeleteCommentHandler)
# [END IMPORTS]

# This app was created by Thomas Lopez and can be contacted at vondirath@gmail.com

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
                               LogoutHandler),
                               ('/blog/upvote',
                               UpVoteHandler),
                               ('/blog/downvote',
                               DownVoteHandler)
                               ], debug=True)
