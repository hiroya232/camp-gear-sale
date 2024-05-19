import unittest

from domain.tweet import create_content


class TestTweet(unittest.TestCase):
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
