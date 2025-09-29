# Conversor de Imagens JPEG para JPG

Um simples e eficiente conversor de imagens desenvolvido em Python que transforma arquivos JPEG em formato JPG.

## 📋 Descrição

Este projeto oferece uma solução prática para converter imagens do formato JPEG para JPG, mantendo a qualidade original da imagem. Ideal para padronização de arquivos de imagem ou para atender requisitos específicos de formato.

## 🚀 Funcionalidades

- ✅ Conversão de JPEG para JPG
- 📁 Processamento de diretórios completos
- 🎯 Preservação da qualidade da imagem
- 📊 Feedback de progresso durante a conversão
- 🔄 Criação automática de diretórios de saída

## 🛠️ Tecnologias Utilizadas

- **Python 3.x**
- **Pillow (PIL)** - Biblioteca para processamento de imagens

## 📦 Instalação

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/leotech-projects/conversao.git
   cd conversao
   ```

2. **Crie um ambiente virtual (recomendado):**
   ```bash
   python -m venv .venv
   ```

3. **Ative o ambiente virtual:**
   - **Windows:**
     ```powershell
     .venv\Scripts\Activate.ps1
     ```
   - **Linux/Mac:**
     ```bash
     source .venv/bin/activate
     ```

4. **Instale as dependências:**
   ```bash
   pip install Pillow
   ```

## 🎯 Como Usar

### Uso Básico

```bash
python converter_para_jpg.py
```

O script irá:
1. Procurar por arquivos JPEG na pasta `imagens_originais/`
2. Converter cada arquivo para formato JPG
3. Salvar os arquivos convertidos na pasta `imagens_convertidas/`

### Estrutura de Pastas

```
conversao/
├── converter_para_jpg.py
├── imagens_originais/
│   └── logo.jpeg           # Imagens de entrada
├── imagens_convertidas/
│   └── logo.jpg            # Imagens convertidas
└── README.md
```

## 📝 Exemplo de Uso

O projeto já inclui um exemplo prático:

- **Arquivo original:** `imagens_originais/logo.jpeg`
- **Arquivo convertido:** `imagens_convertidas/logo.jpg`

Simplesmente execute o script e veja a conversão acontecer!

## 🔧 Personalização

Você pode facilmente modificar o código para:

- Alterar os diretórios de entrada e saída
- Adicionar suporte para outros formatos de imagem
- Implementar redimensionamento de imagens
- Adicionar watermarks ou outros efeitos

### Exemplo de Modificação

```python
# Alterar diretórios
pasta_entrada = "suas_imagens/"
pasta_saida = "imagens_prontas/"

# Alterar qualidade da conversão
imagem.save(caminho_saida, "JPEG", quality=95)
```

## 📋 Requisitos do Sistema

- Python 3.6 ou superior
- Pillow 8.0 ou superior
- Sistema operacional: Windows, Linux ou macOS

## 🤝 Contribuição

Contribuições são sempre bem-vindas! Para contribuir:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 🐛 Problemas Conhecidos

- Certifique-se de que as pastas de entrada existem antes de executar
- Verifique as permissões de escrita na pasta de destino
- Alguns formatos de JPEG específicos podem necessitar ajustes

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👨‍💻 Autor

**Leonardo Silva** - [leotech-projects](https://github.com/leotech-projects)

## 🙏 Agradecimentos

- Comunidade Python pela excelente documentação
- Desenvolvedores da biblioteca Pillow
- Todos que contribuírem para melhorar este projeto

## 📞 Suporte

Se você encontrar algum problema ou tiver sugestões:

- Abra uma [Issue](https://github.com/leotech-projects/conversao/issues)
- Entre em contato através do GitHub

---

⭐ **Se este projeto foi útil para você, considere dar uma estrela!** ⭐