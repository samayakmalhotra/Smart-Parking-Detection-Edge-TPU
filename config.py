import os
import datetime
import json
import os


class Config:
    '''
    General configuration class
    '''
    LABEL_PATH = os.path.join('models', 'labels', 'parked_binary_labels.txt')
    with open(LABEL_PATH) as f:
        LABELS = f.readlines()

    with open(os.path.join('utils', 'image_grid.json')) as f:
        IMAGE_MAP = json.loads(f.read())

    MODEL_PATH = os.path.join(
        os.getcwd(), 'models', 'parking_detection_mobilenet_quant.tflite'
    )


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
