from textwrap import dedent
import unittest

from domain.post import Post


class TestPost(unittest.TestCase):
    def setUp(self):
        self.post = Post()

    def test_calculate_excess_length(self):
        test_cases = [
            {
                # テンプレートの文字数と動的部分の文字数の合計が139文字以下
                "dynamic_content_list": [
                    "texttexttexttexttexttexttexttexttexttext",
                    "texttexttexttexttexttexttexttexttext",
                ],
                "expected": 0,
            },
            {
                # テンプレートの文字数と動的部分の文字数の合計が140文字ちょうど
                "dynamic_content_list": [
                    "texttexttexttexttexttexttexttexttexttext",
                    "texttexttexttexttexttexttexttexttextt",
                ],
                "expected": 0,
            },
            {
                # テンプレートの文字数と動的部分の文字数の合計が141文字以上
                "dynamic_content_list": [
                    "texttexttexttexttexttexttexttexttexttext",
                    "texttexttexttexttexttexttexttexttextte",
                ],
                "expected": 1,
            },
        ]

        for test_case in test_cases:
            result = self.post.calculate_excess_length(
                test_case["dynamic_content_list"]
            )
            self.assertEqual(result, test_case["expected"])

    def test_add_hashtags(self):
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
            result = self.post.add_hashtags(
                test_case["product_title"], test_case["brand"]
            )
            self.assertEqual(result, test_case["expected"])

    def test_create_post(self):
        test_case = {
            "content": "Test Content",
            "media_id": "12345",
            "expected": {"text": "Test Content", "media": {"media_ids": ["12345"]}},
        }

        result = self.post.create_post(test_case["content"], test_case["media_id"])
        self.assertEqual(result, test_case["expected"])

    def test_shorten_content(self):
        test_case = {
            "target_content": "[#ソト  (#SOTO )] 日本製 キャンドル 風 ガスランタン 専用スタビライザー 転倒防止 折りたたみ式 コンパク",
            "shorten_length": 1,
            "expected": "[#ソト  (#SOTO )] 日本製 キャンドル 風 ガスランタン 専用スタビライザー 転倒防止 折りたたみ式 コンパ…",
        }

        result = self.post.shorten_content(
            test_case["target_content"], test_case["shorten_length"]
        )
        self.assertEqual(result, test_case["expected"])

    def test_create_content(self):
        test_case = {
            "dynamic_content_list": [
                10,
                1000,
                "テスト商品1",
                "http://tinyurl.com/test",
            ],
            "expected": dedent(
                f"""
                    🏷️ 10%🈹 1000円オフ！ 🏷️

                    テスト商品1

                    詳細は下記リンクからチェック☑️
                    http://tinyurl.com/test

                    #キャンプ
                    #アウトドア
                    #キャンプ好きと繋がりたい
                """
            ),
        }

        result = self.post.create_content(
            test_case["dynamic_content_list"],
        )
        self.assertEqual(result, test_case["expected"])


if __name__ == "__main__":
    unittest.main()
