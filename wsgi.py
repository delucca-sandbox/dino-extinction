"""Dino Extinction WGSI.

This package is responsible for importing all required dependencies to start
a new Dino Extinction server and them doing so.

"""
from gevent.pywsgi import WSGIServer
from dino_extinction import create_app

if __name__ == '__main__':
    default_port = 8080
    app = create_app()
    server = WSGIServer(('0.0.0.0', default_port), app)

    art_file = open('ascii.txt')
    art = art_file.read()
    print(f"\033[92m{art}")
    print(f"\033[94m\033[1m===> Server up and running on port {default_port}\033[0m")
    server.serve_forever()
