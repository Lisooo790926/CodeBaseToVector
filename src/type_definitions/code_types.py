from typing import Any, List
from pydantic import BaseModel


class BaseCode(BaseModel):
    """Base class for code elements."""
    name: str
    type: str
    start_line: int = 0
    end_line: int = 0
    body: str = ""

    def __str__(self):
        return self.body
class ParameterInfo(BaseCode):
    """Type definition for parameter information."""
    pass

class MethodInfo(BaseCode):
    """Type definition for method information."""
    return_type: str = ""
    parameters: List[ParameterInfo] = []
    modifiers: List[str] = []


class FieldInfo(BaseCode):
    """Type definition for field information."""
    modifiers: List[str] = []


class ClassInfo(BaseCode):
    """Type definition for class information."""
    modifiers: List[str] = []
    fields: List[FieldInfo] = []
    methods: List[MethodInfo] = []


class CodeMetadata(BaseModel):
    """Type definition for code metadata."""
    file_path: str
    package: str = ""
    imports: List[str] = []
    classes: List[ClassInfo] = []
    content: str = ""
    size: int = 0

class CodeVectorMetadata(BaseModel):
    """Metadata for code vectors stored in Qdrant."""
    file_path: str
    code_type: str  # 'class', 'method', 'file'
    package: str = ""
    class_name: str = ""
    methods_name: List[str] = []
    fields_name: List[str] = []

    def __init__(self, code_metadata: CodeMetadata, **data: Any):
        super().__init__(**data)
        self.file_path = code_metadata.file_path
        self.code_type = code_metadata.type
        self.package = code_metadata.package

        if code_metadata.classes:
            self.class_name = code_metadata.classes[0].name
            self.methods_name = [method.name for method in code_metadata.classes[0].methods] if code_metadata.classes[0].methods else []
            self.fields_name = [field.name for field in code_metadata.classes[0].fields] if code_metadata.classes[0].fields else []


class ProcessedCodeChunk(BaseModel):
    """Type definition for processed code chunk."""
    content: str
    chunk_type: str
    name: str
    start_line: int
    end_line: int 