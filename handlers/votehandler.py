# [BEGIN IMPORTS]
from mainhandler import MainHandler
from sec.data import *
# [END IMPORTS]


class UpVoteHandler (MainHandler):

    def get(self):
        user = self.get_user()
        if user:
            post_id = self.request.get('post_id')
            post = PostData.get_by_id(int(post_id))

            voter_list = post.voter_list

            if post.author == user:
                error = "cant vote for self"
                self.render('mainpage.html', error=error)
            elif user in voter_list:
                error = "cant vote twice"
                self.render('mainpage.html', error=error)
            else:
                post.upscore += 1
                voter_list.append(user)
                post.put()
                self.redirect('/blog/' + post_id)
        else:
            self.redirect('/')


class DownVoteHandler (MainHandler):

    def get(self):
        user = self.get_user()
        if user:
            post_id = self.request.get('post_id')
            post = PostData.get_by_id(int(post_id))

            voter_list = post.voter_list

            if post.author == user:
                error = "cant vote for self"
                self.render('mainpage.html', error=error)
            elif user in voter_list:
                error = "cant vote twice"
                self.render('mainpage.html', error=error)
            else:
                post.downscore += 1
                voter_list.append(user)
                post.put()
                self.redirect('/blog/' + post_id)
        else:
            self.redirect('/')
