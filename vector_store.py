from typing import List, Dict
import os
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Qdrant
from dataclasses import dataclass
import inspect
import importlib.util
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class ApiSpec:
    path: str
    method: str
    required_params: List[str]
    optional_params: List[str] = None
    description: str = ""

class VectorApiRouter:
    def __init__(self, project_path: str, collection_name: str = None):
        # Initialize Gemini
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-exp-03-07")
        
        # Initialize Qdrant with environment variables
        self.qdrant_client = QdrantClient(
            host=os.getenv("QDRANT_HOST", "localhost"),
            port=int(os.getenv("QDRANT_PORT", 6333))
        )
        self.collection_name = collection_name or os.getenv("QDRANT_COLLECTION_NAME", "api_routes")
        
        # Create collection if it doesn't exist
        self._create_collection()
        
        # Load and index API specs from project structure
        self.api_specs = self._load_api_specs_from_project(project_path)
        self._index_api_specs()

    def _create_collection(self):
        """Create Qdrant collection with necessary parameters"""
        try:
            self.qdrant_client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=768, distance=Distance.COSINE)
            )
        except Exception:
            # Collection might already exist
            pass

    def _load_api_specs_from_project(self, project_path: str) -> Dict[str, ApiSpec]:
        """Load API specifications by analyzing the project structure"""
        api_specs = {}
        userinterface_path = Path(project_path) / "userinterface"
        
        if not userinterface_path.exists():
            raise ValueError(f"userinterface directory not found at {userinterface_path}")

        # Walk through all Python files in the userinterface directory
        for py_file in userinterface_path.rglob("*.py"):
            # Import the module
            spec = importlib.util.spec_from_file_location(py_file.stem, py_file)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Analyze each function in the module
                for name, obj in inspect.getmembers(module):
                    if inspect.isfunction(obj):
                        # Get function signature
                        sig = inspect.signature(obj)
                        doc = inspect.getdoc(obj) or ""
                        
                        # Extract parameters
                        required_params = []
                        optional_params = []
                        for param_name, param in sig.parameters.items():
                            if param.default == inspect.Parameter.empty:
                                required_params.append(param_name)
                            else:
                                optional_params.append(param_name)
                        
                        # Create route path based on file and function structure
                        route_path = f"/{py_file.parent.name}/{py_file.stem}/{name}"
                        
                        # Create ApiSpec
                        api_specs[name] = ApiSpec(
                            path=route_path,
                            method="GET",  # Default to GET, can be enhanced with decorators
                            required_params=required_params,
                            optional_params=optional_params,
                            description=doc
                        )
        
        return api_specs

    def _index_api_specs(self):
        """Index API specifications in the vector store"""
        texts = []
        metadatas = []
        
        for route_name, spec in self.api_specs.items():
            # Create a rich text description for the API
            text = f"API Route: {route_name}\nPath: {spec.path}\nMethod: {spec.method}\n"
            text += f"Required parameters: {', '.join(spec.required_params)}\n"
            if spec.optional_params:
                text += f"Optional parameters: {', '.join(spec.optional_params)}\n"
            if spec.description:
                text += f"Description: {spec.description}"
            
            texts.append(text)
            metadatas.append({"route_name": route_name})

        # Create vector store
        self.vector_store = Qdrant(
            client=self.qdrant_client,
            collection_name=self.collection_name,
            embeddings=self.embeddings
        )
        
        # Add texts to vector store
        self.vector_store.add_texts(texts=texts, metadatas=metadatas)

    def find_route(self, query: str) -> ApiSpec:
        """Find the most relevant API route based on the query"""
        results = self.vector_store.similarity_search_with_score(query, k=1)
        if not results:
            raise ValueError("No matching route found")
            
        doc, score = results[0]
        route_name = doc.metadata["route_name"]
        return self.api_specs[route_name] 