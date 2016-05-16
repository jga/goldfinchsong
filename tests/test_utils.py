from collections import OrderedDict
from datetime import datetime, timezone
import unittest
from os.path import join
from tinydb import TinyDB, storages
from goldfinchsong import utils

IMAGE_NAMES = ['goldfinch1.jpg', 'goldfinch2.jpg', 'goldfinch3.jpg',
               'goldfinch4.jpg', 'goldfinch5.jpg']

TEST_TEXT1 = 'This is a test of the goldfinchsong project. This test checks ' \
            'abbreviations, vowel elision, length checking, and other logic. ' \
            'Tests are important!'

TEST_TEXT2 = 'This is a test of the goldfinchsong project. Tests ' \
            'abbreviations, vowel elision, length checking, and other logic. ' \
            'Tests are important!'


class LoadContentTests(unittest.TestCase):

    def test_basic_load(self):
        image_directory = 'tests/images/'
        db = TinyDB(storage=storages.MemoryStorage)
        content = utils.load_content(db, image_directory)
        full_image_path = content[0]
        image_file = full_image_path.replace(image_directory, '')
        status_text = content[1]
        self.assertTrue(image_file in IMAGE_NAMES)
        self.assertEqual(image_file.replace('.jpg', ''), status_text)

    def test_storage_in_db(self):
        image_directory = 'tests/images/'
        # let's load a list of tweets into the db
        db = TinyDB(storage=storages.MemoryStorage)
        image_names = [
            'goldfinch1.jpg',
            'goldfinch2.jpg',
            'goldfinch3.jpg',
            'goldfinch4.jpg'
        ]
        for image_name in image_names:
            delivery_timestamp = datetime.now(tz=timezone.utc).isoformat()
            tweet = {'image': image_name, 'delivered_on': delivery_timestamp}
            db.insert(tweet)
        content = utils.load_content(db, image_directory)
        self.assertEqual(content[2], 'goldfinch5.jpg')
        tweets = db.all()
        self.assertEqual(len(tweets), 4, msg=tweets)


class UtilitiesTests(unittest.TestCase):

    def test_apply_abbreviations(self):
        text_conversions = {
            'abbreviations': 'abbr',
            'goldfinchsong': 'gf',
            'important': 'impt'
        }
        # exhausts all conversions before reaching limit
        new_text1 = utils.apply_abbreviations(TEST_TEXT1, text_conversions)
        expected_text1 = 'This is a test of the gf project. This test checks ' \
                    'abbr, vowel elision, length checking, and other logic. ' \
                    'Tests are impt!'
        self.assertEqual(expected_text1, new_text1)
        new_text2 = utils.apply_abbreviations(TEST_TEXT2, text_conversions)
        self.assertTrue(len(new_text2) <= 117)

    def test_apply_vowel_elision(self):
        result_text = utils.apply_vowel_elision(TEST_TEXT1)
        expected_text = 'This is a tst of the gldfnchsng prjct. Ths tst chcks ' \
                        'abbrvtns, vwl elsn, lngth chckng, and othr lgc. Tsts ' \
                        'are imprtnt!'
        self.assertEqual(expected_text, result_text)

    def test_assemble_elided_status(self):
        complete_words = ['test', 'a', 'is', 'This']
        elided_words = ['systm', 'gldfnch', 'the', 'of']
        result = utils.assemble_elided_status(complete_words, elided_words)
        self.assertEqual('This is a test of the gldfnch systm', result)

    def test_chop_words(self):
        result_text = utils.chop_words(TEST_TEXT1)
        expected_text = 'This is a test of the goldfinchsong project. This test checks ' \
                        'abbreviations, vowel elision, length checking, and'
        self.assertEqual(expected_text, result_text)

    def test_is_image(self):
        image_files = [
            'image.gif',
            'image.jpg',
            'image.jpeg',
            'image.png',
            'image.GIF',
            'image.JPG',
            'image.JPEG',
            'image.PNG',
            'image.GiF',
            'image.JpG',
            'image.JpEg',
            'image.PnG'
        ]
        for image_file in image_files:
            self.assertTrue(utils.is_image_file(image_file))

    def test_is_not_image(self):
        image_files = [
            'image.docx',
            'image.pdf',
            'image.md',
            'image.html',
            'image.css',
            'image.odt',
            'image.sh',
            'image.xlsx',
            'image.txt',
            'image.c',
            'image.py',
            'image'
        ]
        for image_file in image_files:
            self.assertFalse(utils.is_image_file(image_file))

    def test_trim_file_extensions(self):
        image_files = [
            'image.gif',
            'image.jpg',
            'image.jpeg',
            'image.png',
            'image.GIF',
            'image.JPG',
            'image.JPEG',
            'image.PNG',
            'image.GiF',
            'image.JpG',
            'image.JpEg',
            'image.PnG'
        ]
        for image_file in image_files:
            self.assertEqual(utils.trim_file_extension(image_file), 'image')

    def test_to_compact_text(self):
        text_conversions = {
            'abbreviations': 'abbrs',
            'goldfinchsong': 'gfnch',
            'important': 'importnt'
        }
        candidate_text1 = utils.to_compact_text(TEST_TEXT1, 100, text_conversions)
        expected_text1 = 'Ths is a tst of the gfnch prjct. Ths tst chcks abbrs, ' \
                         'vwl elsn, lngth chckng, and othr lgc. Tsts are'
        self.assertEqual(expected_text1, candidate_text1)
        candidate_text2 = utils.to_compact_text(TEST_TEXT1, 50, text_conversions)
        expected_text2 = 'Ths is a tst of the gfnch prjct. Ths tst chcks'
        self.assertEqual(expected_text2, candidate_text2)
        candidate_text3 = utils.to_compact_text(TEST_TEXT1, 20, text_conversions)
        expected_text3 = 'Ths is a tst of the'
        self.assertEqual(expected_text3, candidate_text3)

    def test_extract_status_text(self):
        conversion_data = (
            ('abbreviations', 'abbrs'),
            ('goldfinchsong', 'gfnch'),
            ('important', 'importnt'),
        )
        text_conversions = OrderedDict(conversion_data)
        file = 'Some_goldfinchsong_image-file_with_a_very_long_set_of_' \
               'characters_and_abbreviations_that_conveys_important_info.png'
        candidate_text1 = utils.extract_status_text(file, text_conversions, maximum_length=100,)
        expected_text1 = 'Some gfnch image-file with a very long set of characters and abbrs that conveys important info'
        self.assertEqual(expected_text1, candidate_text1)
        candidate_text2 = utils.extract_status_text(file, text_conversions, maximum_length=70,)
        expected_text2 = 'Sme gfnch imge-fle wth a vry lng st of chrctrs and abbrs tht cnvys'
        self.assertEqual(expected_text2, candidate_text2)

    def test_get_unused_files(self):
        available_files = list()
        for index in range(1,101):
            image_name = 'image{0}.png'.format(index)
            available_files.append(image_name)
        db = TinyDB(storage=storages.MemoryStorage)
        for id in range(1,52):
            image_name = 'image{0}.png'.format(id)
            db.insert({'image': image_name})
        unused_files = utils.get_unused_files(db, available_files)
        self.assertEqual(len(unused_files), 49)
        self.assertEqual(unused_files[0], 'image52.png')
        self.assertEqual(unused_files[5], 'image57.png')
        self.assertEqual(unused_files[10], 'image62.png')
        self.assertEqual(unused_files[15], 'image67.png')
        self.assertEqual(unused_files[20], 'image72.png')
        self.assertEqual(unused_files[33], 'image85.png')
        self.assertEqual(unused_files[48], 'image100.png')

    def test_db_purge_when_all_posted(self):
        available_files = list()
        for index in range(1,101):
            image_name = 'image{0}.png'.format(index)
            available_files.append(image_name)
        db = TinyDB(storage=storages.MemoryStorage)
        for id in range(1,106):
            image_name = 'image{0}.png'.format(id)
            db.insert({'image': image_name})
        self.assertEqual(len(db.all()), 105)
        unused_files = utils.get_unused_files(db, available_files)
        self.assertEqual(len(unused_files), 100)
        self.assertEqual(unused_files[0], 'image1.png')
        self.assertEqual(unused_files[5], 'image6.png')
        self.assertEqual(unused_files[10], 'image11.png')
        self.assertEqual(unused_files[33], 'image34.png')
        self.assertEqual(unused_files[50], 'image51.png')




