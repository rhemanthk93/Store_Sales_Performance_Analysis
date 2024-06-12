import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost/sales_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
