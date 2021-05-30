from flask import current_app
from PIL import Image
import numpy as np
import tflite_runtime.interpreter as tflite

import app.parking_detector.classify as classify
from config import Config


def load_labels(path, encoding='utf-8'):
    """Loads labels from file (with or without index numbers).
    Args:
        path: path to label file.
        encoding: label file encoding.
    Returns:
        Dictionary mapping indices to labels.
    """
    with open(path, 'r', encoding=encoding) as f:
        lines = f.readlines()
        if not lines:
            return {}

        if lines[0].split(' ', maxsplit=1)[0].isdigit():
            pairs = [line.split(' ', maxsplit=1) for line in lines]
            return {int(index): label.strip() for index, label in pairs}
        else:
            return {index: line.strip() for index, line in enumerate(lines)}


def make_interpreter(model_file):
    model_file, *device = model_file.split('@')
    return tflite.Interpreter(
        model_path=model_file,
        # experimental_delegates=[
        #     tflite.load_delegate(EDGETPU_SHARED_LIB,
        #                         {'device': device[0]} if device else {})
        # ]
    )


labels = load_labels(Config.LABEL_PATH)
interpreter = make_interpreter(
    model_file=Config.MODEL_PATH
)
interpreter.allocate_tensors()


def make_inference(img):
    size = classify.input_size(interpreter)
    image = img.convert('RGB').resize(size, Image.ANTIALIAS)
    classify.set_input(interpreter, image)

    interpreter.invoke()
    classes = classify.get_output(interpreter)

    return labels[classes[0]] if classes else None
