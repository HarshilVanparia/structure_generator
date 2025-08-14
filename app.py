#!/usr/bin/env python3
"""
Dynamic Project Structure Generator
Handles any project structure format with comments support
Fixed path parsing to avoid folder/file duplication issues
"""

import os
import re
import json
from pathlib import Path

class ProjectStructureGenerator:
    """
    Dynamic project structure generator with fixed path handling.
    Handles folder/file paths correctly without duplication issues.
    """

    def __init__(self, base_path="."):
        self.base_path = Path(base_path).resolve()

    def detect_input_format(self, input_text: str) -> str:
        input_text = input_text.strip()
        if input_text.startswith('{') and input_text.endswith('}'):
            return 'json'
        elif '│' in input_text or '├' in input_text or '└' in input_text:
            return 'unix_tree'
        elif 'PATH listing' in input_text or 'Volume serial' in input_text:
            return 'windows_tree'
        elif ':' in input_text and '\n' in input_text:
            return 'yaml_like'
        else:
            return 'simple_list'

    def strip_comment(self, line: str) -> str:
        """Remove in-line comments and trailing whitespace."""
        comment_pos = line.find('#')
        if comment_pos != -1:
            return line[:comment_pos].rstrip()
        return line.rstrip()

    def parse_json_structure(self, json_input: str) -> dict:
        try:
            return json.loads(json_input)
        except Exception as e:
            raise ValueError(f"Invalid JSON: {e}")

    def parse_simple_list(self, list_input: str) -> dict:
        lines = []
        for line in list_input.strip().split('\n'):
            cleaned = self.strip_comment(line).strip()
            if cleaned:
                lines.append(cleaned)
        structure = {}
        for line in lines:
            parts = [p for p in line.replace('\\', '/').split('/') if p]
            current = structure
            # Navigate through all parts except the last one (create folders)
            for i, part in enumerate(parts[:-1]):
                if part not in current:
                    current[part] = {'type': 'folder', 'contents': {}}
                current = current[part]['contents']
            # Handle the last part
            if parts:
                last_part = parts[-1]
                if '.' in last_part:  # It's a file
                    current[last_part] = {'type': 'file'}
                else:  # It's a folder
                    if last_part not in current:
                        current[last_part] = {'type': 'folder', 'contents': {}}
        return structure

    def parse_unix_tree_structure(self, tree_input: str) -> dict:
        lines = tree_input.strip().split('\n')
        structure = {}
        path_stack = []
        for line in lines:
            line = self.strip_comment(line)
            if not line.strip():
                continue
            if re.match(r'^\d+\s+(directories|files)', line):
                continue
            clean_line = re.sub(r'^[│├└─\s]*', '', line).strip()
            if not clean_line:
                continue
            tree_chars = re.findall(r'[│├└]', line)
            level = len(tree_chars)
            path_stack = path_stack[:level]
            if clean_line.endswith('/'):
                folder_name = clean_line.rstrip('/')
                path_stack.append(folder_name)
                self._add_to_structure(structure, path_stack[:-1], 'folder', folder_name)
            else:
                if '.' in clean_line:
                    self._add_to_structure(structure, path_stack, 'file', clean_line)
                else:
                    path_stack.append(clean_line)
                    self._add_to_structure(structure, path_stack[:-1], 'folder', clean_line)
        return structure

    def parse_tree_structure(self, tree_input: str) -> dict:
        lines = []
        for line in tree_input.strip().split('\n'):
            if ('PATH listing' not in line and
                'Volume serial' not in line and
                'Folder PATH' not in line and
                line.strip()):
                lines.append(line)
        return self.parse_unix_tree_structure('\n'.join(lines))
    
    def parse_yaml_like_structure(self, yaml_input: str) -> dict:
        lines = []
        for line in yaml_input.strip().split('\n'):
            cleaned = self.strip_comment(line)
            if cleaned.strip():
                lines.append(cleaned)
        structure = {}
        path_stack = []
        for line in lines:
            indent = len(line) - len(line.lstrip())
            level = indent // 2  # Assuming 2 spaces per level
            item = line.strip().rstrip(':').rstrip('/')
            if not item:
                continue
            path_stack = path_stack[:level]
            if line.strip().endswith('/') or line.strip().endswith(':'):
                path_stack.append(item)
                self._add_to_structure(structure, path_stack[:-1], 'folder', item)
            else:
                if '.' in item:
                    self._add_to_structure(structure, path_stack, 'file', item)
                else:
                    path_stack.append(item)
                    self._add_to_structure(structure, path_stack[:-1], 'folder', item)
        return structure

    def _add_to_structure(self, structure: dict, path: list, item_type: str, name: str):
        current = structure
        for folder in path:
            if folder not in current:
                current[folder] = {'type': 'folder', 'contents': {}}
            current = current[folder]['contents']
        if item_type == 'folder':
            if name not in current:
                current[name] = {'type': 'folder', 'contents': {}}
        elif item_type == 'file':
            current[name] = {'type': 'file'}

    def get_file_content_by_extension(self, file_path: Path) -> str:
        extension = file_path.suffix.lower()
        filename = file_path.stem
        content_templates = {
            '.py': f'''#!/usr/bin/env python3
\"\"\"
{filename}.py - Auto-generated Python module
\"\"\"

def main():
    \"\"\"Main function\"\"\"
    pass

if __name__ == \"__main__\":
    main()
''',
            '.php': f'''<?php
/**
 * {filename}.php - Auto-generated PHP file
 */

// Add your PHP code here

?>
''',
            '.js': f'''/**
 * {filename}.js - Auto-generated JavaScript file
 */

console.log("Hello from {filename}.js");
''',
            '.css': f'''/* {filename}.css - Auto-generated CSS file */

body {{
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 20px;
}}
''',
            '.html': f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{filename}</title>
</head>
<body>
    <h1>{filename}</h1>
    <p>Auto-generated HTML file</p>
</body>
</html>
''',
            '.md': f'''# {filename}

Auto-generated Markdown file.

## Description

This file was automatically created by the Project Structure Generator.
''',
            '.txt': f'''This is {filename}.txt - Auto-generated text file.

You can add your content here.
''',
            '.json': f'''{{"name": "{filename}", "description": "Auto-generated JSON file"}}''',
            '.htaccess': '''# Auto-generated .htaccess file
RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^(.*)$ index.php [QSA,L]
''',
        }
        return content_templates.get(extension, f"# {filename}\n\nAuto-generated file: {file_path.name}\n")

    def create_structure(self, structure: dict, current_path=None, default_file_content=""):
        if current_path is None:
            current_path = self.base_path
        for name, item in structure.items():
            item_path = current_path / name
            if item['type'] == 'folder':
                item_path.mkdir(parents=True, exist_ok=True)
                print(f"Created folder: {item_path}")
                if 'contents' in item and item['contents']:
                    self.create_structure(item['contents'], item_path, default_file_content)
            elif item['type'] == 'file':
                item_path.parent.mkdir(parents=True, exist_ok=True)
                if default_file_content:
                    content = default_file_content
                else:
                    content = self.get_file_content_by_extension(item_path)
                with open(item_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Created file: {item_path}")

    def preview_structure(self, structure: dict, indent="") -> str:
        preview = ""
        for name, item in structure.items():
            if item['type'] == 'folder':
                preview += f"{indent}📁 {name}/\n"
                if 'contents' in item and item['contents']:
                    preview += self.preview_structure(item['contents'], indent + "  ")
            else:
                preview += f"{indent}📄 {name}\n"
        return preview

    def generate(self, input_text, target_folder="generated_project", file_content=""):
        print(f"Input text preview:\n{input_text[:200]}...\n")
        fmt = self.detect_input_format(input_text)
        print(f"Detected format: {fmt}")
        if fmt == 'json':
            structure = self.parse_json_structure(input_text)
        elif fmt == 'unix_tree':
            structure = self.parse_unix_tree_structure(input_text)
        elif fmt == 'windows_tree':
            structure = self.parse_tree_structure(input_text)
        elif fmt == 'yaml_like':
            structure = self.parse_yaml_like_structure(input_text)
        else:
            structure = self.parse_simple_list(input_text)
        print(f"\nParsed structure preview:")
        print(self.preview_structure(structure))
        self.base_path = Path(target_folder).resolve()
        print(f"\nCreating structure in: {self.base_path}")
        print("-" * 50)
        self.create_structure(structure, default_file_content=file_content)  # ✅ Fixed line
        print("-" * 50)
        print(f"Project structure generated successfully at: {self.base_path}")


def main():
    print("=== Dynamic Project Structure Generator ===")
    print("Supports: tree output, simple paths, YAML-like, JSON")
    print("Comments (# ...) are automatically stripped")
    print("\nPaste your project structure below (end with double Enter):")

    lines = []
    while True:
        try:
            line = input()
            if line.strip() == "" and lines and lines[-1].strip() == "":
                break
            lines.append(line)
        except (EOFError, KeyboardInterrupt):
            break

    input_text = "\n".join(lines[:-1]) if lines else ""  # Remove last empty line
    if not input_text.strip():
        print("No input provided!")
        return

    generator = ProjectStructureGenerator()
    try:
        # Detect structure format and parse it
        fmt = generator.detect_input_format(input_text)
        if fmt == 'json':
            structure = generator.parse_json_structure(input_text)
        elif fmt == 'unix_tree':
            structure = generator.parse_unix_tree_structure(input_text)
        elif fmt == 'windows_tree':
            structure = generator.parse_tree_structure(input_text)
        elif fmt == 'yaml_like':
            structure = generator.parse_yaml_like_structure(input_text)
        else:
            structure = generator.parse_simple_list(input_text)

        print(f"\nParsed structure preview:")
        print(generator.preview_structure(structure))

        # Use first folder name as the target folder
        if not structure:
            print("Error: Parsed structure is empty.")
            return

        first_item = next(iter(structure))
        if structure[first_item]['type'] == 'folder':
            target = first_item
            structure = structure[first_item]['contents']  # ✅ Drop top-level folder from structure
        else:
            target = "generated_project"

        generator.base_path = Path(target).resolve()

        print(f"\nCreating structure in: {generator.base_path}")
        print("-" * 50)
        generator.create_structure(structure, default_file_content="")  # Always use default content
        print("-" * 50)
        print(f"Project structure generated successfully at: {generator.base_path}")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
