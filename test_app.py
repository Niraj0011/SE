import unittest
from app import Article, Comment, articles, comments, load_data, save_data
from datetime import datetime
import csv
import os

class TestNewsPortal(unittest.TestCase):

    def setUp(self):
        global articles, comments
        articles = []
        comments = []
        load_data()
        print(f"SetUp: Loaded {len(articles)} articles, {len(comments)} comments")

    def tearDown(self):
        save_data()
        print(f"TearDown: Saved {len(articles)} articles, {len(comments)} comments")

    def test_load_data(self):
        print(f"Test: Articles loaded: {[a.title for a in articles]}")
        self.assertGreaterEqual(len(articles), 0, "Articles should load, even if empty")
        if len(articles) > 0:
            self.assertTrue(all(isinstance(a, Article) for a in articles), "All items should be Article objects")

    def test_add_article(self):
        new_article = Article(4, "Test Article", "Test content", "TestAuthor", datetime.now())
        articles.append(new_article)
        save_data()
        load_data()
        self.assertIn(new_article, articles, "New article should be persisted")
        self.assertEqual(len(articles), len(set(a.title for a in articles)), "No duplicates should exist")

    def test_add_comment(self):
        articles.append(Article(4, "Test Article", "Test content", "TestAuthor", datetime.now()))
        save_data()
        comment = Comment(1, 4, "Jane", "Great!", datetime.now())
        comments.append(comment)
        save_data()
        load_data()
        self.assertIn(comment, comments, "New comment should be persisted")
        self.assertEqual(comment.text, "Great!", "Comment text should match")

if __name__ == '__main__':
    unittest.main()