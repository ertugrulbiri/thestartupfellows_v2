from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

import base64
import os
import time as t
from datetime import datetime, timedelta
from hashlib import md5
from time import time

import jwt
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from config.config import Config as c
from app import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    # This field determines the type of user: Client, StartupUser, Investor, etc.
    type = db.Column(db.String(50))


    # Relationships
    # Define relationships to different user types
    startup_user = db.relationship('StartupUser', back_populates='user', uselist=False)
    partner_user = db.relationship('PartnerUser', back_populates='user', uselist=False)
    admin_user = db.relationship('AdminUser', back_populates='user', uselist=False)


    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'type': self.type
        }


    # Add other relationships here as needed

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')

    def get_start_up(self):
        # returns the Client object if it exists
        return self.startup_user
    def get_partner(self):
        # returns the Client object if it exists
        return self.partner_user
    def get_admin(self):
        # returns the Client object if it exists
        return self.admin_user



class StartupUser(User):
    __tablename__ = 'startup_users'
    id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), primary_key=True)
    user = db.relationship('User', back_populates='startup_user')
    startup_company_id = db.Column(db.Integer, db.ForeignKey('startup_companies.id', ondelete="CASCADE"))

    name = db.Column(db.String(240))
    surname = db.Column(db.String(240))
    telephone = db.Column(db.String(120), index=True, unique=True)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(50))
    birthday = db.Column(db.DateTime)

    university_name = db.Column(db.String(400))
    major = db.Column(db.String(400))
    student_level = db.Column(db.String(400))
    uni_start_date = db.Column(db.DateTime)
    uni_end_date = db.Column(db.DateTime)

    reason_to_fs = db.Column(db.String(400))
    motivation_letter = db.Column(db.Text())

    address = db.Column(db.String(480))
    city = db.Column(db.String(480))
    country = db.Column(db.String(120))
    role = db.Column(db.String(50))
    linkedin_url = db.Column(db.String(300))

    reference = db.Column(db.String(300))

    # Consent
    is_consent_given = db.Column(db.Boolean, default=False)
    are_terms_accepted = db.Column(db.Boolean, default=False)
    is_agreed_to_rules = db.Column(db.Boolean, default=False)

    # Add other fields specific to StartupUser here

    # Language
    english_test = db.Column(db.String(480))
    english_proficiency_lvl = db.Column(db.String(300))

    def to_dict(self):
        data = {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'surname': self.surname,
            'telephone': self.telephone,
            'university_name': self.university_name,
            'uni_start_date': self.uni_start_date,
            'uni_end_date': self.uni_end_date,
            'student_level': self.student_level,
            'major': self.major,
            'gender': self.gender,
            'age': self.age,
            'birthday': self.birthday,
            'city': self.city,
            'motivation_letter': self.motivation_letter,
            'reason_to_fs': self.reason_to_fs,
            'linkedin_url': self.linkedin_url,
            'reference': self.reference,
            'country': self.country,
            'english_test': self.english_test,
            'english_proficiency_lvl': self.english_proficiency_lvl,
            'role': self.role,
            "is_consent_given": self.is_consent_given,
            'are_terms_accepted': self.are_terms_accepted,
            'is_agreed_to_rules': self.is_agreed_to_rules,
            'startUpCompanyId': self.startup_company_id}
        return data

    def from_dict(self, data):

        for field in ['email', 'name', 'surname', 'telephone', 'university_name', 'reason_to_fs',
                      'gender', 'age', 'birthday', 'city', 'country', 'role', 'startUpCompanyId',
                      'student_level', 'major', 'linkedin_url', 'address', 'english_test', 'english_proficiency_lvl',
                      'are_terms_accepted',
                      'is_agreed_to_rules', 'uni_start_date', 'uni_end_date', 'motivation_letter', 'reference']:
            if field in data:
                if field in ['uni_start_date', 'uni_end_date', 'birthday']:
                    setattr(self, field, datetime.strptime(data[field], "%d-%m-%Y") if data[field] else None)
                else:
                    setattr(self, field, data[field])

    # Add other fields specific to StartupUser here


class AdminUser(User):
    __tablename__ = 'admin_users'
    id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), primary_key=True)
    user = db.relationship('User', back_populates='admin_user')
    telephone = db.Column(db.String(120), index=True, unique=True)
    job = db.Column(db.String(120))
    img_url = db.Column(db.String(340))

    def to_dict(self):
        data = {
            "id": self.id,
            'telephone': self.telephone,
            'job': self.job,
            'img_url': self.img_url
        }
        return data

    def from_dict(self, data):
        for field in ['telephone', 'job', 'img_url']:
            if field in data:
                setattr(self, field, data[field])


    # Add other fields specific to StartupUser here

class PartnerUser(User):
    __tablename__ = 'partner_users'
    id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), primary_key=True)
    user = db.relationship('User', back_populates='partner_user')
    name = db.Column(db.String(150), nullable=False)
    surname = db.Column(db.String(150), nullable=False)
    profession = db.Column(db.String(500))
    company_name = db.Column(db.String(250))

    type = db.Column(db.String(100))

    def to_dict(self):
        data = {
            "id": self.id,
            'surname': self.surname,
            'name': self.name,
            'profession': self.profession,
            'company_name': self.company_name,
            "type":self.type
        }
        return data

    def from_dict(self, data):
        for field in ['surname', 'name', 'profession', 'company_name', 'type']:
            if field in data:
                setattr(self, field, data[field])


class StartupCompany(db.Model):
    __tablename__ = 'startup_companies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(240))
    logo_url = db.Column(db.String(500))
    industry = db.Column(db.String(120))
    description = db.Column(db.Text())
    web_site_url = db.Column(db.String(500))
    hq_country = db.Column(db.String(120))
    founding_date = db.Column(db.DateTime)
    founding_stage = db.Column(db.String(400))
    start_up_status = db.Column(db.String(400))
    total_founding = db.Column(db.Integer)
    current_employee_count = db.Column(db.Integer)
    business_model = db.Column(db.String(240))  # B2C, B2B, B2G
    old_accelerator_programs = db.Column(db.String(240))
    fs_incubation_participant = db.Column(db.Boolean, default=False)
    fs_accelerator_participant = db.Column(db.String(240))
    equity_free_investments_by_fs = db.Column(db.Integer, default=0)
    pitch_deck_url = db.Column(db.String(500))

    monthly_reports = db.relationship('MonthlyReport', back_populates='startup_company', cascade="all, delete-orphan")
    program_applications = db.relationship('ProgramApplication', back_populates='startup_company', cascade="all, delete-orphan")
    # Relationship
    startup_users = db.relationship('StartupUser', backref='startup_company')
    created_at = db.Column(db.DateTime, default=datetime.now)
    # Add other fields specific to StartupCompany here
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'logo_url': self.logo_url,
            'industry': self.industry,
            'description': self.description,
            'web_site_url': self.web_site_url,
            'hq_country': self.hq_country,
            'founding_date': self.founding_date.strftime('%Y-%m-%d %H:%M:%S') if self.founding_date else None,
            'founding_stage': self.founding_stage,
            'start_up_status': self.start_up_status,
            'total_founding': self.total_founding,
            'current_employee_count': self.current_employee_count,
            'business_model': self.business_model,
            'old_accelerator_programs': self.old_accelerator_programs,
            'fs_incubation_participant': self.fs_incubation_participant,
            'fs_accelerator_participant': self.fs_accelerator_participant,
            'equity_free_investments_by_fs': self.equity_free_investments_by_fs,
            'pitch_deck_url': self.pitch_deck_url,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            'startup_users': [startup_user.to_dict() for startup_user in self.startup_users],
            'start_up_reports': [monthly_reports.to_dict() for monthly_reports in self.monthly_reports]
        }

    def from_dict(self, data):
        for field in ['name', 'logo_url', 'industry', 'description', 'web_site_url',
                      'hq_country', 'founding_date', 'founding_stage', 'start_up_status',
                      'total_founding', 'current_employee_count', 'business_model',
                      'old_accelerator_programs', 'fs_incubation_participant',
                      'fs_accelerator_participant', 'equity_free_investments_by_fs',
                      'pitch_deck_url', 'created_at', 'updated_at']:

            if field in data:
                # For the dates, we convert from string format back to datetime object
                if field in ['founding_date']:
                    setattr(self, field, datetime.strptime(data[field], "%d-%m-%Y") if data[field] else None)
                else:
                    setattr(self, field, data[field])

        if 'startup_users' in data:
            self.startup_users = [StartupUser().from_dict(user_dict) for user_dict in data['startup_users']]


class MonthlyReport(db.Model):
    __tablename__ = 'monthly_reports'
    id = db.Column(db.Integer, primary_key=True)
    startup_company_id = db.Column(db.Integer, db.ForeignKey('startup_companies.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)  # Stores the month and year of the report

    # Relationship back to the StartupCompany
    startup_company = db.relationship('StartupCompany', back_populates='monthly_reports')

    # Relationship to KPIs
    # I want to delete all kpis when delete report

    kpis = db.relationship('KPI', back_populates='monthly_report', cascade="all, delete")

    def to_dict(self):
        data = {
            'created_at': self.created_at,
            'startup_company_id': self.startup_company_id,
            'kpis': [kpi.to_dict() for kpi in self.kpis]
        }
        return data


class KPI(db.Model):
    __tablename__ = 'kpis'
    id = db.Column(db.Integer, primary_key=True)
    monthly_report_id = db.Column(db.Integer, db.ForeignKey('monthly_reports.id', ondelete='CASCADE'))
    name = db.Column(db.String(120))  # The name of the KPI, e.g., "Revenue Growth"
    kpi_value = db.Column(
        db.Integer)  # The value of the KPI, could be a numeric value stored as a string for flexibility
    north_star_metric = db.Column(db.Boolean, default=False)  # Indicates if this KPI is the North Star Metric

    created_at = db.Column(db.DateTime, default=datetime.now)
    # Relationship back to the MonthlyReport
    monthly_report = db.relationship('MonthlyReport', back_populates='kpis', cascade="all")

    def to_dict(self):
        data = {
            'id':self.id,
            'monthly_report_id': self.monthly_report_id,
            'name': self.name,
            'kpi_value': self.kpi_value,
            'north_star_metric': self.north_star_metric,
            "created_at": self.created_at
        }
        return data
    def from_dict(self, data):
        for field in ['monthly_report_id', 'name', 'kpi_value', 'north_star_metric']:
            if field in data:
                setattr(self, field, data[field])


meeting_users = db.Table('meeting_users',
    db.Column('meeting_id', db.Integer, db.ForeignKey('meetings.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)

note_authors = db.Table('note_authors',
    db.Column('note_id', db.Integer, db.ForeignKey('meeting_notes.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)

class Meeting(db.Model):
    __tablename__ = 'meetings'
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(255), default="MEETING URL")
    purpose = db.Column(db.Text)

    # Relationships
    attendees = db.relationship('User', secondary=meeting_users, backref=db.backref('meetings', lazy='dynamic'))
    notes = db.relationship('MeetingNote', backref='meeting', lazy=True)

    def __init__(self, **kwargs):
        super(Meeting, self).__init__(**kwargs)
        self.end_date = self.start_date + timedelta(minutes=45)

class MeetingNote(db.Model):
    __tablename__ = 'meeting_notes'
    id = db.Column(db.Integer, primary_key=True)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meetings.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    # Relationship
    authors = db.relationship('User', secondary=note_authors, backref=db.backref('authored_notes', lazy='dynamic'))



class ProgramApplication(db.Model):
    __tablename__ = 'program_applications'
    id = db.Column(db.Integer, primary_key=True)
    startup_company_id = db.Column(db.Integer, db.ForeignKey('startup_companies.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)  # Stores the month and year of the report
    program_name = db.Column(db.String(120))
    status = db.Column(db.String(120))
    # Relationship back to the StartupCompany
    startup_company = db.relationship('StartupCompany', back_populates='program_applications')


class Slot(db.Model):
    __tablename__ = 'slots'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    is_booked = db.Column(db.Boolean, default=False, nullable=False)

    # Relationship back to User
    user = db.relationship('User', backref='slots')

    def __init__(self, **kwargs):
        super(Slot, self).__init__(**kwargs)
        # Automatically set the end_time to 45 minutes after the start_time
        if 'start_time' in kwargs:
            self.end_time = self.start_time + timedelta(minutes=45)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'start_time': self.start_time.strftime('%Y-%m-%d %H:%M:%S'),
            'end_time': self.end_time.strftime('%Y-%m-%d %H:%M:%S'),
            'is_booked': self.is_booked
        }