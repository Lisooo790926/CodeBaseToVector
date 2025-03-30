import os
from pathlib import Path
from typing import List, Dict, Optional, Any
import logging

from src.type_definitions.code_types import ClassInfo, CodeMetadata, FieldInfo, MethodInfo, ParameterInfo

from src.config.settings import settings
from tree_sitter_languages import get_language, get_parser

class JavaCodeParser:
    """Parser for Java source code using tree-sitter.
    
    This class provides functionality to parse Java source files and extract
    structural information such as classes, methods, and fields.
    """
    
    def __init__(self):
        """Initialize the Java code parser with tree-sitter."""
        try:
            self.JAVA_LANGUAGE = get_language('java')
            self.parser = get_parser('java')
            self.logger = logging.getLogger(__name__)
        except Exception as e:
            self.logger.error(f"Failed to initialize Java parser: {str(e)}")
            raise

    def _extract_node_text(self, node: Any, content: bytes) -> str:
        """Extract text from a tree-sitter node.
        
        Args:
            node: Tree-sitter node
            content: Source file content in bytes
            
        Returns:
            Extracted text as string
        """
        return content[node.start_byte:node.end_byte].decode('utf-8')

    def _extract_parameters(self, params_node: Any, content: bytes) -> List[Dict[str, str]]:
        """Extract method parameters from a formal_parameters node.
        
        Args:
            params_node: Tree-sitter node containing formal parameters
            content: Source file content in bytes
            
        Returns:
            List of parameter information dictionaries
        """
        parameters = []
        for param in params_node.children:
            if param.type == 'formal_parameter':
                param_info = self._extract_parameter_info(param, content)
                if param_info:
                    parameters.append(param_info)
        return parameters

    def _extract_parameter_info(self, param_node: Any, content: bytes) -> Optional[Dict[str, str]]:
        """Extract information from a single parameter node.
        
        Args:
            param_node: Tree-sitter node for a single parameter
            content: Source file content in bytes
            
        Returns:
            Parameter information dictionary or None if incomplete
        """
        param_type = None
        param_name = None

        
        for param_child in param_node.children:
            if param_child.type == 'type_identifier':
                param_type = self._extract_node_text(param_child, content)
            elif param_child.type == 'identifier':
                param_name = self._extract_node_text(param_child, content)
                
        if param_type and param_name:
            return ParameterInfo(
                type=param_type, 
                name=param_name,
                start_line=param_node.start_point[0],
                end_line=param_node.end_point[0],
                body=self._extract_node_text(param_node, content)
            )
        return None

    def _extract_modifiers(self, modifiers_node: Any, content: bytes) -> List[str]:
        """Extract modifiers (public, private, static, etc.) from a modifiers node.
        
        Args:
            modifiers_node: Tree-sitter node containing modifiers
            content: Source file content in bytes
            
        Returns:
            List of modifier strings
        """
        return [self._extract_node_text(modifier, content) 
                for modifier in modifiers_node.children]

    def _extract_method_info(self, method_node: Any, content: bytes) -> MethodInfo:
        """Extract information from a method declaration node.
        
        Args:
            method_node: Tree-sitter node for method declaration
            content: Source file content in bytes
            
        Returns:
            Dictionary containing method information
        """
        method_info = MethodInfo(
            name='',
            type='method',
            return_type='',
            parameters=[],
            modifiers=[],
            start_line=method_node.start_point[0],
            end_line=method_node.end_point[0],
            body=self._extract_node_text(method_node, content)
        )

        for child in method_node.children:
            if child.type == 'identifier':
                method_info.name = self._extract_node_text(child, content)
            elif child.type == 'modifiers':
                method_info.modifiers = self._extract_modifiers(child, content)
            elif child.type == 'formal_parameters':
                method_info.parameters = self._extract_parameters(child, content)
            elif child.type == 'type_identifier':
                method_info.return_type = self._extract_node_text(child, content)

        return method_info

    def _extract_field_info(self, field_node: Any, content: bytes) -> FieldInfo:
        """Extract information from a field declaration node.
        
        Args:
            field_node: Tree-sitter node for field declaration
            content: Source file content in bytes
            
        Returns:
            Dictionary containing field information
        """
        field_info = FieldInfo(
            type='field',
            name='',
            start_line=field_node.start_point[0],
            end_line=field_node.end_point[0],
            body=self._extract_node_text(field_node, content),
            modifiers=[]
        )

        for child in field_node.children:
            if child.type == 'modifiers':
                field_info.modifiers = self._extract_modifiers(child, content)
            elif child.type == 'type_identifier':
                field_info.type = self._extract_node_text(child, content)
            elif child.type == 'variable_declarator':
                for var_child in child.children:
                    if var_child.type == 'identifier':
                        field_info.name = self._extract_node_text(var_child, content)

        return field_info

    def _extract_class_info(self, class_node: Any, content: bytes) -> ClassInfo:
        """Extract information from a class declaration node.
        
        Args:
            class_node: Tree-sitter node for class declaration
            content: Source file content in bytes
            
        Returns:
            Dictionary containing class information
        """
        class_info = ClassInfo(
            name='',
            type='class',
            modifiers=[],
            fields=[],
            methods=[],
            start_line=class_node.start_point[0],
            end_line=class_node.end_point[0], 
            body=self._extract_node_text(class_node, content)
        )

        for child in class_node.children:
            if child.type == 'identifier':
                class_info.name = self._extract_node_text(child, content)
            elif child.type == 'modifiers':
                class_info.modifiers = self._extract_modifiers(child, content)
            elif child.type == 'class_body':
                self._process_class_body(child, content, class_info)

        return class_info

    def _process_class_body(self, body_node: Any, content: bytes, class_info: ClassInfo) -> None:
        """Process the body of a class node to extract fields and methods.
        
        Args:
            body_node: Tree-sitter node for class body
            content: Source file content in bytes
            class_info: Dictionary to update with extracted information
        """
        for child in body_node.children:
            if child.type == 'field_declaration':
                field_info = self._extract_field_info(child, content)
                class_info.fields.append(field_info)
            elif child.type == 'method_declaration':
                method_info = self._extract_method_info(child, content)
                class_info.methods.append(method_info)

    def _extract_file_metadata(self, root_node: Any, content: bytes, file_info: CodeMetadata) -> None:
        """Extract package and import information from file.
        
        Args:
            root_node: Root tree-sitter node
            content: Source file content in bytes
            file_info: CodeMetadata object to update
        """
        for child in root_node.children:
            if child.type == 'package_declaration':
                for pkg_child in child.children:
                    if pkg_child.type == 'scoped_identifier':
                        file_info.package = self._extract_node_text(pkg_child, content)
            elif child.type == 'import_declaration':
                for imp_child in child.children:
                    if imp_child.type == 'scoped_identifier':
                        file_info.imports.append(self._extract_node_text(imp_child, content))
            elif child.type == 'class_declaration':
                class_info = self._extract_class_info(child, content)
                file_info.classes.append(class_info)

    def parse_file(self, file_path: str) -> Optional[CodeMetadata]:
        """Parse a single Java file and extract its structure.
        
        Args:
            file_path: Path to the Java file
            
        Returns:
            Dictionary containing the parsed content or None if parsing fails
        """
        try:
            with open(file_path, 'rb') as f:
                content = f.read()

            print(f"Parsing file {file_path}")
            file_info = CodeMetadata(
                file_path=file_path,
                content=content.decode('utf-8'),
                size=len(content.splitlines()),
                classes=[],
                imports=[],
                package=""
            )

            tree = self.parser.parse(content)
            self._extract_file_metadata(tree.root_node, content, file_info)

            self.logger.debug(f"Parsed file {file_path} with metadata: {file_info}")
            
            return file_info

        except Exception as e:
            self.logger.error(f"Error parsing file {file_path}: {str(e)}")
            return None

    def parse_directory(self, directory_path: str) -> List[CodeMetadata]:
        """Parse all Java files in a directory.
        
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
            self.logger.error(f"Error parsing directory {directory_path}: {str(e)}")
        
        return parsed_files 