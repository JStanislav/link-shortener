import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '86f98987045e4cc1aa89060201f83783'
    
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'shortener'

    SERVER_NAME = "127.0.0.1:5000"#change to domain in prod