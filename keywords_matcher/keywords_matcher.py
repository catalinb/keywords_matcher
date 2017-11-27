from flask import Flask
import ahocorasick
import sys
import os

class KeywordsMatcher(Flask):
    def __init__(self):
        Flask.__init__(self, __name__,
                        instance_path=os.getcwd(),
                        instance_relative_config=True)
        self.phrases = []
        self.automaton = None


    def load_phrases(self, phrases_path):
        with self.open_instance_resource(phrases_path, 'rt') as f:
            content = f.readlines()

        self.automaton = ahocorasick.Automaton()
        self.phrases = [x.rstrip() for x in content]
        for phrase in self.phrases:
            self.automaton.add_word(phrase, (phrase))
        self.automaton.make_automaton()


def create_app():
    app = KeywordsMatcher()

    # default settings
    app.config.update(dict(
        PORT=8080,
        DEBUG=True,
        PHRASES_PATH='data/phrases'
    ))
    app.config.from_envvar('KMATCHER_SETTINGS', silent=True)
    return app
