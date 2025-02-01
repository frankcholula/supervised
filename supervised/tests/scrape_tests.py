import unittest
from supervised.scrape import fetch_recent_papers

class TestScraping(unittest.TestCase):
    def setUp(self):
        self.test_name = "Mark Plumbley"
        self.author, self.papers = fetch_recent_papers(self.test_name, 3)

    def test_valid_author(self):
        """Test that author data is valid and complete"""
        self.assertIsNotNone(self.author)
        self.assertIsNotNone(self.author["name"])
        self.assertGreaterEqual(self.author["h_index"], 0)
        self.assertGreaterEqual(self.author["citations"], 0)
        self.assertIsNotNone(self.author["affiliation"])
        self.assertIsNotNone(self.author["interests"])
        self.assertIsNotNone(self.author["picture_url"])

    def test_recent_papers_sorted(self):
        """Test that recent papers are sorted by year in descending order"""
        recent_papers = self.papers["recent_papers"]
        self.assertTrue(len(recent_papers) > 0)
        
        # Check papers are sorted by year descending
        years = [paper["year"] for paper in recent_papers]
        self.assertEqual(years, sorted(years, reverse=True))

        # Check abstracts exist
        for paper in recent_papers:
            self.assertIsNotNone(paper["abstract"])
            self.assertNotEqual(paper["abstract"], "")

    def test_cited_papers_sorted(self):
        """Test that most cited papers are sorted by citations in descending order"""
        cited_papers = self.papers["most_cited_papers"]
        self.assertTrue(len(cited_papers) > 0)

        # Check papers are sorted by citations descending
        citations = [paper["citations"] for paper in cited_papers]
        self.assertEqual(citations, sorted(citations, reverse=True))

        # Check abstracts exist
        for paper in cited_papers:
            self.assertIsNotNone(paper["abstract"])
            self.assertNotEqual(paper["abstract"], "")

if __name__ == '__main__':
    unittest.main()

