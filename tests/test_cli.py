import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from collab_lab.cli import digest, find_duplicates, main


class DuplicateFinderTests(unittest.TestCase):
    def test_detects_same_content_across_names_and_subdirectories(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "nested").mkdir()
            (root / "a.txt").write_text("same")
            (root / "nested" / "b.txt").write_text("same")
            (root / "unique.txt").write_text("different")
            self.assertEqual(find_duplicates(root), [["a.txt", "nested/b.txt"]])

    def test_same_size_different_contents_are_not_duplicates(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "one").write_bytes(b"abc")
            (root / "two").write_bytes(b"xyz")
            self.assertEqual(find_duplicates(root), [])

    def test_invalid_directory_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(NotADirectoryError):
                find_duplicates(Path(directory) / "missing")

    def test_json_output(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "a").write_bytes(b"test")
            (root / "b").write_bytes(b"test")
            output = StringIO()
            with redirect_stdout(output):
                self.assertEqual(main([directory, "--json"]), 0)
            self.assertEqual(json.loads(output.getvalue()), {"duplicate_groups": [["a", "b"]]})

    def test_sha256_matches_known_value(self):
        with tempfile.TemporaryDirectory() as directory:
            file = Path(directory) / "empty"
            file.write_bytes(b"")
            self.assertEqual(digest(file), "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")


if __name__ == "__main__":
    unittest.main()
