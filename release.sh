#!/bin/bash

# Verifica se o número da versão foi fornecido
if [ -z "$1" ]; then
    echo "Uso: ./release.sh <número-da-versão>"
    exit 1
fi

# Inclua o token do GitHub usando o comando abaixo:
# export GITHUB_TOKEN="..."

# Configurações
VERSION="$1"
CHANGELOG_FILE="CHANGELOG.md"
VERSION_FILE="VERSION"
REPO="marcelomdevasconcellos/emensageria"

# Obtém o token do GitHub do ambiente
if [ -z "$GITHUB_TOKEN" ]; then
    echo "A variável GITHUB_TOKEN não foi configurada."
    exit 1
fi

# Executa o quickcheck.sh e verifica se foi bem-sucedido
if ! bash quickcheck.sh; then
    echo "O quickcheck.sh encontrou problemas. Corrija-os antes de prosseguir com o release."
    exit 1
fi

# Função para gerar o changelog a partir dos PRs fechados
generate_changelog() {
    # Captura a data do último lançamento
    LAST_RELEASE_DATE=$(gh release list --repo "$REPO" --limit 1 --json publishedAt --jq '.[0].publishedAt')

    # Adiciona título da nova versão ao changelog temporário
    echo "## Versão $VERSION - $(date +'%Y-%m-%d')" > temp_changelog.md
    echo "" >> temp_changelog.md

    # Listar PRs mesclados após a última data de lançamento
    gh pr list -s merged -L 100 --json title,number,mergedAt --jq \
        ".[] | select(.mergedAt > \"$LAST_RELEASE_DATE\") | \"* PR #\(.number): \(.title) \"" \
        --repo "$REPO" >> temp_changelog.md

    if [ $? -ne 0 ]; then
        echo "Erro ao gerar o changelog."
        exit 1
    fi

    echo "" >> temp_changelog.md
    cat "$CHANGELOG_FILE" >> temp_changelog.md
    mv temp_changelog.md "$CHANGELOG_FILE"
    echo "Changelog atualizado no $CHANGELOG_FILE."
}

# Função para atualizar o arquivo de versão
update_version_file() {
    echo "$VERSION" > "$VERSION_FILE"
    echo "Arquivo de versão atualizado para $VERSION."
}

# Função para criar uma release no GitHub
create_github_release() {
    gh release create "$VERSION" --title "Versão $VERSION" --notes-file "$CHANGELOG_FILE" --repo "$REPO"
    if [ $? -ne 0 ]; then
        echo "Erro ao criar a release no GitHub."
        exit 1
    fi
    echo "Release $VERSION criada com sucesso no GitHub."
}

# Função principal
main() {
    generate_changelog
    update_version_file
    git add "$CHANGELOG_FILE" "$VERSION_FILE"
    git commit -m "Atualiza para versão $VERSION"
    git push
    create_github_release
}

# Executa o script principal
main
