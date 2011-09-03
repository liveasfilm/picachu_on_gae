from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
from google.appengine.api import channel
from google.appengine.ext.webapp import template

canvas_width = 640;
canvas_height = 480;
pica_width = 64;
pica_height = 64;
position_x = canvas_width / 2 - pica_width / 2;
position_y = canvas_height / 2 - pica_height / 2;

class MainPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
            return
        token = channel.create_channel(user.user_id())
        template_values = {'token': token,
                           'canvas_width': canvas_width,
                           'canvas_height': canvas_height,
                           'init_x': position_x,
                           'init_y': position_y }
        self.response.out.write(template.render('index.html', template_values))


class ProcessKey(webapp.RequestHandler):
    def post(self):
        global position_x
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
            return
        key_name = self.request.get('key')
        if key_name == '1':
            position_x -= 10
        if key_name == '5':
            position_x += 10            
        channel.send_message(user.user_id(), '%d' % position_x)


application = webapp.WSGIApplication([('/', MainPage),
                                      ('/process_key', ProcessKey)], debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
