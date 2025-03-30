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
    assert parsed_file.file_path == java_file
    assert parsed_file.content is not None
    assert parsed_file.size is not None
    
    # 元數據斷言
    assert parsed_file.package is not None
    assert parsed_file.imports is not None
    assert parsed_file.classes is not None
    
    # 如果有類，測試類的元數據
    if parsed_file.classes:
        test_class = parsed_file.classes[0]
        assert test_class.name is not None
        assert test_class.modifiers is not None
        assert test_class.fields is not None
        assert test_class.methods is not None
        
        # 如果有方法，測試方法的元數據
        if test_class.methods:
            test_method = test_class.methods[0]
            assert test_method.name is not None
            assert test_method.parameters is not None
            assert test_method.modifiers is not None
            assert test_method.body is not None
            assert test_method.start_line is not None
            assert test_method.end_line is not None
            
            print(f"Successfully parsed file: {java_file}")
            print(f"Found class: {test_class.name} with {len(test_class.methods)} methods")

if __name__ == '__main__':
    pytest.main(['-v', __file__]) 