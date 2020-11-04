import os
import datetime


class Config:
    '''
    General configuration class
    '''
    

class ProdConfig(Config):
    '''
    Production configuration class
    Args:
        Config: Parent configuration class with General configuration settings
    '''
    DEBUG = False


class DevConfig(Config):
    '''
    Development configuration class
    Args:
        Config: Parent configuration class with general configuration settings
    '''
    DEBUG = True


class TestConfig(Config):
    '''
    Test configuration child class
    Args:
        Config: Parent configuration class with general configuration settings
    '''
   

config_options = {
    'development': DevConfig,
    'production': ProdConfig,
    'TESTING': TestConfig,
}