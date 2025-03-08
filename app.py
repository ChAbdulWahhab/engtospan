from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests
import json
import time

app = Flask(__name__)

def translate_text(text, target_lang='es'):
    if not text or text.isspace():
        return text
    try:
        url = "https://translate.googleapis.com/translate_a/single"
        params = {
            "client": "gtx",
            "sl": "auto",
            "tl": target_lang,
            "dt": "t",
            "q": text
        }
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        result = response.json()
        translated_text = ''.join([sentence[0] for sentence in result[0]])
        return translated_text
    except Exception as e:
        print(f"Translation error: {e}")
        return text

@app.route('/', methods=['GET', 'POST'])
def index():
    translated_html = ""
    original_html = ""
    error_message = ""
    if request.method == 'POST':
        try:
            original_html = request.form.get('html_input', '')
            soup = BeautifulSoup(original_html, 'html.parser')
            for element in soup.find_all(text=True):
                if element.parent.name in ['script', 'style']:
                    continue
                if not element.strip():
                    continue
                translated_text = translate_text(element)
                element.replace_with(translated_text)
                time.sleep(0.1)
            translated_html = str(soup)
        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            print(error_message)
    return render_template('index.html', translated_html=translated_html, original_html=original_html, error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)
