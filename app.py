from flask import Flask, request, render_template, send_from_directory, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import tensorflow as tf
import numpy as np
from PIL import Image
import os
import uuid
import random
from flask_mail import Mail, Message

app = Flask(__name__)

# App configuration
app.config['SECRET_KEY'] = 'your-secret-key-here'  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'abienterpriseabi@gmail.com'
app.config['MAIL_PASSWORD'] = 'zyrx hreq lecs lkuj' 

# Initialize extensions
db = SQLAlchemy(app)
mail = Mail(app)

# Load the trained model
MODEL_PATH = 'herbal_leaf_classifier.h5'
model = tf.keras.models.load_model(MODEL_PATH)

# Define class names
CLASS_NAMES = [
    'Alpinia Galanga (Rasna)', 'Amaranthus Viridis (Arive-Dantu)', 'Artocarpus Heterophyllus (Jackfruit)',
    'Azadirachta Indica (Neem)', 'Basella Alba (Basale)', 'Brassica Juncea (Indian Mustard)',
    'Carissa Carandas (Karanda)', 'Citrus Limon (Lemon)', 'Ficus Auriculata (Roxburgh fig)',
    'Ficus Religiosa (Peepal Tree)', 'Hibiscus Rosa-sinensis', 'Jasminum (Jasmine)',
    'Mangifera Indica (Mango)', 'Mentha (Mint)', 'Moringa Oleifera (Drumstick)',
    'Muntingia Calabura (Jamaica Cherry-Gasagase)', 'Murraya Koenigii (Curry)', 'Nerium Oleander (Oleander)',
    'Nyctanthes Arbor-tristis (Parijata)', 'Ocimum Tenuiflorum (Tulsi)', 'Piper Betle (Betel)',
    'Plectranthus Amboinicus (Mexican Mint)', 'Pongamia Pinnata (Indian Beech)', 'Psidium Guajava (Guava)',
    'Punica Granatum (Pomegranate)', 'Santalum Album (Sandalwood)', 'Syzygium Cumini (Jamun)',
    'Syzygium Jambos (Rose Apple)', 'Tabernaemontana Divaricata (Crape Jasmine)',
    'Trigonella Foenum-graecum (Fenugreek)'
]

# Define detailed benefits
HERB_BENEFITS = {
    'Alpinia Galanga (Rasna)': 'Alpinia Galanga, commonly known as Rasna, is a medicinal herb used in Ayurveda. It is known for its anti-inflammatory properties, helping to relieve arthritis and joint pain. It also aids digestion and is used to treat respiratory issues like cough and cold.',
    'Amaranthus Viridis (Arive-Dantu)': 'Amaranthus Viridis, or Arive-Dantu, is a nutrient-rich leafy vegetable. Packed with vitamins A and C, it boosts immunity and promotes healthy skin. It’s also a great source of iron, helping to prevent anemia.',
    'Artocarpus Heterophyllus (Jackfruit)': 'Jackfruit is a tropical fruit with high fiber content, supporting digestive health. It’s rich in antioxidants, which promote heart health, and its potassium content helps regulate blood pressure.',
    'Azadirachta Indica (Neem)': 'Neem is a powerhouse of medicinal properties. Its antibacterial and antifungal qualities make it excellent for skin health, treating acne and infections. It also supports oral hygiene and boosts immunity.',
    'Basella Alba (Basale)': 'Basella Alba, or Basale, is a leafy green rich in iron and calcium. It helps prevent anemia, strengthens bones, and its vitamin A content supports eye health.',
    'Brassica Juncea (Indian Mustard)': 'Indian Mustard leaves are anti-inflammatory and rich in antioxidants. They aid respiratory health by clearing congestion and are a good source of vitamins K, A, and C.',
    'Carissa Carandas (Karanda)': 'Karanda is a berry-like fruit loaded with antioxidants. It boosts immunity, aids digestion, and its vitamin C content helps fight infections.',
    'Citrus Limon (Lemon)': 'Lemon is a citrus fruit known for its detoxifying effects. High in vitamin C, it boosts immunity, aids digestion, and promotes healthy skin by reducing blemishes.',
    'Ficus Auriculata (Roxburgh fig)': 'Roxburgh fig supports digestion due to its fiber content. It’s rich in vitamins and minerals, contributing to overall nutritional health.',
    'Ficus Religiosa (Peepal Tree)': 'Peepal Tree leaves are used in traditional medicine to improve respiratory health, treating asthma and cough. It holds spiritual significance in many cultures.',
    'Hibiscus Rosa-sinensis': 'Hibiscus is renowned for promoting hair growth and preventing hair fall. It also lowers blood pressure and has antioxidant properties that benefit overall health.',
    'Jasminum (Jasmine)': 'Jasmine is known for its calming fragrance, reducing stress and anxiety. It’s also used in teas to aid digestion and promote relaxation.',
    'Mangifera Indica (Mango)': 'Mango leaves are rich in vitamins A, B, and C. They boost immunity, support eye health, and have anti-inflammatory properties.',
    'Mentha (Mint)': 'Mint is a refreshing herb that aids digestion, relieves bloating, and freshens breath. It’s also used to alleviate headaches and colds.',
    'Moringa Oleifera (Drumstick)': 'Moringa is a superfood packed with nutrients. It’s anti-inflammatory, supports brain health, and its high vitamin content boosts immunity.',
    'Muntingia Calabura (Jamaica Cherry-Gasagase)': 'Jamaica Cherry is an antioxidant-rich fruit that reduces inflammation and supports heart health. It’s also used to relieve headaches.',
    'Murraya Koenigii (Curry)': 'Curry leaves improve digestion, reduce cholesterol, and promote hair health by preventing premature graying and hair loss.',
    'Nerium Oleander (Oleander)': 'Oleander is primarily ornamental but toxic if ingested. It has historical use in herbal medicine (with caution) for skin conditions.',
    'Nyctanthes Arbor-tristis (Parijata)': 'Parijata leaves relieve cough and fever. Its flowers are aromatic and used in traditional remedies for relaxation.',
    'Ocimum Tenuiflorum (Tulsi)': 'Tulsi, or Holy Basil, boosts immunity, reduces stress, and supports respiratory health. It’s a staple in Ayurvedic medicine.',
    'Piper Betle (Betel)': 'Betel leaves improve digestion and oral health. They’re often chewed to freshen breath and have antiseptic properties.',
    'Plectranthus Amboinicus (Mexican Mint)': 'Mexican Mint relieves colds and congestion. Its anti-inflammatory properties also help with skin irritations.',
    'Pongamia Pinnata (Indian Beech)': 'Indian Beech has antiseptic qualities, used in skin care for treating infections. It’s also beneficial for joint pain relief.',
    'Psidium Guajava (Guava)': 'Guava leaves are rich in vitamin C, aiding digestion and boosting immunity. They’re also used to manage diabetes.',
    'Punica Granatum (Pomegranate)': 'Pomegranate is an antioxidant powerhouse, supporting heart health and reducing inflammation. It also improves digestion.',
    'Santalum Album (Sandalwood)': 'Sandalwood calms the skin, reducing acne and irritation. Its aroma promotes relaxation and mental clarity.',
    'Syzygium Cumini (Jamun)': 'Jamun controls blood sugar levels and aids digestion. It’s rich in antioxidants, benefiting skin and heart health.',
    'Syzygium Jambos (Rose Apple)': 'Rose Apple is hydrating and rich in fiber, supporting digestion. It also has mild antimicrobial properties.',
    'Tabernaemontana Divaricata (Crape Jasmine)': 'Crape Jasmine relieves pain and inflammation. It’s also used ornamentally for its fragrant flowers.',
    'Trigonella Foenum-graecum (Fenugreek)': 'Fenugreek lowers cholesterol, aids digestion, and supports lactation in nursing mothers. It’s also good for hair health.'
}

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

# Admin hardcoded credentials
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin'

# Ensure upload folders exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
if not os.path.exists('static/uploads'):
    os.makedirs('static/uploads')

# Helper functions
def generate_otp():
    return str(random.randint(1000, 9999))

def preprocess_image(image):
    img = image.resize((224, 224))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

# Routes
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password) and not user.is_admin:
            session['user_id'] = user.id
            session['is_admin'] = user.is_admin
            return redirect(url_for('dashboard'))
        elif username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['user_id'] = None
            session['is_admin'] = True
            return redirect(url_for('admin_dashboard'))
        flash('Invalid credentials', 'error')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return redirect(url_for('signup'))
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return redirect(url_for('signup'))
        
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_password, email=email)
        db.session.add(new_user)
        db.session.commit()
        
        # Generate and send OTP
        otp = generate_otp()
        session['otp'] = otp
        session['new_user_id'] = new_user.id
        
        msg = Message('Your OTP for Signup Verification', sender=app.config['MAIL_USERNAME'], recipients=[email])
        msg.body = f'Your OTP for Medical Herbs Detection signup verification is: {otp}'
        mail.send(msg)
        
        flash('An OTP has been sent to your email. Please verify.', 'info')
        return redirect(url_for('otp_verify'))
    return render_template('signup.html')

@app.route('/otp_verify', methods=['GET', 'POST'])
def otp_verify():
    if request.method == 'POST':
        entered_otp = request.form['otp']
        if 'otp' in session and entered_otp == session['otp']:
            user = User.query.get(session['new_user_id'])
            session['user_id'] = user.id
            session.pop('new_user_id', None)
            session.pop('otp', None)
            flash('Signup verified successfully. You can now login.', 'success')
            return redirect(url_for('login'))
        flash('Invalid OTP. Please try again.', 'error')
    return render_template('otp_verify.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if not session.get('user_id') or session.get('is_admin'):
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('dashboard.html', error='No file uploaded')
        
        file = request.files['file']
        if file.filename == '':
            return render_template('dashboard.html', error='No file selected')
        
        try:
            image = Image.open(file).convert('RGB')
            processed_image = preprocess_image(image)
            
            filename = f"{uuid.uuid4()}.jpg"
            image.save(os.path.join('static/uploads', filename))
            
            predictions = model.predict(processed_image)
            predicted_class_idx = np.argmax(predictions[0])
            predicted_class = CLASS_NAMES[predicted_class_idx]
            confidence = predictions[0][predicted_class_idx] * 100
            benefits = HERB_BENEFITS.get(predicted_class, 'Detailed benefits not available')
            
            return render_template('result.html', 
                                 herb_name=predicted_class, 
                                 confidence=f'{confidence:.2f}', 
                                 benefits=benefits,
                                 image_url=f'/uploads/{filename}')
        except Exception as e:
            return render_template('dashboard.html', error=f'Error processing image: {str(e)}')
    
    return render_template('dashboard.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('static/uploads', filename)

@app.route('/admin')
def admin_dashboard():
    if not session.get('is_admin'):
        return redirect(url_for('login'))
    
    users = User.query.all()
    return render_template('admin.html', users=users)

@app.route('/delete_user/<int:user_id>')
def delete_user(user_id):
    if not session.get('is_admin'):
        return redirect(url_for('login'))
    
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('is_admin', None)
    session.pop('otp', None)
    session.pop('new_user_id', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
