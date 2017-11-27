import os
import unittest
import tempfile
import json
from keywords_matcher import app
from contextlib import closing

class KeywordsMatcherTestBase(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.app.testing = True
        self.client = app.test_client()

        fd, self.path = tempfile.mkstemp()
        with closing(os.fdopen(fd, 'w')) as file:
            file.write("keyword1\nkeyword2\n")
        app.load_phrases(self.path)


    def tearDown(self):
        os.unlink(self.path)


    def test_simple_match(self):
        rv = self.client.get('/parse', query_string=dict(text='keyword1abcd'))
        self.assertEqual(rv.status_code, 200)
        result = json.loads(rv.data)
        self.assertEqual(result['phrases'], ['keyword1'])


    def test_not_found(self):
        rv = self.client.get('/not_found')
        self.assertEqual(rv.status_code, 404)


    def test_missing_query_parameter(self):
        rv = self.client.get('/parse')
        self.assertEqual(rv.status_code, 400)


    def test_unicode_query(self):
        rv = self.client.get('/parse', query_string=dict(text='hiçŒ«'))
        self.assertEqual(rv.status_code, 200)


    def test_empty_query(self):
        rv = self.client.get('/parse', query_string=dict(text=''))
        self.assertEqual(rv.status_code, 200)
        result = json.loads(rv.data)
        self.assertEqual(result['phrases'], [])


if __name__ == "__main__":
    unittest.main()
