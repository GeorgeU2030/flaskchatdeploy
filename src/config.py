class Config():
    SECRET_KEY = 'DSFDGDGDGGF'

class DevelopmentConfig(Config):
    DEBUG = True

config = {
    'development':DevelopmentConfig
}
    