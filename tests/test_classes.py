import configparser
import os
import unittest
import pytest
from tinydb import TinyDB, Query, storages
from goldfinchsong.cli import parse_configuration
from goldfinchsong.classes import Manager


class MockManagerAPI:

    def update_with_media(self, image, text):
        pass


class ManagerTests(unittest.TestCase):

    def test_bad_send_tweet(self):
        config_parser = configparser.ConfigParser()
        config_parser.optionxform = str
        config_parser.read('tests/goldfinchsong.ini')
        active_configuration = parse_configuration(config_parser)
        credentials = active_configuration['credentials']
        text_conversions = active_configuration['text_conversions']
        db = TinyDB(storage=storages.MemoryStorage)
        manager = Manager(credentials, db, active_configuration['image_directory'], text_conversions)
        with pytest.raises(Exception):
            manager.content = None
            manager.post_tweet()

    def test_tweet_insert_into_db(self):
        config_parser = configparser.ConfigParser()
        config_parser.optionxform = str
        config_parser.read('tests/goldfinchsong.ini')
        active_configuration = parse_configuration(config_parser)
        credentials = active_configuration['credentials']
        text_conversions = active_configuration['text_conversions']
        try:
            db = TinyDB(active_configuration['db_location'])
            manager = Manager(credentials, db, active_configuration['image_directory'], text_conversions)
            manager.api = MockManagerAPI()
            manager.post_tweet()
            tweets = db.all()
            self.assertEqual(len(tweets), 1)
        finally:
            if os.path.isfile(active_configuration['db_location']):
                os.remove(active_configuration['db_location'])

