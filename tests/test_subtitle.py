import unittest

import opencc
import requests

from subhd.exceptions import SubHDDownloadException
from subhd.subtitle import SubHDSubtitle


class TestSubtitle(unittest.TestCase):
    KEYWORD = u"普羅米修斯"
    ID = 309312

    def setUp(self):
        self.item = SubHDSubtitle(self.ID)

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

    def test_download_archive(self):
        with self.item.download_archive() as archive:
            self.assertGreater(len(archive.read()), 0)

    def test_extract_subtitles(self):
        self.assertGreater(len(self.item.extract_subtitles()), 0)

    def test_translate_subtitles(self):
        subtitle_files = self.item.translate_subtitles()
        self.assertGreater(len(subtitle_files), 0)

        subtitle_file = subtitle_files[0]
        self.assertIn(self.KEYWORD, subtitle_file.content)

if __name__ == "__main__":
    unittest.main()
