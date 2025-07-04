# creating a class called config
class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@localhost/gko_db"
    JWT_SECRET_KEY = "author"