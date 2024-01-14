import unittest
from unittest.mock import patch

from product import (
    hashtagging_brand_names_in_product_titie,
    omit_product_title,
    get_product_info,
)


class TestProduct(unittest.TestCase):
    def test_hashtagging_brand_names_in_product_titie(self):
        test_cases = [
            {
                # ブランド名の中に半角スペースが存在しない
                "product_title": "ソト (SOTO) マイクロトーチ",
                "brand": "ソト(SOTO)",
                "expected": "#ソト  (#SOTO ) マイクロトーチ",
            },
            {
                # ブランド名の中に半角スペースが存在する
                "product_title": "スノーピーク(snow peak) HOME&CAMPバーナー",
                "brand": "Snow Peak(スノーピーク)",
                "expected": "#スノーピーク (#SnowPeak ) HOME&CAMPバーナー",
            },
            {
                # ブランド名が英語のみ
                "product_title": "Naturehike 寝袋",
                "brand": "Naturehike",
                "expected": "#Naturehike  寝袋",
            },
            {
                # 「ブランド名に半角スペースが存在する」かつ「商品タイトルには半角スペースが存在しない」
                "product_title": "PrimeCamp エアーポンプ",
                "brand": "Prime Camp",
                "expected": "#PrimeCamp  エアーポンプ",
            },
        ]

        for test_case in test_cases:
            result = hashtagging_brand_names_in_product_titie(
                test_case["product_title"], test_case["brand"]
            )
            self.assertEqual(result, test_case["expected"])

    def test_omit_product_title(self):
        test_cases = [
            {
                # 商品タイトルが61文字以上
                "product_title": "[#ソト  (#SOTO )] 日本製 キャンドル 風 ガスランタン 専用スタビライザー 転倒防止 折りたたみ式 コンパク",
                "expected": "[#ソト  (#SOTO )] 日本製 キャンドル 風 ガスランタン 専用スタビライザー 転倒防止 折りたたみ式 コンパ…",
            },
            {
                # 商品タイトルが60文字
                "product_title": "[#ソト  (#SOTO )] 日本製 キャンドル 風 ガスランタン 専用スタビライザー 転倒防止 折りたたみ式 コンパ",
                "expected": "[#ソト  (#SOTO )] 日本製 キャンドル 風 ガスランタン 専用スタビライザー 転倒防止 折りたたみ式 コンパ…",
            },
            {
                # 商品タイトルが59文字以下
                "product_title": "[#ソト  (#SOTO )] 日本製 キャンドル 風 ガスランタン 専用スタビライザー 転倒防止 折りたたみ式 コン",
                "expected": "[#ソト  (#SOTO )] 日本製 キャンドル 風 ガスランタン 専用スタビライザー 転倒防止 折りたたみ式 コン",
            },
        ]

        for test_case in test_cases:
            result = omit_product_title(test_case["product_title"])
            self.assertEqual(result, test_case["expected"])

    @patch("product.Shortener")
    @patch("product.auth_amazon_api")
    def test_get_product_info(self, mock_auth_amazon_api, mock_shortener):
        test_cases = [
            {
                # 割引に関する情報がNoneの場合
                "data": [
                    {
                        "offers": {"listings": [{"price": {"savings": None}}]},
                        "item_info": {
                            "title": {"display_value": "テスト商品1"},
                            "by_line_info": {"brand": {"display_value": "テストブランド1"}},
                        },
                        "detail_page_url": "http://test1.com",
                    },
                    {
                        "offers": {
                            "listings": [{"price": {"savings": {"percentage": 20}}}]
                        },
                        "item_info": {
                            "title": {"display_value": "テスト商品2"},
                            "by_line_info": {"brand": {"display_value": "テストブランド2"}},
                        },
                        "detail_page_url": "http://test2.com",
                    },
                    {
                        "offers": {
                            "listings": [{"price": {"savings": {"percentage": 30}}}]
                        },
                        "item_info": {
                            "title": {"display_value": "テスト商品3"},
                            "by_line_info": {"brand": {"display_value": "テストブランド3"}},
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
                            "by_line_info": {"brand": {"display_value": "テストブランド2"}},
                        },
                        "detail_page_url": "http://test2.com",
                    },
                    {
                        "offers": {
                            "listings": [{"price": {"savings": {"percentage": 30}}}]
                        },
                        "item_info": {
                            "title": {"display_value": "テスト商品3"},
                            "by_line_info": {"brand": {"display_value": "テストブランド3"}},
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
                            "by_line_info": {"brand": {"display_value": "テストブランド1"}},
                        },
                        "detail_page_url": "http://amazon.com",
                    },
                    {
                        "offers": {
                            "listings": [{"price": {"savings": {"percentage": 20}}}]
                        },
                        "item_info": {
                            "title": {"display_value": "テスト商品2"},
                            "by_line_info": {"brand": {"display_value": "テストブランド2"}},
                        },
                        "detail_page_url": "http://test2.com",
                    },
                    {
                        "offers": {
                            "listings": [{"price": {"savings": {"percentage": 30}}}]
                        },
                        "item_info": {
                            "title": {"display_value": "テスト商品3"},
                            "by_line_info": {"brand": {"display_value": "テストブランド3"}},
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
                            "by_line_info": {"brand": {"display_value": "テストブランド1"}},
                        },
                        "detail_page_url": None,
                    },
                    {
                        "offers": {
                            "listings": [{"price": {"savings": {"percentage": 20}}}]
                        },
                        "item_info": {
                            "title": {"display_value": "テスト商品2"},
                            "by_line_info": {"brand": {"display_value": "テストブランド2"}},
                        },
                        "detail_page_url": "http://test2.com",
                    },
                    {
                        "offers": {
                            "listings": [{"price": {"savings": {"percentage": 30}}}]
                        },
                        "item_info": {
                            "title": {"display_value": "テスト商品3"},
                            "by_line_info": {"brand": {"display_value": "テストブランド3"}},
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

            result = get_product_info()

            self.assertEqual(result, test_case["expected"])


if __name__ == "__main__":
    unittest.main()
