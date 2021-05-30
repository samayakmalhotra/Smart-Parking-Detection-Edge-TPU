import os
import argparse

import tensorflow as tf
from tensorflow.keras.models import load_model


IMAGE_SIZE = 96

parser = argparse.ArgumentParser()
parser.add_argument(
    '-m',
    '--model_path',
    default=os.path.join(os.getcwd(), 'models', 'model.h5'),
    help='model to be converted'
)
parser.add_argument(
    '-o',
    '--output_path',
    default=os.path.join(os.getcwd(), 'models', 'model.h5'),
    help='model output path'
)
parser.add_argument(
    '-r',
    '--rep_data_path',
    default=os.path.join(os.getcwd(), 'data'),
    help='Representative data path'
)

args = parser.parse_args()

def representative_data_gen():
    dataset_list = tf.data.Dataset.list_files(
        args.rep_data_path + '/*/*'
    )
    for i in range(100):
        image = next(iter(dataset_list))
        image = tf.io.read_file(image)
        image = tf.io.decode_png(image, channels=3)
        image = tf.image.resize(image, [IMAGE_SIZE, IMAGE_SIZE])
        # image = tf.cast(image / 255., tf.float32)
        image = tf.expand_dims(image, 0)
        yield [image]


converter = tf.lite.TFLiteConverter.from_keras_model_file(args.model_path)
converter.optimizations = [tf.lite.Optimize.DEFAULT]

converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]

converter.inference_input_type = tf.uint8
converter.inference_output_type = tf.uint8

converter.representative_dataset = representative_data_gen
tflite_model = converter.convert()

with open(args.output_path, 'wb') as f:
    f.write(tflite_model)
