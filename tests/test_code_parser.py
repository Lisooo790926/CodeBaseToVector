import pytest
import os
from pathlib import Path

from src.services.code_parser import JavaCodeParser

@pytest.fixture
def parser():
    """創建 JavaCodeParser 實例"""
    return JavaCodeParser()

@pytest.fixture
def test_paths():
    """獲取測試相關的路徑"""
    test_dir = os.path.dirname(os.path.abspath(__file__))
    test_app_dir = os.path.join(os.path.dirname(test_dir), 'test_app')
    return {
        'test_dir': test_dir,
        'test_app_dir': test_app_dir
    }

@pytest.fixture
def java_file(test_paths):
    """找到一個測試用的 Java 文件"""
    for root, _, files in os.walk(test_paths['test_app_dir']):
        for file in files:
            if file.endswith('.java'):
                return os.path.join(root, file)
    pytest.fail("No Java file found in test_app directory")

def test_parse_directory(parser, test_paths):
    """測試解析 Java 文件目錄"""
    parsed_files = parser.parse_directory(test_paths['test_app_dir'])
    assert len(parsed_files) > 0
    print(f"Successfully parsed {len(parsed_files)} files from directory")

def test_parse_file(parser, java_file):
    """測試解析單個 Java 文件"""
    # 解析文件
    parsed_file = parser.parse_file(java_file)
    
    # 基本斷言
    assert parsed_file is not None
    assert 'file_path' in parsed_file
    assert 'content' in parsed_file
    assert 'size' in parsed_file
    
    # 元數據斷言
    assert 'package' in parsed_file
    assert 'imports' in parsed_file
    assert 'classes' in parsed_file
    
    # 如果有類，測試類的元數據
    if parsed_file['classes']:
        test_class = parsed_file['classes'][0]
        assert 'name' in test_class
        assert 'modifiers' in test_class
        assert 'fields' in test_class
        assert 'methods' in test_class
        
        # 如果有方法，測試方法的元數據
        if test_class['methods']:
            test_method = test_class['methods'][0]
            assert 'name' in test_method
            assert 'parameters' in test_method
            assert 'modifiers' in test_method
            assert 'body' in test_method
            assert 'start_line' in test_method
            assert 'end_line' in test_method
            
            print(f"Successfully parsed file: {java_file}")
            print(f"Found class: {test_class['name']} with {len(test_class['methods'])} methods")

if __name__ == '__main__':
    pytest.main(['-v', __file__]) 