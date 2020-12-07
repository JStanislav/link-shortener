import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '86f98987045e4cc1aa89060201f83783'
    