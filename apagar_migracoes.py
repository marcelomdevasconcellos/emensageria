import os

def apagar_migracoes():
    # Percorre todos os diretórios e subdiretórios
    for root, dirs, files in os.walk("."):
        if "migrations" in root and 'venv' not in root:
            # Verifica cada arquivo no diretório de migrações
            for file in files:
                if file != "__init__.py":
                    file_path = os.path.join(root, file)
                    print(f"Removendo {file_path}")
                    os.remove(file_path)

if __name__ == "__main__":
    apagar_migracoes()