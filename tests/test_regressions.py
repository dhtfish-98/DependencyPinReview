import json
import plistlib
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from review import review_text


class RegressionTests(unittest.TestCase):

    def test_wildcard_pin_and_invalid_version(self):
        self.assertEqual(review_text("owned==1.*\n")[0]["rule"],"not-exactly-pinned")
        self.assertEqual(review_text("owned==${VERSION}\n")[0]["rule"],"unparsed-line")
    def test_marker_and_continued_hash(self):
        line="owned[extra] == 1.2; python_version >= '3.12' \\\n --hash=sha256:"+"a"*64+"\n"
        self.assertEqual(review_text(line),[])
        with self.assertRaises(ValueError): review_text("owned==1 \\\n")
