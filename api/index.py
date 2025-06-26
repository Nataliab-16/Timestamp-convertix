from flask import Flask, render_template
from datetime import datetime
import sqlite3
send_from_directory = Flask.send_static_file
import os

app = Flask(__name__,  template_folder="templates")
DB_PATH = 'database.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS acessos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_hora TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    agora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO acessos (data_hora) VALUES (?)", (agora,))
    conn.commit()
    conn.close()
    return render_template('index.html', horario=agora)


@app.route('/registros')
def listar_registros():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM acessos ORDER BY id DESC")
    registros = cursor.fetchall()
    conn.close()
    return render_template('registros.html', registros=registros)


if __name__ == '__main__':
    init_db()
    app.run()
