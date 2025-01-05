import unittest

from dotenv import load_dotenv
from src.utils.embedding import generate_embedding

load_dotenv()


class TestEmbedding(unittest.TestCase):
    def setUp(self):
        self.text = "This is a test text"

    def test_generate_embedding_dimensions(self):
        embedding = generate_embedding(self.text)
        self.assertIsInstance(embedding, list)
        self.assertEqual(len(embedding), 768)
        all(self.assertIsInstance(x, float) for x in embedding)

    def test_generate_embedding_consistency(self):
        # Same text should produce same embedding
        embedding1 = generate_embedding(self.text)
        embedding2 = generate_embedding(self.text)

        self.assertEqual(embedding1, embedding2)

    def test_generate_embedding_different_texts(self):
        text1 = "This is the first text"
        text2 = "This is a completely different text"

        embedding1 = generate_embedding(text1)
        embedding2 = generate_embedding(text2)

        # Different texts should produce different embeddings
        self.assertNotEqual(embedding1, embedding2)


if __name__ == "__main__":
    unittest.main()
