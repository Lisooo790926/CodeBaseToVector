import unittest
import os
from pathlib import Path

from src.services.code_parser import JavaCodeParser

class TestJavaCodeParser(unittest.TestCase):
    def setUp(self):
        self.parser = JavaCodeParser()
        # Get the absolute path of the test directory
        self.test_dir = os.path.dirname(os.path.abspath(__file__))
        self.test_app_dir = os.path.join(os.path.dirname(self.test_dir), 'test_app')
        
    def test_parse_directory(self):
        """Test parsing a directory of Java files"""
        parsed_files = self.parser.parse_directory(self.test_app_dir)
        self.assertTrue(len(parsed_files) > 0)
        
    def test_parse_file(self):
        """Test parsing a single Java file"""
        # Find a Java file in the test_app directory
        java_file = None
        for root, _, files in os.walk(self.test_app_dir):
            for file in files:
                if file.endswith('.java'):
                    java_file = os.path.join(root, file)
                    break
            if java_file:
                break
                
        self.assertIsNotNone(java_file, "No Java file found in test_app directory")
        
        # Parse the file
        parsed_file = self.parser.parse_file(java_file)
        
        # Basic assertions
        self.assertIsNotNone(parsed_file)
        self.assertIn('file_path', parsed_file)
        self.assertIn('content', parsed_file)
        self.assertIn('size', parsed_file)
        
        # New metadata assertions
        self.assertIn('package', parsed_file)
        self.assertIn('imports', parsed_file)
        self.assertIn('classes', parsed_file)
        
        # If there are classes, test class metadata
        if parsed_file['classes']:
            test_class = parsed_file['classes'][0]
            self.assertIn('name', test_class)
            self.assertIn('modifiers', test_class)
            self.assertIn('fields', test_class)
            self.assertIn('methods', test_class)
            
            # If there are methods, test method metadata
            if test_class['methods']:
                test_method = test_class['methods'][0]
                self.assertIn('name', test_method)
                self.assertIn('parameters', test_method)
                self.assertIn('modifiers', test_method)
                self.assertIn('body', test_method)
                self.assertIn('start_line', test_method)
                self.assertIn('end_line', test_method)

if __name__ == '__main__':
    unittest.main() 