from .base_config import BaseConfig
from conduit.tests.factories import ArticleFactory

class ArticlesTestCase(BaseConfig):

    def test_user_can_create_article(self):
        response = self.client.post(
            '/api/articles',
            data = {
                "article": {
                    "title": "Test title",
                    "body": "This is a very awesome article on testing tests",
                    "description": "Written by testing tester",
                    "tags": ["religion", "nature", "film"]
                }
            },
            format='json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["description"], "Written by testing tester")

    def test_user_can_get_articles(self):
        for i in range(0,15):
            #generates multiple article instances using the factory class
            ArticleFactory()
        response = self.client.get('/api/articles')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 15)


