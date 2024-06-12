import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://root:{os.getenv('MYSQL_ROOT_PASSWORD')}@localhost/sales_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
