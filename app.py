from flask import Flask, render_template, Response, send_file
import mss
from io import BytesIO

app = Flask(__name__)

# Usamos um bloco try-except para o caso do MSS não funcionar imediatamente
try:
    sct = mss.mss()
except Exception as e:
    print(f"Erro ao inicializar o MSS: {e}")
    sct = None

@app.route('/')
def index():
    """Serve a página HTML principal."""
    return render_template('index.html')

@app.route('/stream.png')
def get_screenshot():
    """Tira um screenshot e o retorna como uma imagem PNG."""
    if sct is None:
        # Retorna um erro se o MSS não pôde ser inicializado
        return Response(status=500)
    try:
        # Define a região do monitor a ser capturada (monitor 1)
        monitor = sct.monitors[1]

        # Captura a imagem dessa região
        img_raw = sct.grab(monitor)

        # Converte a imagem capturada para o formato PNG
        img_bytes = mss.tools.to_png(img_raw.rgb, img_raw.size)

        # Usa BytesIO para tratar os bytes da imagem como um arquivo em memória
        buffer = BytesIO(img_bytes)
        buffer.seek(0)

        return send_file(buffer, mimetype='image/png')

    except Exception as e:
        print(f"Erro ao capturar o frame: {e}")
        return Response(status=500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
