import os

def build_repo_context(root_dir, target_extensions=['.py', '.js', '.sql', '.html']):
    """
    Recorre un directorio y concatena el contenido de los archivos 
    relevantes en un formato que Nemotron pueda entender.
    """
    context = "ESTRUCTURA DEL REPOSITORIO Y CÓDIGO FUENTE:\n\n"
    
    # Carpetas a ignorar para no desperdiciar tokens
    exclude_dirs = {'.git', '__pycache__', 'node_modules', 'venv', 'env', 'dist'}

    for root, dirs, files in os.walk(root_dir):
        # Filtrar directorios ignorados
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for file in files:
            if any(file.endswith(ext) for ext in target_extensions):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, root_dir)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        context += f"--- ARCHIVO: {relative_path} ---\n"
                        context += content + "\n\n"
                except Exception as e:
                    print(f"Error leyendo {file_path}: {e}")
                    
    return context

# Ejemplo de uso:
# repo_text = build_repo_context("./mi-proyecto-web")
