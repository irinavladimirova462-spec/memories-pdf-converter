import io
import requests
from flask import Flask, request, send_file
from pdf2image import convert_from_bytes

app = Flask(__name__)

@app.route('/render_card.jpg')
def convert():
    # Получаем ссылку на PDF из параметров запроса
    pdf_url = request.args.get('url')
    if not pdf_url:
        return "Ошибка: Не указан URL", 400

    try:
        # Скачиваем PDF
        response = requests.get(pdf_url, timeout=10)
        # Конвертируем 1-ю страницу в картинку
        images = convert_from_bytes(response.content, dpi=200)
        
        # Сохраняем результат в память (буфер)
        img_io = io.BytesIO()
        images[0].save(img_io, 'JPEG', quality=85)
        img_io.seek(0)
        
        return send_file(img_io, mimetype='image/jpeg')
    except Exception as e:
        return f"Ошибка конвертации: {str(e)}", 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
