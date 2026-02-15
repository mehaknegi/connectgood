"""
Database Models for ConnectGood
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User authentication model"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'volunteer' or 'ngo'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    volunteer = db.relationship('Volunteer', backref='user', uselist=False, cascade='all, delete-orphan')
    ngo = db.relationship('NGO', backref='user', uselist=False, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.email}>'

class Volunteer(db.Model):
    """Volunteer profile model"""
    __tablename__ = 'volunteers'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Profile fields
    location = db.Column(db.String(100))
    skills = db.Column(db.Text)  # Comma-separated skills
    interests = db.Column(db.Text)
    availability = db.Column(db.String(50))
    hours_per_week = db.Column(db.Integer)
    
    # Stats
    total_hours = db.Column(db.Integer, default=0)
    credits = db.Column(db.Integer, default=0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    matches = db.relationship('Match', backref='volunteer', foreign_keys='Match.volunteer_id', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Volunteer {self.user.name}>'

class NGO(db.Model):
    """NGO profile model"""
    __tablename__ = 'ngos'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Profile fields
    organization_name = db.Column(db.String(200))
    location = db.Column(db.String(100))
    cause_area = db.Column(db.String(50))
    description = db.Column(db.Text)
    skills_required = db.Column(db.Text)  # Comma-separated skills
    commitment_type = db.Column(db.String(50))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    matches = db.relationship('Match', backref='ngo', foreign_keys='Match.ngo_id', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<NGO {self.organization_name}>'

class Match(db.Model):
    """Match between volunteer and NGO"""
    __tablename__ = 'matches'
    
    id = db.Column(db.Integer, primary_key=True)
    volunteer_id = db.Column(db.Integer, db.ForeignKey('volunteers.id'), nullable=False)
    ngo_id = db.Column(db.Integer, db.ForeignKey('ngos.id'), nullable=False)
    
    score = db.Column(db.Integer, nullable=False)  # Match percentage
    matched_skills = db.Column(db.Text)  # Comma-separated matched skills
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Match {self.volunteer_id} <-> {self.ngo_id} ({self.score}%)>'
