import unittest

from server import app, text_data


class ServerApiTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_save_and_get(self):
        response = self.client.post("/save", json={"text": "production test"})
        self.assertEqual(response.status_code, 200)
        payload = self.client.get("/get").get_json()
        self.assertEqual(payload["text"], "production test")

    def test_rejects_invalid_json(self):
        response = self.client.post(
            "/save",
            data="not-json",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_rejects_oversized_text(self):
        response = self.client.post("/save", json={"text": "x" * 10001})
        self.assertEqual(response.status_code, 413)


if __name__ == "__main__":
    unittest.main()
