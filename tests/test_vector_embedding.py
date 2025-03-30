import pytest
from unittest.mock import Mock, patch, AsyncMock
from src.services.vector_embedding import VectorEmbeddingService
from src.type_definitions.code_types import CodeInfo
import numpy as np

# 簡單的測試數據
SAMPLE_CODE = """
public class SimpleTest {
    private String name;
    
    public void test() {
        System.out.println("test");
    }
}
"""

# 模擬 embedding 維度
EMBEDDING_DIM = 3072

@pytest.fixture
def mock_embedding():
    """創建模擬的 embedding 向量"""
    return list(np.random.rand(EMBEDDING_DIM))

@pytest.fixture
def code_info() -> CodeInfo:
    """創建測試用的代碼信息"""
    return {
        'content': SAMPLE_CODE,
        'file_path': 'test/SimpleTest.java',
        'type': 'class',
        'name': 'SimpleTest',
        'start_line': 1,
        'end_line': 7,
        'package': 'com.test'
    }

def test_preprocess_code():
    """測試代碼預處理功能"""
    with patch('src.services.vector_embedding.GoogleGenerativeAIEmbeddings'):
        service = VectorEmbeddingService()
        
        # 測試空白行和空格處理
        input_code = "\n  public void test()  {\n\n    test();\n\n}\n"
        processed = service._preprocess_code(input_code)
        expected = "public void test() {\n    test();\n}"
        
        assert processed.strip() == expected.strip()
        print(f"Preprocessed code test passed. Input:\n{input_code}\nOutput:\n{processed}")

@pytest.mark.asyncio
async def test_metadata_creation(code_info):
    """測試元數據創建"""
    with patch('src.services.vector_embedding.GoogleGenerativeAIEmbeddings'):
        service = VectorEmbeddingService()
        metadata = service._create_metadata(code_info)
        
        # 驗證元數據字段
        assert metadata['file_path'] == code_info['file_path']
        assert metadata['type'] == code_info['type']
        assert metadata['name'] == code_info['name']
        print(f"Metadata creation test passed. Created metadata: {metadata}")

@pytest.mark.asyncio
async def test_embedding_generation(mock_embedding):
    """測試 embedding 生成（使用 mock）"""
    with patch('src.services.vector_embedding.GoogleGenerativeAIEmbeddings') as mock_embeddings:
        # 設置 mock 返回值
        mock_instance = AsyncMock()
        mock_instance.aembed_query.return_value = mock_embedding
        mock_embeddings.return_value = mock_instance
        
        service = VectorEmbeddingService()
        embedding = await service.generate_embedding("test code")
        
        assert isinstance(embedding, list)
        assert len(embedding) == EMBEDDING_DIM
        print(f"Embedding generation test passed. Embedding dimension: {len(embedding)}")

@pytest.mark.asyncio
async def test_batch_embedding_generation(mock_embedding):
    """測試批量 embedding 生成（使用 mock）"""
    with patch('src.services.vector_embedding.GoogleGenerativeAIEmbeddings') as mock_embeddings:
        # 設置 mock 返回值
        mock_instance = AsyncMock()
        mock_instance.aembed_documents.return_value = [mock_embedding, mock_embedding]
        mock_embeddings.return_value = mock_instance
        
        service = VectorEmbeddingService()
        embeddings = await service.generate_embeddings_batch(["test1", "test2"])
        
        assert isinstance(embeddings, list)
        assert len(embeddings) == 2
        assert all(isinstance(emb, list) for emb in embeddings)
        assert all(len(emb) == EMBEDDING_DIM for emb in embeddings)
        print(f"Batch embedding generation test passed. Number of embeddings: {len(embeddings)}")

@pytest.mark.asyncio
async def test_process_code_chunk(code_info, mock_embedding):
    """測試完整的代碼處理流程"""
    with patch('src.services.vector_embedding.GoogleGenerativeAIEmbeddings') as mock_embeddings:
        # 設置 mock 返回值
        mock_instance = AsyncMock()
        mock_instance.aembed_query.return_value = mock_embedding
        mock_embeddings.return_value = mock_instance
        
        service = VectorEmbeddingService()
        result = await service.process_code_chunk(code_info)
        
        assert 'embedding' in result
        assert 'metadata' in result
        assert 'content' in result
        assert result['metadata']['name'] == code_info['name']
        assert len(result['embedding']) == EMBEDDING_DIM
        print(f"Code chunk processing test passed. Result structure: {list(result.keys())}")

if __name__ == '__main__':
    pytest.main(['-v', __file__]) 