import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import time
import os

from vae_model import CVAE
from dataset_utils import get_celebface_dataset



def generate_and_save_images(model, store_produce_image_dir):
    if not os.path.exists(store_produce_image_dir):
        os.mkdir(store_produce_image_dir)

    predictions = model.sample()
    fig = plt.figure(figsize=(4, 4))

    for i in range(predictions.shape[0]):
        if i < 16:
            plt.subplot(4, 4, i + 1)
            plt.imshow(predictions[i])
            plt.axis('off')

    # tight_layout minimizes the overlap between 2 sub-plots
    plt.savefig(os.path.join(store_produce_image_dir, 'inference_image.png'))
    # plt.show()
    plt.close(fig)

def create_vae_model(latent_dim):
    # create model
    model = CVAE(latent_dim)
    optimizer = tf.keras.optimizers.Adam(1e-4)

    checkpoint = tf.train.Checkpoint(optimizer=optimizer, model=model)

    ckpt_manager = tf.train.CheckpointManager(checkpoint, checkpoint_dir, max_to_keep=10)

    # if a checkpoint exists, restore the latest checkpoint.
    if ckpt_manager.latest_checkpoint:
        checkpoint.restore(ckpt_manager.latest_checkpoint)
        print(f'Latest checkpoint restored!')

    return model

if __name__ == "__main__":
    epochs = 100
    BATCH_SIZE = 64
    latent_dim = 50
    num_examples_to_generate = 16
    checkpoint_dir = './training_checkpoints'
    store_produce_image_dir = "inference_produce_images"

    model = create_vae_model(latent_dim)
    generate_and_save_images(model, store_produce_image_dir)
