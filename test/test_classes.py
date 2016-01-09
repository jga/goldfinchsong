import configparser
import unittest
import pytest
from goldfinchsong.cli import parse_configuration
from goldfinchsong.classes import Manager


class ManagerTests(unittest.TestCase):

    def test_bad_send_tweet(self):
        config_parser = configparser.ConfigParser()
        config_parser.optionxform = str
        config_parser.read('test/goldfinchsong.ini')
        active_configuration = parse_configuration(config_parser)
        credentials = active_configuration['credentials']
        text_conversions = active_configuration['text_conversions']
        manager = Manager(credentials, active_configuration['image_directory'], text_conversions)
        with pytest.raises(Exception):
            manager.content = None
            manager.post_tweet()
