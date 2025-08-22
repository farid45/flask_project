"""app flask"""


from flask import Flask


def create_app():
    """функция создания приложения"""
    app = Flask(__name__)
    return app
