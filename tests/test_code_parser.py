import unittest
import os
import sys
from pathlib import Path

# Get current file's directory and project root
current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent

# Add project root to Python path
sys.path.append(str(project_root))

from src.services.code_parser import JavaCodeParser

class TestJavaCodeParser(unittest.TestCase):
    def setUp(self):
        self.parser = JavaCodeParser()
        # Use absolute path for test directory
        self.test_dir = os.path.join(project_root, "test_app/src/main/java/com/example/demo")
        
        # Ensure test directory exists
        if not os.path.exists(self.test_dir):
            raise RuntimeError(f"Test directory not found: {self.test_dir}")
        
    def test_parse_file(self):
        # Test parsing a single file
        test_file = os.path.join(self.test_dir, "DemoApplication.java")
        if not os.path.exists(test_file):
            raise RuntimeError(f"Test file not found: {test_file}")
            
        result = self.parser.parse_file(test_file)
        
        self.assertIsNotNone(result)
        self.assertEqual(result['file_path'], test_file)
        self.assertGreater(len(result['content']), 0)
        print(f"\nParsed file result: {result}")
        
    def test_parse_directory(self):
        # Test parsing entire directory
        results = self.parser.parse_directory(self.test_dir)
        
        self.assertGreater(len(results), 0)
        for result in results:
            self.assertIn('file_path', result)
            self.assertIn('content', result)
            self.assertIn('size', result)
            print(f"\nParsed directory result: {result}")

if __name__ == '__main__':
    unittest.main() 