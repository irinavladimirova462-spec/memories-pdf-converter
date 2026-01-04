import io
import requests
from flask import Flask, request, send_file
from pdf2image import convert_from_bytes
import os

app = Flask(__name__)

@app.route('/render_card.jpg')
def convert():
    pdf_url = request.args.get('url')
    if not pdf_url:
        return "URL is missing", 400

    try:
        response = requests.get(pdf_url, timeout=15)
        response.raise_for_status()
        
        # Конвертируем PDF
        images = convert_from_bytes(response.content, dpi=200)
        
        if not images:
            return "Could not convert PDF", 500

        img_io = io.BytesIO()
        images[0].save(img_io, 'JPEG', quality=85)
        img_io.seek(0)
        
        return send_file(img_io, mimetype='image/jpeg')
    except Exception as e:
        return str(e), 500

if __name__ == "__main__":
    # Render использует переменную окружения PORT
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
