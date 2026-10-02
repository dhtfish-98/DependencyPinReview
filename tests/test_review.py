import unittest
from review import review_text


class DependencyTests(unittest.TestCase):
    def test_exact_pin(self):
        self.assertEqual(review_text("# owned project\nrequests==2.32.3\nfoo[bar]==1.2; python_version > '3.10'\n"), [])

    def test_unpinned_and_sources(self):
        rules = [x["rule"] for x in review_text("requests>=2\n-r extras.txt\ngit+https://example.invalid/repo\n")]
        self.assertEqual(rules, ["not-exactly-pinned", "external-include", "direct-source"])

    def test_comments_and_options(self):
        self.assertEqual(review_text("--extra-index-url https://example.invalid\n")[0]["rule"], "installer-option")
        self.assertEqual(review_text("requests==2.0,>=3\n")[0]["rule"], "not-exactly-pinned")
