from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
import random

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def generate_realistic_price():
    # 現実的な価格を生成するロジック（仮の例）
    property_type = random.choice(['土地', '賃貸'])
    if property_type == '土地':
        price = f"{random.randint(1200, 1600)}万円"
    else:
        price = f"月額{random.randint(70000, 90000)}円（2LDK）"
    return property_type, price

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/estimate', methods=['POST'])
def estimate():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # ここで画像認識モデルを使用して価格を推定します（ダミーの推定価格）
        property_type, estimated_price = generate_realistic_price()
        age = 10  # 経年劣化年数を固定
        
        return render_template('result.html', price=estimated_price, image_url=filepath, age=age, property_type=property_type)
    return redirect(request.url)

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(host='0.0.0.0', port=5000, debug=True)
