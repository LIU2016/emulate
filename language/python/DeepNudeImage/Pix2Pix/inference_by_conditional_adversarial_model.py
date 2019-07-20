import tensorflow as tf
import os
import sys
import time
import matplotlib.pyplot as plt
from conditional_adversarial_model import Generator, Discriminator
from dataset_utils import download_and_processing_pix2pix_dataset, predefined_task_name_list


def generate_images(idx, model, test_input, store_produce_image_dir):
    if not os.path.exists(store_produce_image_dir):
        os.mkdir(store_produce_image_dir)

    prediction = model(test_input)

    fig = plt.figure(figsize=(12, 12))

    display_list = [test_input[0], prediction[0]]
    title = ['Input Image', 'Predicted Image']

    for i in range(2):
        plt.subplot(1, 2, i + 1)
        plt.title(title[i])
        # getting the pixel values between [0, 1] to plot it.
        plt.imshow(display_list[i] * 0.5 + 0.5)
        plt.axis('off')
    save_image_path = os.path.join(store_produce_image_dir, 'image_at_{:04d}.png'.format(idx))
    plt.savefig(save_image_path)
    # plt.show()
    plt.close(fig)


class CycleGAN_Inference_Manager(object):
    def __init__(self, checkpoint_path='./training_checkpoints'):
        self.create_model_restore_weight(checkpoint_path)

    def create_model_restore_weight(self, checkpoint_dir):
        # create model
        self.generator = Generator()
        discriminator = Discriminator()

        generator_optimizer = tf.keras.optimizers.Adam(2e-4, beta_1=0.5)
        discriminator_optimizer = tf.keras.optimizers.Adam(2e-4, beta_1=0.5)

        checkpoint = tf.train.Checkpoint(generator_optimizer=generator_optimizer,
                                         discriminator_optimizer=discriminator_optimizer,
                                         generator=self.generator,
                                         discriminator=discriminator)

        ckpt_manager = tf.train.CheckpointManager(checkpoint, checkpoint_dir, max_to_keep=5)

        # if a checkpoint exists, restore the latest checkpoint.
        if ckpt_manager.latest_checkpoint:
            checkpoint.restore(ckpt_manager.latest_checkpoint)
            print('Latest checkpoint restored!')
        else:
            print("Not found checkpoint")

    def get_test_dataset(self, data_dir_or_predefined_task_name="edges2shoes", BATCH_SIZE=1):
        # prepare data
        _, test_dataset = download_and_processing_pix2pix_dataset(data_dir_or_predefined_task_name, BATCH_SIZE)
        return test_dataset


if __name__ == "__main__":
    # task_name and data_dir only need to provide one of them
    # data_dir_or_predefined_task_name = "/home/b418a/.keras/datasets/apple2orange"
    data_dir_or_predefined_task_name = "edges2shoes"

    print("You can choose a task_name from predefined_task_name_list!")
    print(predefined_task_name_list)

    if len(sys.argv) == 2:
        data_dir_or_predefined_task_name = sys.argv[1]
    print(f"You choose data_dir_or_predefined_task_name is {data_dir_or_predefined_task_name}")

    inference_data_number = 6
    BATCH_SIZE = 1
    checkpoint_path = "./checkpoints/train"
    store_produce_image_dir = 'inference_images'

    # create CycleGAN_Inference_Manager
    cyclegan_infer = CycleGAN_Inference_Manager(checkpoint_path)

    # prepare data
    test_dataset = cyclegan_infer.get_test_dataset(data_dir_or_predefined_task_name, BATCH_SIZE)

    # Run the trained model on the test dataset
    for idx, (input_image, real_image) in enumerate(test_dataset.take(inference_data_number)):
        generate_images(idx, cyclegan_infer.generator, input_image, store_produce_image_dir)
