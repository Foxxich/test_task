import openai
import os
from dotenv import load_dotenv

# Wczytywanie zmiennych środowiskowych
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("Brak klucza API. Dodaj go do pliku .env.")

# Funkcja odczytująca treść artykułu
def read_article(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Funkcja generująca HTML za pomocą OpenAI
def generate_html(article_content):
    prompt = (
        "Przekształć poniższy tekst w kod HTML z odpowiednią strukturą. "
        "Użyj tagów <h1>, <h2>, <p>, <img> zgodnie z treścią. "
        "Dodaj tagi <img> z src='image_placeholder.jpg' i odpowiednim alt "
        "oraz podpisami pod obrazkami.\n\n" + article_content
    )
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Jesteś asystentem pomagającym w generowaniu kodu HTML."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    
    return response['choices'][0]['message']['content'].strip()

# Funkcja zapisująca HTML do pliku
def save_html(file_path, html_content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(html_content)

# Funkcja tworząca szablon HTML
def create_template(file_path):
    template = """
<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Szablon Artykułu</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; margin: 20px; }
        img { max-width: 100%; height: auto; display: block; margin: 10px 0; }
        figcaption { font-style: italic; text-align: center; }
    </style>
</head>
<body>
    <!-- Wklej kod artykułu tutaj -->
</body>
</html>
"""
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(template)

# Funkcja tworząca pełny podgląd HTML
def create_preview(template_path, article_path, output_path):
    with open(template_path, 'r', encoding='utf-8') as template_file:
        template = template_file.read()
    with open(article_path, 'r', encoding='utf-8') as article_file:
        article = article_file.read()
    full_html = template.replace("<!-- Wklej kod artykułu tutaj -->", article)
    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write(full_html)

def main():
    openai.api_key = OPENAI_API_KEY
    
    # Odczyt artykułu
    article_path = "Zadanie dla JJunior AI Developera - tresc artykulu.txt"
    article_content = read_article(article_path)
    
    # Generowanie HTML
    print("Generowanie kodu HTML...")
    html_content = generate_html(article_content)
    
    # Zapis wygenerowanego HTML
    output_path = "artykul.html"
    save_html(output_path, html_content)
    print(f"Zapisano wygenerowany kod HTML w pliku: {output_path}")
    
    # Tworzenie szablonu HTML
    template_path = "szablon.html"
    create_template(template_path)
    print(f"Szablon HTML zapisany w pliku: {template_path}")
    
    # Tworzenie podglądu HTML
    preview_path = "podglad.html"
    create_preview(template_path, output_path, preview_path)
    print(f"Podgląd artykułu zapisany w pliku: {preview_path}")

if __name__ == "__main__":
    main()
