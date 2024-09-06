from flask import Flask, render_template, send_file
from flask_socketio import SocketIO, emit
import matplotlib.pyplot as plt
import io
import random
import threading
import time

app = Flask(__name__)
socketio = SocketIO(app)

# Almacenar datos para graficar
data_x = []
data_y = []

# Función para actualizar datos y gráficos
def update_data():
    while True:
        data_x.append(len(data_x))
        data_y.append(random.randint(0, 10))
        if len(data_x) > 20:  # Mantener solo los últimos 20 puntos
            data_x.pop(0)
            data_y.pop(0)
        time.sleep(0.5)  # Esperar 0.5 segundos

        # Emitir la gráfica actualizada
        socketio.emit('update_graph', {'data': 'new graph'})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/plot.png')
def plot():
    plt.figure(figsize=(10, 6))
    plt.plot(data_x, data_y)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Real-time Graph')

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    return send_file(img, mimetype='image/png')

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('update_graph', {'data': 'initial graph'})

if __name__ == '__main__':
    # Iniciar el hilo para actualizar los datos
    thread = threading.Thread(target=update_data)
    thread.daemon = True
    thread.start()

    socketio.run(app, debug=True)
