import os
from pdf2image import convert_from_path
from PyPDF2 import PdfReader

# Caminho para o arquivo PDF
pdf_path = 'C:\\Trabalho\\PGR-MultiAgents\\pgr_analyst\\path\\pgr.pdf'

# Diretório onde as imagens serão salvas
output_dir = 'C:\\Trabalho\\PGR-MultiAgents\\pgr_analyst\\imgs\\pgr'

# Certifique-se de que o diretório de saída exista
os.makedirs(output_dir, exist_ok=True)

# Ler o PDF usando PyPDF2
with open(pdf_path, 'rb') as file:
    reader = PdfReader(file)
    number_of_pages = len(reader.pages)
    
    # Exibir o número de páginas
    print(f"O PDF contém {number_of_pages} páginas.")
    
    # Extrair texto de cada página
    for i in range(number_of_pages):
        page = reader.pages[i]
        text = page.extract_text()
        print(f"\n--- Página {i + 1} ---")
        print(text)

# Converter o PDF em imagens usando pdf2image
images = convert_from_path(pdf_path, poppler_path="C:\Trabalho\PGR-MultiAgents\pgr_analyst\imgs\poppler-22.04.0")

# Salvar cada imagem no diretório escolhido
for i, image in enumerate(images):
    image_path = os.path.join(output_dir, f'pagina_{i + 1}.png')  # Ajuste a extensão conforme desejar
    image.save(image_path, 'PNG')

print("Conversão de PDF para imagens concluída! As imagens foram salvas em:", output_dir)