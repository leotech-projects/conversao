from PIL import Image
import os

def converter_para_jpg(pasta_entrada, pasta_saida):
    # Cria a pasta de saída, se não existir
    os.makedirs(pasta_saida, exist_ok=True)
    
    # Percorre os arquivos da pasta de entrada
    for arquivo in os.listdir(pasta_entrada):
        if arquivo.lower().endswith((".jpeg", ".png")):
            caminho_entrada = os.path.join(pasta_entrada, arquivo)
            nome_arquivo = os.path.splitext(arquivo)[0] + ".jpg"
            caminho_saida = os.path.join(pasta_saida, nome_arquivo)
            
            # Abre e converte a imagem
            with Image.open(caminho_entrada) as img:
                rgb_img = img.convert("RGB")  # garante que não terá canal alfa
                rgb_img.save(caminho_saida, "JPEG")
            
            print(f"Convertido: {arquivo} -> {nome_arquivo}")

# Exemplo de uso:
converter_para_jpg("imagens_originais", "imagens_convertidas")
