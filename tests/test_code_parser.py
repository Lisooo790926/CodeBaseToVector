import unittest
import os
import sys
from pathlib import Path

# Add the project root directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

from src.services.code_parser import JavaCodeParser

class TestJavaCodeParser(unittest.TestCase):
    def setUp(self):
        self.parser = JavaCodeParser()
        self.test_dir = "../test_app/src/main/java/com/example/demo"
        
    def test_parse_file(self):
        # Test parsing a single file
        test_file = os.path.join(self.test_dir, "DemoApplication.java")
        result = self.parser.parse_file(test_file)
        
        self.assertIsNotNone(result)
        self.assertEqual(result['file_path'], test_file)
        self.assertGreater(len(result['content']), 0)
        print(result)
        
    def test_parse_directory(self):
        # Test parsing entire directory
        results = self.parser.parse_directory(self.test_dir)
        
        self.assertGreater(len(results), 0)
        for result in results:
            self.assertIn('file_path', result)
            self.assertIn('content', result)
            self.assertIn('size', result)

if __name__ == '__main__':
    unittest.main() 