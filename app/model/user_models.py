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
    gender = db.Column(db.String(50))

    education = db.Column(db.String(200))
    address = db.Column(db.String(120))
    city = db.Column(db.String(120))
    country = db.Column(db.String(120))
    role_on_start_up = db.Column(db.String(50))

    # Add other fields specific to StartupUser here


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

class PartnerUser(User):
    __tablename__ = 'partner_users'
    id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), primary_key=True)
    user = db.relationship('User', back_populates='partner_user')
    partner_company_id = db.Column(db.Integer, db.ForeignKey('partner_companies.id'))

    telephone = db.Column(db.String(120), index=True, unique=True)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(50))
    birthday = db.Column(db.DateTime)

    education = db.Column(db.String(200))
    address = db.Column(db.String(120))
    city = db.Column(db.String(120))
    country = db.Column(db.String(120))
    role = db.Column(db.String(50))


class PartnerCompany(db.Model):
    __tablename__ = 'partner_companies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, unique=True)
    logo_url = db.Column(db.String(500))
    description = db.Column(db.Text())
    web_site_url = db.Column(db.String(500))
    hq_country = db.Column(db.String(120))
    # Relationship
    partner_user = db.relationship('PartnerUser', backref='partner_company')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class PartnerCompanyTag(db.Model):
    __tablename__ = 'partner_company_tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, unique=True)

    # Relationship

    created_at = db.Column(db.DateTime, default=datetime.now)
    # Add other fields specific to StartupCompany here


class PartnerCompanyTagAssociation(db.Model):
    __tablename__ = 'partner_company_tag_associations'
    partner_company_id = db.Column(db.Integer, db.ForeignKey('partner_companies.id'), primary_key=True)
    partner_company_tag_id = db.Column(db.Integer, db.ForeignKey('partner_company_tags.id'), primary_key=True)

    # Relationship to the PartnerCompany and PartnerCompanyTag models
    partner_company = db.relationship('PartnerCompany', backref=db.backref("tag_associations"))
    partner_company_tag = db.relationship('PartnerCompanyTag', backref=db.backref("company_associations"))

    created_at = db.Column(db.DateTime, default=datetime.now)


class ProgramApplication(db.Model):
    __tablename__ = 'program_applications'
    id = db.Column(db.Integer, primary_key=True)
    startup_company_id = db.Column(db.Integer, db.ForeignKey('startup_companies.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)  # Stores the month and year of the report
    program_name = db.Column(db.String(120))
    status = db.Column(db.String(120))
    # Relationship back to the StartupCompany
    startup_company = db.relationship('StartupCompany', back_populates='program_applications')

