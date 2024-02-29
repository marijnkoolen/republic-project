import json
import unittest

from pagexml.parser import json_to_pagexml_page, read_pagexml_file

import republic.parser.pagexml.republic_page_parser as page_parser


class TestPageParser(unittest.TestCase):

    def setUp(self) -> None:
        self.page_files = {
            'page1': './tests/test_data/NL-HaNA_1.01.02_4561_0088-page-175-date-2024-02-13.json',
            'page2': './tests/test_data/NL-HaNA_1.01.02_4561_0089-page-177-date-2024-02-13.json',
            'page3': './tests/test_data/NL-HaNA_1.01.02_4561_0094-page-187-date-2024-02-13.json',
            'page4': './tests/test_data/NL-HaNA_1.01.02_4542_0002-page-2-date-2023-12-19.json'
        }

    def test_update_line_types(self):
        page_json = json.loads(read_pagexml_file(self.page_files['page1']))
        page = json_to_pagexml_page(page_json)
        new_page = page_parser.update_line_types(page)
        test_id = "NL-HaNA_1.01.02_4561_0088-text_region-2660-180-623-140"
        trs = [tr for col in new_page.columns for tr in col.text_regions]
        test_tr = [tr for tr in trs if tr.id == test_id][0]
        for li, line in enumerate(test_tr.lines):
            with self.subTest(li):
                self.assertEqual('date_header', line.metadata['line_class'])

    def test_split_page_column_text_regions(self):
        page_json = json.loads(read_pagexml_file(self.page_files['page2']))
        page = json_to_pagexml_page(page_json)
        new_page = page_parser.split_page_column_text_regions(page, update_type=True)
        test_map = {
            "NL-HaNA_1.01.02_4561_0089-text_region-2661-171-624-177": "date_header",
            "NL-HaNA_1.01.02_4561_0089-text_region-2605-1570-1095-298": "attendance"
        }
        trs = [tr for col in new_page.columns for tr in col.text_regions]
        print([tr.id for tr in trs])
        test_trs = [tr for tr in trs if tr.id in test_map]
        self.assertEqual(len(test_map), len(test_trs))
        count = 0
        for ti, test_tr in enumerate(test_trs):
            for li, line in enumerate(test_tr.lines):
                with self.subTest(count):
                    self.assertEqual(test_map[test_tr.id], line.metadata['line_class'])
                    count += 1

    def test_split_page_column_text_regions_avoids_splitting_regions(self):
        page_json = json.loads(read_pagexml_file(self.page_files['page4']))
        page = json_to_pagexml_page(page_json)
        new_page = page_parser.split_page_column_text_regions(page, update_type=True)
        test_id = "NL-HaNA_1.01.02_4542_0002-text_region-1021-1097-1509-1414"
        trs = [tr for col in new_page.columns for tr in col.text_regions]
        print([tr.id for tr in trs])
        self.assertEqual(True, any([tr.id == test_id for tr in trs]))