"""
ConnectGood - Flask Application
Main application file with configuration and route registration
"""

from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime

from models import db, User, Volunteer, NGO, Match
from forms import SignupForm, LoginForm, VolunteerProfileForm, NGOProfileForm

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///connectgood.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create database tables
with app.app_context():
    db.create_all()
    print("✅ Database tables created!")

# ==================== ROUTES ====================

@app.route('/')
def landing():
    """Landing page - public"""
    return render_template('landing.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """User signup"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = SignupForm()
    if form.validate_on_submit():
        # Check if user exists
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already registered. Please login.', 'danger')
            return redirect(url_for('login'))
        
        # Create new user
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        new_user = User(
            name=form.name.data,
            email=form.email.data,
            password=hashed_password,
            role=form.role.data
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        # Create associated profile
        if form.role.data == 'volunteer':
            volunteer = Volunteer(user_id=new_user.id)
            db.session.add(volunteer)
        else:
            ngo = NGO(user_id=new_user.id)
            db.session.add(ngo)
        
        db.session.commit()
        
        flash('Account created successfully! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'Welcome back, {user.name}!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Login failed. Check your email and password.', 'danger')
    
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('landing'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard - redirects based on user role"""
    if current_user.role == 'volunteer':
        return redirect(url_for('volunteer_dashboard'))
    else:
        return redirect(url_for('ngo_dashboard'))

@app.route('/volunteer/dashboard')
@login_required
def volunteer_dashboard():
    """Volunteer dashboard"""
    if current_user.role != 'volunteer':
        flash('Access denied.', 'danger')
        return redirect(url_for('dashboard'))
    
    volunteer = Volunteer.query.filter_by(user_id=current_user.id).first()
    
    # Get matches for this volunteer
    matches = Match.query.filter_by(volunteer_id=volunteer.id).order_by(Match.score.desc()).all()
    
    # Calculate stats
    total_hours = volunteer.hours_per_week * 52 if volunteer.hours_per_week else 0
    credits = total_hours * 50
    people_helped = int(total_hours / 2) if total_hours else 0
    projects = int(total_hours / 20) if total_hours else 0
    
    # Get top volunteers for leaderboard
    top_volunteers = Volunteer.query.filter(Volunteer.hours_per_week.isnot(None)).order_by(Volunteer.hours_per_week.desc()).limit(5).all()
    
    return render_template('volunteer_dashboard.html', 
                         volunteer=volunteer,
                         matches=matches,
                         stats={
                             'total_hours': total_hours,
                             'credits': credits,
                             'people_helped': people_helped,
                             'projects': projects
                         },
                         top_volunteers=top_volunteers)

@app.route('/volunteer/profile', methods=['GET', 'POST'])
@login_required
def volunteer_profile():
    """Volunteer profile form"""
    if current_user.role != 'volunteer':
        flash('Access denied.', 'danger')
        return redirect(url_for('dashboard'))
    
    volunteer = Volunteer.query.filter_by(user_id=current_user.id).first()
    form = VolunteerProfileForm(obj=volunteer)
    
    if form.validate_on_submit():
        volunteer.location = form.location.data
        volunteer.skills = ','.join(form.skills.data) if form.skills.data else ''
        volunteer.interests = form.interests.data
        volunteer.availability = form.availability.data
        volunteer.hours_per_week = form.hours_per_week.data
        
        db.session.commit()
        
        # Generate matches
        generate_matches_for_volunteer(volunteer)
        
        flash('Profile updated successfully! Finding your matches...', 'success')
        return redirect(url_for('volunteer_dashboard'))
    
    return render_template('volunteer_profile.html', form=form, volunteer=volunteer)

@app.route('/ngo/dashboard')
@login_required
def ngo_dashboard():
    """NGO dashboard"""
    if current_user.role != 'ngo':
        flash('Access denied.', 'danger')
        return redirect(url_for('dashboard'))
    
    ngo = NGO.query.filter_by(user_id=current_user.id).first()
    
    # Get matches for this NGO
    matches = Match.query.filter_by(ngo_id=ngo.id).order_by(Match.score.desc()).all()
    
    # Skill gap analysis
    if ngo.skills_required:
        required_skills = ngo.skills_required.split(',')
        skill_gap = calculate_skill_gap(required_skills)
    else:
        skill_gap = []
    
    return render_template('ngo_dashboard.html', 
                         ngo=ngo,
                         matches=matches,
                         skill_gap=skill_gap)

@app.route('/ngo/profile', methods=['GET', 'POST'])
@login_required
def ngo_profile():
    """NGO profile form"""
    if current_user.role != 'ngo':
        flash('Access denied.', 'danger')
        return redirect(url_for('dashboard'))
    
    ngo = NGO.query.filter_by(user_id=current_user.id).first()
    form = NGOProfileForm(obj=ngo)
    
    if form.validate_on_submit():
        ngo.organization_name = form.organization_name.data
        ngo.location = form.location.data
        ngo.cause_area = form.cause_area.data
        ngo.description = form.description.data
        ngo.skills_required = ','.join(form.skills_required.data) if form.skills_required.data else ''
        ngo.commitment_type = form.commitment_type.data
        
        db.session.commit()
        
        # Generate matches
        generate_matches_for_ngo(ngo)
        
        flash('Profile updated successfully! Finding volunteers...', 'success')
        return redirect(url_for('ngo_dashboard'))
    
    return render_template('ngo_profile.html', form=form, ngo=ngo)

# ==================== MATCHING LOGIC ====================

def generate_matches_for_volunteer(volunteer):
    """Generate matches for a volunteer"""
    if not volunteer.skills:
        return
    
    volunteer_skills = set(volunteer.skills.split(','))
    ngos = NGO.query.filter(NGO.skills_required.isnot(None)).all()
    
    # Clear existing matches
    Match.query.filter_by(volunteer_id=volunteer.id).delete()
    
    for ngo in ngos:
        ngo_skills = set(ngo.skills_required.split(','))
        
        # Calculate match score
        matching_skills = volunteer_skills.intersection(ngo_skills)
        if matching_skills:
            score = len(matching_skills) / len(ngo_skills) * 100
            score = min(95, 60 + score)  # Scale between 60-95
            
            match = Match(
                volunteer_id=volunteer.id,
                ngo_id=ngo.id,
                score=int(score),
                matched_skills=','.join(matching_skills)
            )
            db.session.add(match)
    
    db.session.commit()

def generate_matches_for_ngo(ngo):
    """Generate matches for an NGO"""
    if not ngo.skills_required:
        return
    
    ngo_skills = set(ngo.skills_required.split(','))
    volunteers = Volunteer.query.filter(Volunteer.skills.isnot(None)).all()
    
    # Clear existing matches
    Match.query.filter_by(ngo_id=ngo.id).delete()
    
    for volunteer in volunteers:
        volunteer_skills = set(volunteer.skills.split(','))
        
        # Calculate match score
        matching_skills = volunteer_skills.intersection(ngo_skills)
        if matching_skills:
            score = len(matching_skills) / len(ngo_skills) * 100
            score = min(95, 60 + score)
            
            match = Match(
                volunteer_id=volunteer.id,
                ngo_id=ngo.id,
                score=int(score),
                matched_skills=','.join(matching_skills)
            )
            db.session.add(match)
    
    db.session.commit()

def calculate_skill_gap(required_skills):
    """Calculate skill gap for NGO"""
    skill_gap = []
    
    for skill in required_skills:
        skill = skill.strip()
        # Count volunteers with this skill
        count = Volunteer.query.filter(Volunteer.skills.like(f'%{skill}%')).count()
        
        # Calculate coverage percentage
        needed = 10  # Assume NGO needs 10 volunteers per skill
        coverage = min(100, (count / needed) * 100)
        
        status = 'good' if coverage >= 60 else 'low' if coverage >= 30 else 'critical'
        
        skill_gap.append({
            'skill': skill,
            'available': count,
            'coverage': int(coverage),
            'status': status
        })
    
    return skill_gap

# ==================== RUN APP ====================

if __name__ == '__main__':
    print("🚀 ConnectGood Flask Server Starting...")
    print("📝 Navigate to: http://localhost:5000")
    print("🔐 Create an account to get started!")
    app.run(debug=True, host='0.0.0.0', port=5001)
