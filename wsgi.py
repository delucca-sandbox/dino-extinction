"""Dino Extinction WGSI.

This package is responsible for importing all required dependencies to start
a new Dino Extinction server and them doing so.

"""
from gevent.pywsgi import WSGIServer
from dino_extinction import create_app

if __name__ == '__main__':
    app = create_app()
    WSGIServer(('0.0.0.0', 8080), app).serve_forever()
