import os
from flask import Flask
from werkzeug.security import generate_password_hash
from models import db, Clinic, Doctor, Admin, Patient, Appointment, AppointmentSlot, MedicalReport, Testimonial, FAQ
from flask_login import LoginManager

login_manager = LoginManager()


def seed_demo_data():
    """Create demo clinic, admin, doctors, FAQs and testimonials."""
    clinic = Clinic.query.filter_by(slug='default').first()
    if not clinic:
        clinic = Clinic(
            name='City ENT Clinic',
            slug='default',
            email='admin@entclinic.com',
            phone='+91-9876543210',
            address='123 Medical Street, Healthcare Plaza',
            city='New Delhi',
            state='Delhi',
            zip_code='110001',
            description='Leading ENT clinic with experienced specialists'
        )
        db.session.add(clinic)
        db.session.commit()

    admin = Admin.query.filter_by(email='admin@entclinic.com').first()
    if not admin:
        admin = Admin(
            clinic_id=clinic.id,
            username='admin',
            email='admin@entclinic.com',
            password_hash=generate_password_hash('admin123'),
            is_super_admin=True
        )
        db.session.add(admin)
        db.session.commit()

    if Doctor.query.filter_by(clinic_id=clinic.id).count() == 0:
        doctors = [
            {
                'name': 'Dr. Sourabh Kumar',
                'specialization': 'Otolaryngologist',
                'bio': 'Senior ENT specialist with 12 years of experience in sinus, allergy and voice care.',
                'experience_years': 12,
                'consultation_fee': 500,
                'email': 'sourabh@entclinic.com',
                'phone': '+91-9876500001'
            },
            {
                'name': 'Dr. Priya Singh',
                'specialization': 'Pediatric ENT',
                'bio': 'Specialized in treating ear, nose, and throat issues in children.',
                'experience_years': 10,
                'consultation_fee': 400,
                'email': 'priya@entclinic.com',
                'phone': '+91-9876543212'
            },
            {
                'name': 'Dr. Amit Patel',
                'specialization': 'Audiologist',
                'bio': 'Expert in hearing assessment and hearing aid fitting.',
                'experience_years': 12,
                'consultation_fee': 300,
                'email': 'amit@entclinic.com',
                'phone': '+91-9876543213'
            }
        ]
        for doc_data in doctors:
            doctor = Doctor(clinic_id=clinic.id, **doc_data)
            db.session.add(doctor)
        db.session.commit()

    if FAQ.query.filter_by(clinic_id=clinic.id).count() == 0:
        faqs = [
            {
                'category': 'Booking',
                'question': 'How do I book an appointment?',
                'answer': 'You can book an appointment through our online portal. Select the doctor, date, and preferred time slot.',
                'keywords': 'book, appointment, online',
                'is_active': True
            },
            {
                'category': 'Services',
                'question': 'What services do you provide?',
                'answer': 'We provide comprehensive ENT services including hearing tests, hearing aids, sinus treatment, and pediatric ENT care.',
                'keywords': 'services, treatment, consultation',
                'is_active': True
            },
            {
                'category': 'General',
                'question': 'What is the consultation fee?',
                'answer': 'Consultation fees vary by doctor, usually ranging from ₹300 to ₹500. You can see fee details when booking.',
                'keywords': 'fee, cost, price, payment',
                'is_active': True
            }
        ]
        for faq_data in faqs:
            faq = FAQ(clinic_id=clinic.id, **faq_data)
            db.session.add(faq)
        db.session.commit()

    if Testimonial.query.filter_by(clinic_id=clinic.id).count() == 0:
        testimonials = [
            {
                'patient_name': 'Rajesh Sharma',
                'rating': 5,
                'message': 'Excellent service! Dr. Sourabh Kumar diagnosed my sinus problem accurately and the treatment was very effective. The staff is very professional.',
                'is_approved': True
            },
            {
                'patient_name': 'Priya Patel',
                'rating': 5,
                'message': 'Very satisfied with the pediatric ENT care for my child. The doctor was amazing and made the entire experience comfortable.',
                'is_approved': True
            },
            {
                'patient_name': 'Amit Singh',
                'rating': 4,
                'message': 'Great hearing aid consultation. The clinic took time to understand my needs and recommended the right solution.',
                'is_approved': True
            }
        ]
        for testimonial_data in testimonials:
            testimonial = Testimonial(clinic_id=clinic.id, **testimonial_data)
            db.session.add(testimonial)
        db.session.commit()

def create_app(config_name='development'):
    """Application factory"""
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL', 
        'sqlite:///ent_clinic.db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JSON_SORT_KEYS'] = False
    
    # File upload config
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
    app.config['REPORT_FOLDER'] = os.path.join(os.path.dirname(__file__), 'reports')
    app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50 MB
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    # Create upload folders
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['REPORT_FOLDER'], exist_ok=True)
    
    # Register blueprints
    from routes.public import public_bp
    from routes.booking import booking_bp
    from routes.admin import admin_bp
    from routes.doctor import doctor_bp
    from routes.chatbot import chatbot_bp
    from routes.auth import auth_bp
    
    app.register_blueprint(public_bp)
    app.register_blueprint(booking_bp, url_prefix='/booking')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(doctor_bp, url_prefix='/doctor')
    app.register_blueprint(chatbot_bp, url_prefix='/chatbot')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    # Create database tables and seed demo content
    with app.app_context():
        db.create_all()
        seed_demo_data()

    # Context processor for clinic info
    @app.context_processor
    def inject_clinic():
        clinic_slug = get_current_clinic_slug()
        clinic = None
        if clinic_slug:
            clinic = Clinic.query.filter_by(slug=clinic_slug).first()
        return {'current_clinic': clinic}
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Not found'}, 404
    
    @app.errorhandler(500)
    def server_error(error):
        return {'error': 'Server error'}, 500
    
    return app

def get_current_clinic_slug():
    """Extract clinic slug from request (subdomain or query param)"""
    from flask import request, has_request_context
    if not has_request_context():
        return 'default'
    # For now, use query param. Later can be enhanced for subdomain
    return request.args.get('clinic', 'default')

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
