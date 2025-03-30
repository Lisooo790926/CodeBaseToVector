import pytest
from unittest.mock import Mock, patch, AsyncMock
from pathlib import Path
from src.services.codebase_service import CodebaseService
from src.type_definitions.code_types import CodeMetadata, ClassInfo, MethodInfo, FieldInfo

# Mock data
MOCK_JAVA_FILE = """
package com.example;

public class TestClass {
    private String name;
    
    public void test() {
        System.out.println("test");
    }
}
"""

@pytest.fixture
def mock_services():
    """Create mock services for testing."""
    with patch('src.services.service_factory.ServiceFactory') as mock_factory:
        # Mock vector storage service
        mock_storage = Mock()
        mock_storage.delete_project_vectors.return_value = True
        mock_storage.store_vectors.return_value = True
        mock_factory.get_vector_storage.return_value = mock_storage

        # Mock vector embedding service
        mock_embedding = AsyncMock()
        mock_embedding.generate_embedding.return_value = [0.1] * 3072
        mock_factory.get_vector_embedding.return_value = mock_embedding

        # Mock Java code parser
        mock_parser = Mock()
        mock_parser.parse_directory.return_value = [
            CodeMetadata(
                file_path="test/TestClass.java",
                content=MOCK_JAVA_FILE,
                size=8,
                package="com.example",
                imports=[],
                classes=[
                    ClassInfo(
                        name="TestClass",
                        type="class",
                        modifiers=["public"],
                        fields=[
                            FieldInfo(
                                name="name",
                                type="field",
                                modifiers=["private"],
                                body="private String name;"
                            )
                        ],
                        methods=[
                            MethodInfo(
                                name="test",
                                type="method",
                                return_type="void",
                                parameters=[],
                                modifiers=["public"],
                                body="public void test() { System.out.println(\"test\"); }"
                            )
                        ],
                        start_line=3,
                        end_line=9,
                        body=MOCK_JAVA_FILE
                    )
                ]
            )
        ]
        mock_factory.get_java_code_parser.return_value = mock_parser

        yield {
            'vector_storage': mock_storage,
            'vector_embedding': mock_embedding,
            'java_code_parser': mock_parser
        }

@pytest.fixture
def codebase_service(mock_services):
    """Create a CodebaseService instance with mocked dependencies."""
    codebase_service = CodebaseService()
    codebase_service.vector_storage = mock_services['vector_storage']
    codebase_service.vector_embedding = mock_services['vector_embedding']
    codebase_service.java_code_parser = mock_services['java_code_parser']
    return codebase_service

@pytest.fixture
def temp_java_project(tmp_path):
    """Create a temporary Java project structure."""
    project_dir = tmp_path / "test_project"
    project_dir.mkdir()
    
    # Create a Java file
    src_dir = project_dir / "src" / "main" / "java" / "com" / "example"
    src_dir.mkdir(parents=True)
    
    test_file = src_dir / "TestClass.java"
    test_file.write_text(MOCK_JAVA_FILE)
    
    # Create some directories that should be ignored
    (project_dir / "target").mkdir()
    (project_dir / "build").mkdir()
    
    return project_dir

@pytest.mark.asyncio
async def test_find_java_files(codebase_service, temp_java_project):
    """Test finding Java files in a directory."""
    java_files = codebase_service._find_java_files(str(temp_java_project))
    
    assert len(java_files) == 1
    assert java_files[0].endswith("TestClass.java")
    assert "target" not in java_files[0]
    assert "build" not in java_files[0]

@pytest.mark.asyncio
async def test_update_codebase(codebase_service, temp_java_project):
    """Test updating codebase vectors."""
    result = await codebase_service.update_codebase(
        project_name="test_project",
        root_path=str(temp_java_project)
    )
    
    assert result is True
    
    # Verify service calls
    codebase_service.vector_storage.delete_project_vectors.assert_called_once()
    codebase_service.java_code_parser.parse_directory.assert_called_once()
    assert codebase_service.vector_embedding.generate_embedding.call_count == 1
    codebase_service.vector_storage.store_vectors.assert_called_once()

@pytest.mark.asyncio
async def test_query_codebase(codebase_service):
    """Test querying codebase."""
    # Mock search results
    codebase_service.vector_storage.search_vectors.return_value = [
        {
            "score": 0.9,
            "metadata": {
                "file_path": "test/TestClass.java",
                "code_type": "class",
                "package": "com.example",
                "class_name": "TestClass"
            }
        }
    ]
    
    results = await codebase_service.query_codebase(
        project_name="test_project",
        question="What does the test method do?"
    )
    
    assert len(results) == 1
    assert results[0]["score"] == 0.9
    assert results[0]["metadata"]["class_name"] == "TestClass"
    
    # Verify service calls
    codebase_service.vector_embedding.generate_embedding.assert_called_once()
    codebase_service.vector_storage.search_vectors.assert_called_once()

@pytest.mark.asyncio
async def test_update_codebase_with_errors(codebase_service, temp_java_project):
    """Test handling errors during codebase update."""
    # Mock an error in vector storage
    codebase_service.vector_storage.store_vectors.return_value = False
    
    result = await codebase_service.update_codebase(
        project_name="test_project",
        root_path=str(temp_java_project)
    )
    
    assert result is False

@pytest.mark.asyncio
async def test_query_codebase_with_errors(codebase_service, mock_services):
    """Test handling errors during codebase query."""
    # Mock an error in embedding generation
    codebase_service.vector_embedding.generate_embedding.side_effect = Exception("Test error")
    
    results = await codebase_service.query_codebase(
        project_name="test_project",
        question="What does the test method do?"
    )
    
    assert len(results) == 0 