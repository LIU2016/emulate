import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import time
import os

from vae_model import CVAE
from dataset_utils import get_celebface_dataset


def log_normal_pdf(sample, mean, logvar, raxis=1):
    log2pi = tf.math.log(2. * np.pi)
    return tf.reduce_sum(
        -.5 * ((sample - mean) ** 2. * tf.exp(-logvar) + logvar + log2pi), axis=raxis)


def compute_loss(model, x):
    mean, logvar = model.encode(x)
    z = model.reparameterize(mean, logvar)
    x_logit = model.decode(z)

    cross_ent = tf.nn.sigmoid_cross_entropy_with_logits(logits=x_logit, labels=x)
    logpx_z = -tf.reduce_sum(cross_ent, axis=[1, 2, 3])
    logpz = log_normal_pdf(z, 0., 0.)
    logqz_x = log_normal_pdf(z, mean, logvar)
    return -tf.reduce_mean(logpx_z + logpz - logqz_x)


def compute_gradients(model, x):
    with tf.GradientTape() as tape:
        loss = compute_loss(model, x)
    return tape.gradient(loss, model.trainable_variables), loss


def apply_gradients(optimizer, gradients, variables):
    optimizer.apply_gradients(zip(gradients, variables))


def generate_and_save_images(model, epoch, test_input, store_produce_image_dir):
    if not os.path.exists(store_produce_image_dir):
        os.mkdir(store_produce_image_dir)

    predictions = model.sample(test_input)
    fig = plt.figure(figsize=(4, 4))

    for i in range(predictions.shape[0]):
        if i < 16:
            plt.subplot(4, 4, i + 1)
            plt.imshow(predictions[i])
            plt.axis('off')

    # tight_layout minimizes the overlap between 2 sub-plots
    plt.savefig(os.path.join(store_produce_image_dir, 'image_at_epoch_{:04d}.png'.format(epoch)))
    # plt.show()
    plt.close(fig)


def main(epochs, latent_dim, num_examples_to_generate, data_dir, BATCH_SIZE, checkpoint_dir, store_produce_image_dir):
    # keeping the random vector constant for generation (prediction) so
    # it will be easier to see the improvement.
    random_vector_for_generation = tf.random.normal(
        shape=[num_examples_to_generate, latent_dim])

    # create model
    model = CVAE(latent_dim)
    optimizer = tf.keras.optimizers.Adam(1e-4)

    checkpoint = tf.train.Checkpoint(optimizer=optimizer, model=model)

    ckpt_manager = tf.train.CheckpointManager(checkpoint, checkpoint_dir, max_to_keep=10)

    start_epoch = 0
    # if a checkpoint exists, restore the latest checkpoint.
    if ckpt_manager.latest_checkpoint:
        start_epoch = int(ckpt_manager.latest_checkpoint.split('-')[-1])
        checkpoint.restore(ckpt_manager.latest_checkpoint)
        print(f'Latest checkpoint restored! start_epoch is {start_epoch}')

    generate_and_save_images(model, 0, random_vector_for_generation, store_produce_image_dir)

    # prepare data
    train_dataset, test_dataset = get_celebface_dataset(celebface_data_dir=data_dir, BATCH_SIZE=BATCH_SIZE)

    for epoch in range(start_epoch, epochs + 1):
        start_time = time.time()
        for train_x in train_dataset:
            gradients, loss = compute_gradients(model, train_x)
            apply_gradients(optimizer, gradients, model.trainable_variables)
        end_time = time.time()

        if epoch % 1 == 0:
            loss = tf.keras.metrics.Mean()
            for test_x in test_dataset:
                loss(compute_loss(model, test_x))
            ELBO = -loss.result()

            print(f'Epoch: {epoch}, Test set ELBO: {ELBO}, time elapse for current epoch {end_time - start_time}')
            generate_and_save_images(model, epoch, random_vector_for_generation, store_produce_image_dir)

        # Save the model every 10 epochs
        if (epoch + 1) % 3 == 0:
            checkpoint.save()


if __name__ == "__main__":
    epochs = 100
    BATCH_SIZE = 64
    latent_dim = 50
    num_examples_to_generate = 16
    data_dir = "/home/b418a/.keras/datasets/celeba-dataset/img_align_celeba"
    checkpoint_dir = './training_checkpoints'
    store_produce_image_dir = "train_produce_images"

    main(epochs, latent_dim, num_examples_to_generate, data_dir, BATCH_SIZE, checkpoint_dir, store_produce_image_dir)
