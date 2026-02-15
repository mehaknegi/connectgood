# ConnectGood - Flask Backend (Backup/Safety Net)

**Full-stack volunteer-NGO matching platform with authentication, database, and real-time features.**

## 🎯 Features

✅ **Complete Authentication System**
- User signup/login with role selection (Volunteer/NGO)
- Password hashing with Werkzeug
- Protected routes with Flask-Login
- Session management

✅ **Database-Backed**
- SQLite database (easy setup, no configuration)
- User, Volunteer, NGO, and Match models
- Automatic relationship management
- Real-time data storage

✅ **Beautiful Multi-Page UI**
- Professional landing page
- Clean auth pages
- Dashboard with left sidebar
- Responsive design

✅ **Smart Matching Algorithm**
- Skill-based matching
- Score calculation (60-95%)
- Real-time match generation
- Persistent matches in database

✅ **All Your Features**
- Impact preview (people helped, hours, projects)
- Credit system (50 credits/hour)
- Leaderboard with top volunteers
- Skill gap analyzer for NGOs
- Certificate generation ready

## 🚀 Quick Start

### Installation

```bash
# Navigate to project directory
cd connectgood-flask

# Install dependencies
pip install -r requirements.txt --break-system-packages

# Run the application
python3 app.py
```

### First Run

```bash
python3 app.py
```

The app will:
1. Create the SQLite database (`connectgood.db`)
2. Set up all tables automatically
3. Start the server on `http://localhost:5000`

### Access the App

1. Open browser: `http://localhost:5000`
2. Click "Get Started" or "Sign Up"
3. Create account (choose Volunteer or NGO)
4. Complete your profile
5. See matches instantly!

## 📁 Project Structure

```
connectgood-flask/
├── app.py                  # Main Flask application
├── models.py               # Database models
├── forms.py                # WTForms for validation
├── requirements.txt        # Python dependencies
├── templates/              # HTML templates
│   ├── base.html          # Base template
│   ├── landing.html       # Landing page
│   ├── login.html         # Login page
│   ├── signup.html        # Signup page
│   ├── volunteer_dashboard.html
│   ├── volunteer_profile.html
│   ├── ngo_dashboard.html
│   └── ngo_profile.html
├── static/
│   ├── css/
│   │   └── style.css      # Complete stylesheet
│   └── js/
│       └── main.js        # Interactive features
└── connectgood.db         # SQLite database (created on first run)
```

## 🎮 User Flows

### As a Volunteer:

1. **Sign Up** → Choose "Volunteer" role
2. **Complete Profile**:
   - Location
   - Skills (multiple selection)
   - Interests/causes
   - Availability
   - Hours per week
3. **View Dashboard**:
   - See impact stats (projected yearly impact)
   - Credits earned
   - Top matches with NGOs
   - Leaderboard position
4. **Connect** with NGOs

### As an NGO:

1. **Sign Up** → Choose "NGO" role
2. **Complete Profile**:
   - Organization name
   - Location
   - Cause area
   - Description of needs
   - Skills required
   - Commitment type
3. **View Dashboard**:
   - Skill gap analysis (which skills are in demand)
   - Matched volunteers
   - Volunteer credentials and stats
4. **Contact** volunteers

## 🗄️ Database Schema

### Users Table
- id, name, email, password (hashed), role, created_at

### Volunteers Table
- id, user_id, location, skills, interests, availability, hours_per_week, total_hours, credits

### NGOs Table
- id, user_id, organization_name, location, cause_area, description, skills_required, commitment_type

### Matches Table
- id, volunteer_id, ngo_id, score, matched_skills, created_at

## 🔧 Customization

### Add More Skills

Edit `forms.py`, line 10:
```python
SKILLS_CHOICES = [
    'Your New Skill',
    # ... existing skills
]
```

### Adjust Match Algorithm

Edit `app.py`, function `generate_matches_for_volunteer`:
```python
# Change scoring formula
score = len(matching_skills) / len(ngo_skills) * 100
score = min(95, 60 + score)  # Adjust these numbers
```

### Credits System

Edit `app.py`, line calculation:
```python
credits = total_hours * 50  # Change 50 to any multiplier
```

## 📊 Database Management

### View Database

```bash
# Install SQLite browser (optional)
# Or use command line:
sqlite3 connectgood.db

# View tables
.tables

# View users
SELECT * FROM users;

# View matches
SELECT * FROM matches;
```

### Reset Database

```bash
# Delete the database file
rm connectgood.db

# Run app again to recreate
python3 app.py
```

## 🎨 Design System

### Colors (CSS Variables)
- Primary: `#2D5F3F` (Green)
- Accent: `#F4A261` (Orange)
- Success: `#27AE60`
- Warning: `#F39C12`
- Danger: `#E74C3C`

### Fonts
- Headings: Clash Display
- Body: Clash Display
- Mono: Spline Sans Mono

## 🚨 Troubleshooting

### Port Already in Use
```bash
# Change port in app.py, last line:
app.run(debug=True, host='0.0.0.0', port=5001)  # Changed to 5001
```

### Database Errors
```bash
# Delete and recreate
rm connectgood.db
python3 app.py
```

### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --break-system-packages --force-reinstall
```

## 📝 Testing Checklist

- [ ] Landing page loads
- [ ] Can sign up as volunteer
- [ ] Can sign up as NGO
- [ ] Login works
- [ ] Volunteer can complete profile
- [ ] NGO can complete profile
- [ ] Matches are generated
- [ ] Dashboard shows stats
- [ ] Leaderboard displays
- [ ] Skill gap shows for NGOs
- [ ] Logout works
- [ ] Mobile responsive

## 🎯 Next Steps

### If Staying with Flask:
1. Add certificate download functionality
2. Implement messaging between volunteers and NGOs
3. Add email notifications
4. Create admin panel
5. Deploy to Render or PythonAnywhere

### If Switching to MERN:
1. Use this as reference for features
2. Replicate the database schema in MongoDB
3. Convert templates to React components
4. Keep the same design system

## 🔐 Security Notes

**For Production:**
1. Change `SECRET_KEY` in `app.py`
2. Use environment variables for sensitive data
3. Enable HTTPS
4. Add CSRF protection (already included via Flask-WTF)
5. Implement rate limiting
6. Use PostgreSQL instead of SQLite

## 💡 Tips

- **Development**: Keep `debug=True` in app.py
- **Testing**: Create 2-3 fake NGOs and volunteers to test matching
- **Demo**: Pre-populate database with sample data before hackathon
- **Deployment**: Use Render (free tier) or PythonAnywhere

## 📚 Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)
- [Flask-Login](https://flask-login.readthedocs.io/)
- [WTForms](https://wtforms.readthedocs.io/)

## 🏆 Hackathon Demo Script

```
1. Show landing page (30 sec)
2. Sign up as volunteer (30 sec)
3. Complete profile (45 sec)
4. Show impact dashboard (30 sec)
5. Show matches (30 sec)
6. Switch to NGO view (15 sec)
7. Show skill gap analyzer (30 sec)

Total: 3 minutes 30 seconds
```

---

**This is your safety net!** You have a fully working app ready to go. Now go learn React with confidence! 🚀
