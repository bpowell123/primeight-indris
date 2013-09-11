from gaesessions import SessionMiddleware
#from google.appengine.dist import use_library
#use_library('django', '1.2')

def webapp_add_wsgi_middleware(app):
    app = SessionMiddleware(app, cookie_key="646f77686974206279207072696d6569676874")
    return app