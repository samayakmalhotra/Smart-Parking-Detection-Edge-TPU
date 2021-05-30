import os
import argparse
import random
import secrets
import logging

import imageio
import imgaug as ia
import imgaug.augmenters as iaa
import numpy as np


parser = argparse.ArgumentParser()
parser.add_argument('--in_dir', help="Input Directory")
parser.add_argument('--out_dir', help='Output directory')
parser.add_argument('--save_original', action='store_true')

args = parser.parse_args()

logging.basicConfig(level=logging.INFO)

for filename in os.listdir(args.in_dir):
    image = imageio.imread(os.path.join(
        os.getcwd(),
        args.in_dir,
        filename
    ))

    rotate = iaa.Affine(rotate=(-50, 30))
    rotated_image = rotate.augment_image(image)
    imageio.imsave(
        os.path.join(
            args.out_dir, f'{secrets.token_hex(12)}.png'
        ), rotated_image
    )
    logging.info(f'Rotated {filename} image saved')

    gaussian_noise = iaa.AdditiveGaussianNoise(10, 20)
    noise_image = gaussian_noise.augment_image(image)
    imageio.imsave(
        os.path.join(args.out_dir, f'{secrets.token_hex(12)}.png'), noise_image
        )
    logging.info(f'Gaussian {filename} image saved')

    crop = iaa.Crop(percent=(
        round(random.choices(np.arange(0, 0.4, 0.1))[0], 2),
        round(random.choices(np.arange(0, 0.4, 0.1))[0], 2)
    ))
    crop_image = crop.augment_image(image)
    imageio.imsave(
        os.path.join(args.out_dir, f'{secrets.token_hex(12)}.png'), crop_image
    )
    logging.info(f'Crop {filename} image saved')

    flip_hr = iaa.Fliplr(p=1.0)
    flip_hr_image = flip_hr.augment_image(image)
    imageio.imsave(
        os.path.join(
            args.out_dir, f'{secrets.token_hex(12)}.png'
        ), flip_hr_image
    )
    logging.info(f'Flip {filename} image saved')

    contrast = iaa.GammaContrast(gamma=random.choices(range(1, 4)))
    contrast_image = contrast.augment_image(image)
    imageio.imsave(
        os.path.join(
            args.out_dir, f'{secrets.token_hex(12)}.png'
        ), contrast_image
    )
    logging.info(f'Contrast Shift {filename} image saved')

    scale_im = iaa.Affine(
        scale={
            'x': (1.0, round(random.choices(np.arange(1.1, 1.7, 0.1))[0], 2)),
            'y': (1.0, round(random.choices(np.arange(1.1, 1.7, 0.1))[0], 2))
        }
    )
    scale_image = scale_im.augment_image(image)
    imageio.imsave(
        os.path.join(args.out_dir, f'{secrets.token_hex(12)}.png'), scale_image
    )
    logging.info(f'Rotated {filename} image saved')

    if args.save_original:
        imageio.imsave(
            os.path.join(
                args.out_dir, f'{secrets.token_hex(12)}.png'
            ), image
        )
        logging.info(f'original {filename} image saved')
