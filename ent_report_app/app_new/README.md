# ENT Clinic Booking System - Multi-Tenant Web Application

This is a comprehensive, production-ready ENT clinic booking and management system built with Flask and SQLAlchemy.

## 🎯 Features

### For Patients
- 🏥 Professional landing page with clinic information
- 👨‍⚕️ Browse doctor profiles with detailed information
- 📅 Real-time appointment slot availability
- ✍️ Easy online registration and booking
- 💬 AI-powered chatbot for FAQs
- 📱 PWA support for mobile app-like experience
- 🔔 Appointment confirmations

### For Admin
- 📊 Comprehensive dashboard with analytics
- 👨‍⚕️ Manage doctors and their profiles
- 📅 Configure appointment slots dynamically
- 📋 Generate medical reports from appointments
- ⭐ Manage patient testimonials
- 👥 Multi-tenant support (serve multiple clinics)
- 🔐 Secure admin authentication

### Technical Features
- ✨ Material Design 3 UI
- 📱 Fully responsive & mobile-optimized
- 🌐 Progressive Web App (PWA)
- 🔐 Multi-tenant architecture
- 🗄️ SQLAlchemy ORM with SQLite/PostgreSQL support
- 🔑 Secure password hashing
- 📡 RESTful API endpoints

## 📋 Project Structure

```
app_new/
├── models/
│   └── __init__.py              # Database models
├── routes/
│   ├── __init__.py
│   ├── auth.py                  # Authentication routes
│   ├── public.py                # Public pages
│   ├── booking.py               # Appointment booking
│   ├── admin.py                 # Admin dashboard
│   ├── doctor.py                # Doctor routes
│   └── chatbot.py               # Chatbot API
├── templates/
│   ├── base.html                # Base template
│   ├── public/                  # Public pages
│   │   ├── index.html
│   │   ├── doctors.html
│   │   ├── doctor_detail.html
│   │   ├── about.html
│   │   ├── services.html
│   │   └── contact.html
│   ├── booking/                 # Booking pages
│   │   ├── check_slots.html
│   │   ├── register.html
│   │   └── book_appointment.html
│   ├── admin/                   # Admin templates
│   │   ├── dashboard.html
│   │   ├── reports.html
│   │   ├── manage_slots.html
│   │   ├── doctors.html
│   │   └── testimonials.html
│   └── auth/                    # Auth templates
│       ├── login.html
│       └── register_clinic.html
├── static/
│   ├── css/
│   │   └── style.css            # Material Design styles
│   ├── js/
│   │   ├── script.js            # Main JS
│   │   ├── carousel.js          # Testimonials carousel
│   │   ├── chatbot.js           # Chatbot functionality
│   │   ├── booking.js           # Booking form logic
│   │   └── sw.js                # Service Worker (PWA)
│   ├── images/                  # Icons, images
│   └── manifest.json            # PWA manifest
└── app.py                       # App factory

```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip
- Virtual environment

### Installation

1. **Clone/Setup the project:**
   ```bash
   cd /Users/shashikumarpandey/git/devOps/ent_report_app/app_new
   ```

2. **Create and activate virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements_new.txt
   ```

4. **Initialize the database:**
   ```bash
   python3 -c "
   from app import create_app
   app = create_app()
   with app.app_context():
       from models import db
       db.create_all()
   "
   ```

5. **Run the development server:**
   ```bash
   python3 app.py
   ```
   
   The app will be available at `http://localhost:5000`

## 📊 Database Models

### Core Entities
- **Clinic**: Multi-tenant organization
- **Admin**: Admin users per clinic
- **Doctor**: Clinic staff with specialization
- **Patient**: Patient information
- **AppointmentSlot**: Available time slots
- **Appointment**: Booked appointments
- **MedicalReport**: Generated medical reports
- **Testimonial**: Patient feedback
- **FAQ**: Chatbot knowledge base

## 🔑 Key Routes

### Public Routes
- `/` - Landing page
- `/doctors` - All doctors listing
- `/doctor/<id>` - Doctor profile
- `/about` - About clinic
- `/services` - Services offered
- `/contact` - Contact page

### Booking Routes
- `/booking/appointment` - Check slots
- `/booking/register` - Patient registration
- `/booking/book/<patient_id>` - Book appointment
- `/booking/my-appointments/<phone>` - Patient's appointments

### Admin Routes (Protected)
- `/admin/dashboard` - Admin dashboard
- `/admin/reports` - Medical reports
- `/admin/slots` - Manage appointment slots
- `/admin/doctors` - Manage doctors
- `/admin/testimonials` - Manage testimonials

### Auth Routes
- `/auth/login` - Admin login
- `/auth/logout` - Logout
- `/auth/register` - Register new clinic

### Chatbot Routes
- `/chatbot/ask` - Chat API
- `/chatbot/faq-list` - FAQ listing

## 🎨 Customization

### Theming
Edit `static/css/style.css` to customize colors:
```css
:root {
    --primary-color: #1976d2;
    --secondary-color: #f57c00;
    /* ... */
}
```

### Adding New Clinic
1. Register via `/auth/register` endpoint
2. Admin can login and configure slots
3. Patients can book appointments

### Slot Configuration
Admin can create slots via:
- Dashboard → Manage Slots
- Or API: `POST /admin/api/slots/create`

## 📱 PWA Features

- ✅ Service Worker for offline support
- ✅ Web App Manifest
- ✅ Add to Home Screen
- ✅ Installable on mobile devices

## 🔒 Security Features

- ✅ Password hashing with werkzeug
- ✅ Flask-Login for sessions
- ✅ CSRF protection
- ✅ Input validation
- ✅ SQL injection prevention (SQLAlchemy ORM)

## 🚀 Production Deployment

### Using Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 "app:create_app()"
```

### Environment Variables:
```bash
export SECRET_KEY="your-secure-key"
export DATABASE_URL="postgresql://user:pass@localhost/ent_clinic"
export FLASK_ENV="production"
```

## 📈 Future Enhancements

- [ ] Payment gateway integration (Stripe/Razorpay)
- [ ] Email notifications
- [ ] SMS appointment reminders
- [ ] Video consultation
- [ ] Mobile app (React Native)
- [ ] Advanced analytics
- [ ] Insurance integration
- [ ] Prescription management

## 🤝 Contributing

This is a customizable template. Feel free to extend it with additional features.

## 📄 License

This project is provided as-is for clinical use.

## 📞 Support

For issues or questions, contact the development team.

---

**Version**: 1.0.0  
**Last Updated**: May 2024  
**Built with**: Flask, SQLAlchemy, Material Design 3
