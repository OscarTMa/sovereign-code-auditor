import os

def build_repo_context(root_dir, target_extensions=['.py', '.js', '.sql', '.html', '.md']):
    """
    Scans a directory and concatenates relevant files into a structured context.
    """
    context = "REPOSITORY STRUCTURE AND SOURCE CODE:\n\n"
    exclude_dirs = {'.git', '__pycache__', 'node_modules', 'venv', 'env', 'dist', '.streamlit'}

    if not os.path.exists(root_dir):
        return "Error: Path does not exist."

    for root, dirs, files in os.walk(root_dir):
        # Filter out excluded directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for file in files:
            if any(file.endswith(ext) for ext in target_extensions):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, root_dir)
                
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        context += f"--- FILE: {relative_path} ---\n"
                        context += content + "\n\n"
                except Exception as e:
                    context += f"--- FILE: {relative_path} (Error reading file: {e}) ---\n\n"
                    
    return context
