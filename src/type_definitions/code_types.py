from typing import Any, Dict, List, Optional, TypedDict
from .code_types import ClassInfo, FieldInfo, MethodInfo, ParameterInfo
from pydantic import BaseModel

class BaseCode(BaseModel):
    """Base class for code elements.
    
    Attributes:
        name: Name of the code element
        start_line: Starting line number in the source file
        end_line: Ending line number in the source file
        body: Body of the code element
    """
    name: str
    type: str
    start_line: int
    end_line: int
    body: str

class CodeMetadata(BaseCode):
    """Type definition for code metadata.
    
    Attributes:
        file_path: Path to the source file
        package: Package name containing this code element
        imports: List of imports used in the code element
        classes: List of classes in the code element
    """
    file_path: str
    package: str
    imports: List[str]
    classes: List[ClassInfo]

    def __str__(self):
        return self.body

class ClassInfo(BaseCode):
    """Type definition for class information.
    
    Attributes:
        modifiers: List of modifiers for the class
        fields: List of fields in the class
        methods: List of methods in the class
    """
    modifiers: List[str]
    fields: List[FieldInfo]
    methods: List[MethodInfo]


class FieldInfo(BaseCode):
    """Type definition for field information.
    
    Attributes:
        modifiers: List of modifiers for the field
    """
    modifiers: List[str]

class MethodInfo(BaseCode):
    """Type definition for method information.

    Attributes:
        return_type: Return type of the method
        parameters: List of parameters for the method
        modifiers: List of modifiers for the method
    """
    return_type: str
    parameters: List[ParameterInfo]
    modifiers: List[str]

class ParameterInfo(BaseCode):
    """Type definition for parameter information."""

class CodeVectorMetadata(BaseModel):
    """Metadata for code vectors stored in Qdrant."""
    file_path: str
    code_type: str  # 'class', 'method', 'file'
    package: str
    class_name: str

    def __init__(self, code_metadata: CodeMetadata):
        self.file_path = code_metadata.file_path
        self.code_type = code_metadata.type
        self.package = code_metadata.package

        if code_metadata.classes:
            self.class_name = code_metadata.classes[0].name
            self.methods_name = [method.name for method in code_metadata.classes[0].methods] if code_metadata.classes[0].methods else []
            self.fields_name = [field.name for field in code_metadata.classes[0].fields] if code_metadata.classes[0].fields else []
        else:
            self.class_name = ""
            self.methods_name = []
            self.fields_name = []

class ProcessedCodeChunk(BaseModel):
    """Type definition for processed code chunk.
    
    Attributes:
        embedding: Vector representation of the code
        metadata: Associated metadata for the code chunk
        content: Original code content
    """
    embedding: List[float]
    metadata: CodeMetadata
    content: str 