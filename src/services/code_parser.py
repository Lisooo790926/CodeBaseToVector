import os
from pathlib import Path
from typing import List, Dict, Optional
from tree_sitter import Language, Parser
import logging

from ..config.config import settings
from tree_sitter_languages import get_language, get_parser

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class JavaCodeParser:
    def __init__(self):
        """Initialize the Java code parser"""
        try:
            # Get the Java language and parser from tree_sitter_languages
            self.JAVA_LANGUAGE = get_language('java')
            self.parser = get_parser('java')
        except Exception as e:
            logger.error(f"Failed to initialize Java parser: {str(e)}")
            raise
        
    def parse_file(self, file_path: str) -> Optional[Dict]:
        """
        Parse a single Java file
        
        Args:
            file_path: Path to the Java file
            
        Returns:
            Dict containing the parsed content or None if parsing fails
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Get file metadata
            file_info = {
                'file_path': file_path,
                'content': content,
                'size': len(content.splitlines())
            }
            
            # Basic validation
            if file_info['size'] > settings.MAX_FILE_SIZE:
                logger.warning(f"File {file_path} exceeds maximum size limit")
                # TODO: Implement file splitting logic here
                return file_info
            
            return file_info
            
        except Exception as e:
            logger.error(f"Error parsing file {file_path}: {str(e)}")
            return None
    
    def parse_directory(self, directory_path: str) -> List[Dict]:
        """
        Parse all Java files in a directory
        
        Args:
            directory_path: Path to the directory containing Java files
            
        Returns:
            List of parsed file contents
        """
        parsed_files = []
        try:
            for root, _, files in os.walk(directory_path):
                for file in files:
                    if file.endswith('.java'):
                        file_path = os.path.join(root, file)
                        parsed_file = self.parse_file(file_path)
                        if parsed_file:
                            parsed_files.append(parsed_file)
        except Exception as e:
            logger.error(f"Error parsing directory {directory_path}: {str(e)}")
        
        return parsed_files 