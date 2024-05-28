import unittest

from domain.post import create_content, shorten_content, add_hashtags


class TestPost(unittest.TestCase):
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
            result = add_hashtags(test_case["product_title"], test_case["brand"])
            self.assertEqual(result, test_case["expected"])

    def test_shorten_content(self):
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
            result = shorten_content(test_case["product_title"])
            self.assertEqual(result, test_case["expected"])

    def test_create_content(self):
        test_case = {
            "discount_rate": 10,
            "product_title": "テスト商品1",
            "short_url": "http://tinyurl.com/test",
            "expected": {
                "text": f"""
【10%オフ！】

テスト商品1

詳細は🔽からチェック✔
http://tinyurl.com/test

#キャンプ
#アウトドア
#キャンプ好きと繋がりたい
        """
            },
        }

        result = create_content(
            test_case["discount_rate"],
            test_case["product_title"],
            test_case["short_url"],
        )
        self.assertEqual(result, test_case["expected"])


if __name__ == "__main__":
    unittest.main()
