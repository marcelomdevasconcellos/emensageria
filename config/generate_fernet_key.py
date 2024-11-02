from pathlib import Path

from cryptography.fernet import Fernet


# Função para gerar a chave Fernet e salvar no arquivo .env
def generate_and_save_key():
    # Gerar a chave Fernet
    key = Fernet.generate_key().decode()

    # Caminho do arquivo .env
    env_path = Path('config/.env')

    # Verificar se o arquivo .env existe
    if not env_path.exists():
        print(f'Erro: O arquivo {env_path} não foi encontrado.')
        return

    # Ler o conteúdo do arquivo .env existente
    with open(env_path, 'r') as file:
        env_content = file.readlines()

    # Verificar se já existe uma chave CRYPTO_KEY
    found_key = False
    for i, line in enumerate(env_content):
        if line.startswith('CRYPTO_KEY='):
            # Atualizar a chave existente
            env_content[i] = f'CRYPTO_KEY={key}\n'
            found_key = True
            break

    # Se não encontrar, adicionar a chave ao final do arquivo
    if not found_key:
        env_content.append(f'CRYPTO_KEY={key}\n')

    # Salvar o conteúdo atualizado no arquivo .env
    with open(env_path, 'w') as file:
        file.writelines(env_content)

    print(f'Chave Fernet gerada e salva no arquivo .env: {key}')


# Executar a função
if __name__ == "__main__":
    generate_and_save_key()
