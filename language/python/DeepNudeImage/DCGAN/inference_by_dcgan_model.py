import os
import matplotlib.pyplot as plt
import tensorflow as tf

from dcgan_model import Generator, Discriminator, discriminator_loss, generator_loss, max_min_normal_matrix


class DCGAN_Inference_Manager(object):
    def __init__(self, checkpoint_dir='./training_checkpoints'):
        self.create_model_restore_weight(checkpoint_dir)

    def create_model_restore_weight(self, checkpoint_dir):
        # create model
        self.generator = Generator()
        self.discriminator = Discriminator()

        # restore model weights
        generator_optimizer = tf.keras.optimizers.Adam(1e-4)
        discriminator_optimizer = tf.keras.optimizers.Adam(1e-4)

        checkpoint = tf.train.Checkpoint(generator_optimizer=generator_optimizer,
                                         discriminator_optimizer=discriminator_optimizer,
                                         generator=self.generator,
                                         discriminator=self.discriminator)

        ckpt_manager = tf.train.CheckpointManager(checkpoint, checkpoint_dir, max_to_keep=5)

        # if a checkpoint exists, restore the latest checkpoint.
        if ckpt_manager.latest_checkpoint:
            checkpoint.restore(ckpt_manager.latest_checkpoint)
            print('Latest checkpoint restored!')

    def produce_images(self, batch_size, noise_dim=100):
        noise = tf.random.normal([batch_size, noise_dim])
        generated_images = self.generator(noise, training=False)
        return generated_images

    def save_images(self, generated_images, store_produce_image_dir="inference_produce_images"):
        if not os.path.exists(store_produce_image_dir):
            os.mkdir(store_produce_image_dir)

        number = 1
        for image in generated_images:
            #plt.imshow(max_min_normal_matrix(image.numpy()))
            plt.imshow(image.numpy() * 0.5 + 0.5)
            plt.axis('off')
            save_image_path = os.path.join(store_produce_image_dir, '{:04d}.png'.format(number))
            plt.savefig(save_image_path)
            number += 1


if __name__ == "__main__":
    checkpoint_dir = './training_checkpoints'
    batch_size = 5
    store_produce_image_dir = "inference_produce_images"

    infer_manger = DCGAN_Inference_Manager(checkpoint_dir)
    generated_images = infer_manger.produce_images(batch_size)
    infer_manger.save_images(generated_images, store_produce_image_dir)
