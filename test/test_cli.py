import unittest
import configparser
from goldfinch import cli


class CommandLineInterfaceTests(unittest.TestCase):

    def test_configuration_file_parsing(self):
        config_parser = configparser.ConfigParser()
        config_parser.optionxform = str
        config_parser.read('test/goldfinch.ini')
        active_configuration = cli.parse_configuration(config_parser)
        credentials = active_configuration['credentials']
        text_conversions = active_configuration['text_conversions']
        self.assertEqual(credentials['consumer_key'], 'goldfinch-consumer-key')
        self.assertEqual(credentials['consumer_secret'], 'goldfinch-consumer-secret')
        self.assertEqual(credentials['access_token'], 'goldfinch-access-token')
        self.assertEqual(credentials['access_token_secret'], 'goldfinch-access-token-secret')
        self.assertEqual(text_conversions['etcetera'], 'etc')
        self.assertEqual(text_conversions['for your information'], 'FYI')
        self.assertEqual(text_conversions['Better View Desired'], 'BVD')
        self.assertEqual(active_configuration['image_directory'], 'test/images')

    def test_get_image_directory(self):
        active_configuration = {'image_directory': 'image-dir-test'}
        self.assertEqual(cli.get_image_directory('command-line-image-arg', active_configuration),
                         'command-line-image-arg')
        self.assertEqual(cli.get_image_directory(None, active_configuration), 'image-dir-test')
        self.assertEqual(cli.get_image_directory(None, {}), 'images')

    def test_conversion_ordering(self):
        # config parser should return an OrderedDict
        config_parser = configparser.ConfigParser()
        config_parser.optionxform = str
        config_parser.read('test/goldfinch.ini')
        active_configuration = cli.parse_configuration(config_parser)
        text_conversions = active_configuration['text_conversions']
        index = 0
        expected_data = {
            '0': 'Better View Desired',
            '1': 'etcetera',
            '2': 'for your information'
        }
        for key in text_conversions:
            self.assertEqual(expected_data[str(index)], key)
            index += 1


