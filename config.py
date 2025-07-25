# config.py

import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_super_secret_key'
    SQLALCHEMY_DATABASE_URI = "postgresql://neondb_owner:npg_TfNsHjeA1D5l@ep-wild-boat-abmgk7yk-pooler.eu-west-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
