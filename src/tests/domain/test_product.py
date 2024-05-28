import unittest
from unittest.mock import patch

from domain.product import fetch_product_info


class TestProduct(unittest.TestCase):

    @patch("product.Shortener")
    @patch("product.auth_amazon_api")
    def test_fetch_product_info(self, mock_auth_amazon_api, mock_shortener):
        test_cases = [
            {
                # 割引に関する情報がNoneの場合
                "data": [
                    {
                        "offers": {"listings": [{"price": {"savings": None}}]},
                        "item_info": {
                            "title": {"display_value": "テスト商品1"},
                            "by_line_info": {
                                "brand": {"display_value": "テストブランド1"}
                            },
                        },
                        "detail_page_url": "http://test1.com",
                    },
                    {
                        "offers": {
                            "listings": [{"price": {"savings": {"percentage": 20}}}]
                        },
                        "item_info": {
                            "title": {"display_value": "テスト商品2"},
                            "by_line_info": {
                                "brand": {"display_value": "テストブランド2"}
                            },
                        },
                        "detail_page_url": "http://test2.com",
                    },
                    {
                        "offers": {
                            "listings": [{"price": {"savings": {"percentage": 30}}}]
                        },
                        "item_info": {
                            "title": {"display_value": "テスト商品3"},
                            "by_line_info": {
                                "brand": {"display_value": "テストブランド3"}
                            },
                        },
                        "detail_page_url": "http://test3.com",
                    },
                ],
                "expected": [20, "テスト商品2", "http://tinyurl.com/test"],
            },
            {
                # ブランド名がNoneの場合
                "data": [
                    {
                        "offers": {
                            "listings": [{"price": {"savings": {"percentage": 10}}}]
                        },
                        "item_info": {
                            "title": {"display_value": "テスト商品1"},
                            "by_line_info": {"brand": {"display_value": None}},
                        },
                        "detail_page_url": "http://amazon.com",
                    },
                    {
                        "offers": {
                            "listings": [{"price": {"savings": {"percentage": 20}}}]
                        },
                        "item_info": {
                            "title": {"display_value": "テスト商品2"},
                            "by_line_info": {
                                "brand": {"display_value": "テストブランド2"}
                            },
                        },
                        "detail_page_url": "http://test2.com",
                    },
                    {
                        "offers": {
                            "listings": [{"price": {"savings": {"percentage": 30}}}]
                        },
                        "item_info": {
                            "title": {"display_value": "テスト商品3"},
                            "by_line_info": {
                                "brand": {"display_value": "テストブランド3"}
                            },
                        },
                        "detail_page_url": "http://test3.com",
                    },
                ],
                "expected": [20, "テスト商品2", "http://tinyurl.com/test"],
            },
            {
                # 商品タイトルがNoneの場合
                "data": [
                    {
                        "offers": {
                            "listings": [{"price": {"savings": {"percentage": 10}}}]
                        },
                        "item_info": {
                            "title": {"display_value": None},
                            "by_line_info": {
                                "brand": {"display_value": "テストブランド1"}
                            },
                        },
                        "detail_page_url": "http://amazon.com",
                    },
                    {
                        "offers": {
                            "listings": [{"price": {"savings": {"percentage": 20}}}]
                        },
                        "item_info": {
                            "title": {"display_value": "テスト商品2"},
                            "by_line_info": {
                                "brand": {"display_value": "テストブランド2"}
                            },
                        },
                        "detail_page_url": "http://test2.com",
                    },
                    {
                        "offers": {
                            "listings": [{"price": {"savings": {"percentage": 30}}}]
                        },
                        "item_info": {
                            "title": {"display_value": "テスト商品3"},
                            "by_line_info": {
                                "brand": {"display_value": "テストブランド3"}
                            },
                        },
                        "detail_page_url": "http://test3.com",
                    },
                ],
                "expected": [20, "テスト商品2", "http://tinyurl.com/test"],
            },
            {
                # 商品詳細ページURLがNoneの場合
                "data": [
                    {
                        "offers": {
                            "listings": [{"price": {"savings": {"percentage": 10}}}]
                        },
                        "item_info": {
                            "title": {"display_value": "テスト商品1"},
                            "by_line_info": {
                                "brand": {"display_value": "テストブランド1"}
                            },
                        },
                        "detail_page_url": None,
                    },
                    {
                        "offers": {
                            "listings": [{"price": {"savings": {"percentage": 20}}}]
                        },
                        "item_info": {
                            "title": {"display_value": "テスト商品2"},
                            "by_line_info": {
                                "brand": {"display_value": "テストブランド2"}
                            },
                        },
                        "detail_page_url": "http://test2.com",
                    },
                    {
                        "offers": {
                            "listings": [{"price": {"savings": {"percentage": 30}}}]
                        },
                        "item_info": {
                            "title": {"display_value": "テスト商品3"},
                            "by_line_info": {
                                "brand": {"display_value": "テストブランド3"}
                            },
                        },
                        "detail_page_url": "http://test3.com",
                    },
                ],
                "expected": [20, "テスト商品2", "http://tinyurl.com/test"],
            },
        ]

        for test_case in test_cases:
            mock_shortener.return_value.tinyurl.short.return_value = (
                "http://tinyurl.com/test"
            )
            mock_auth_amazon_api.return_value.search_items.return_value = test_case

            result = fetch_product_info()

            self.assertEqual(result, test_case["expected"])


if __name__ == "__main__":
    unittest.main()
