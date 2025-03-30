import pytest
from src.services.vector_storage import VectorStorageService, CodeVectorMetadata

# Dummy classes to simulate Qdrant client behavior
class DummyHit:
    def __init__(self, score, payload):
        self.score = score
        self.payload = payload

class DummyCollections:
    def __init__(self, collections):
        self.collections = collections

class DummyCollection:
    def __init__(self, name):
        self.name = name

class DummyQdrantClient:
    def __init__(self):
        self.create_collection_called = False
        self.upsert_called = False
        self.search_called = False
        self.delete_called = False
        self.get_collections_called = False

    def create_collection(self, collection_name, vectors_config):
        self.create_collection_called = True

    def upsert(self, collection_name, points):
        self.upsert_called = True

    def search(self, collection_name, query_vector, limit, **kwargs):
        self.search_called = True
        # simulate returning a list of dummy hit objects
        dummy_hit = DummyHit(score=0.9, payload={'project_name': 'test_project', 'data': 'example'})
        return [dummy_hit]

    def delete(self, collection_name, points_selector):
        self.delete_called = True

    def get_collections(self):
        self.get_collections_called = True
        # Simulate returning collection data
        dummy_coll = DummyCollection("existing_collection")
        return DummyCollections(collections=[dummy_coll])


@pytest.fixture
def vector_storage_service():
    # Create a VectorStorageService instance with a dummy Qdrant client
    service = VectorStorageService(host="localhost", port=6333)
    service.client = DummyQdrantClient()
    return service


def test_create_collection(vector_storage_service):
    result = vector_storage_service.create_collection("test_collection", vector_size=512)
    assert result is True
    assert vector_storage_service.client.create_collection_called is True


def test_store_vectors(vector_storage_service):
    vectors = [[0.1, 0.2, 0.3]]
    metadata = [
        CodeVectorMetadata(
            file_path="dummy.java",
            code_type="method",
            code_content="void dummy() {}",
            language="java",
            project_name="test_project"
        )
    ]
    result = vector_storage_service.store_vectors("test_collection", vectors, metadata)
    assert result is True
    assert vector_storage_service.client.upsert_called is True


def test_search_vectors(vector_storage_service):
    query_vector = [0.1, 0.2, 0.3]
    results = vector_storage_service.search_vectors("test_collection", query_vector, limit=1, project_name="test_project")
    assert isinstance(results, list)
    assert len(results) == 1
    hit = results[0]
    assert "score" in hit and "metadata" in hit
    # Check if the metadata contains the expected project name
    project_name = hit['metadata'].get('project_name')
    assert project_name == 'test_project'


def test_delete_project_vectors(vector_storage_service):
    result = vector_storage_service.delete_project_vectors("test_collection", "test_project")
    assert result is True
    assert vector_storage_service.client.delete_called is True


def test_collection_exists(vector_storage_service):
    exists = vector_storage_service.collection_exists("existing_collection")
    assert exists is True
    not_exists = vector_storage_service.collection_exists("non_existing_collection")
    assert not_exists is False 