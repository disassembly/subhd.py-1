import unittest

import opencc
import requests

from subhd.exceptions import SubHDDownloadException
from subhd.item import SubHDItem


class TestItem(unittest.TestCase):
    KEYWORD = u"普羅米修斯"
    ID = 309312

    def setUp(self):
        self.item = SubHDItem(self.ID)

    def test_parse_content(self):
        document = self.item.parse_content()
        converted_keyword = opencc.convert(self.KEYWORD, config="t2s.json")
        self.assertIn(converted_keyword, document.title.text)

    def test_get_file_url(self):
        file_url = self.item.get_file_url()
        response = requests.get(file_url)
        self.assertEqual(response.status_code, 200)

    def test_get_file_url_raises_exception(self):
        self.item.id = -1
        self.assertRaises(SubHDDownloadException, self.item.get_file_url)


if __name__ == "__main__":
    unittest.main()