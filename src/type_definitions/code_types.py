from typing import List, TypedDict

class CodeMetadata(TypedDict):
    """Type definition for code metadata.
    
    Attributes:
        file_path: Path to the source file
        type: Type of the code element ('class', 'method', 'field' etc.)
        name: Name of the code element
        start_line: Starting line number in the source file
        end_line: Ending line number in the source file
        package: Package name containing this code element
    """
    file_path: str
    type: str
    name: str
    start_line: int
    end_line: int
    package: str

class CodeInfo(TypedDict):
    """Type definition for code information.
    
    Attributes:
        content: Actual code content
        file_path: Path to the source file
        type: Type of the code element
        name: Name of the code element
        start_line: Starting line number
        end_line: Ending line number
        package: Package name
    """
    content: str
    file_path: str
    type: str
    name: str
    start_line: int
    end_line: int
    package: str

class ProcessedCodeChunk(TypedDict):
    """Type definition for processed code chunk.
    
    Attributes:
        embedding: Vector representation of the code
        metadata: Associated metadata for the code chunk
        content: Original code content
    """
    embedding: List[float]
    metadata: CodeMetadata
    content: str 