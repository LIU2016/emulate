import tensorflow as tf
import os
import sys
import time
import matplotlib.pyplot as plt
from conditional_adversarial_model import Generator, Discriminator, generator_loss, discriminator_loss
from dataset_utils import download_and_processing_pix2pix_dataset, predefined_task_name_list


def generate_images(epoch, model, test_input, tar, store_produce_image_dir):
    # the training=True is intentional here since
    # we want the batch statistics while running the model
    # on the test dataset. If we use training=False, we will get
    # the accumulated statistics learned from the training dataset
    # (which we don't want)
    if not os.path.exists(store_produce_image_dir):
        os.mkdir(store_produce_image_dir)

    prediction = model(test_input, training=True)
    fig = plt.figure(figsize=(15, 15))

    display_list = [test_input[0], tar[0], prediction[0]]
    title = ['Input Image', 'Ground Truth', 'Predicted Image']

    for i in range(3):
        plt.subplot(1, 3, i + 1)
        plt.title(title[i])
        # getting the pixel values between [0, 1] to plot it.
        plt.imshow(display_list[i] * 0.5 + 0.5)
        plt.axis('off')
    save_image_path = os.path.join(store_produce_image_dir, 'image_at_epoch_{:04d}.png'.format(epoch))
    plt.savefig(save_image_path)
    #plt.show()
    plt.close(fig)


def main(data_dir_or_predefined_task_name="apple2orange", EPOCHS=200, BATCH_SIZE=1,
         store_produce_image_dir="train_produce_images", checkpoint_dir="./checkpoints/train"):
    @tf.function
    def train_step(input_image, target):
        with tf.GradientTape() as gen_tape, tf.GradientTape() as disc_tape:
            gen_output = generator(input_image, training=True)

            disc_real_output = discriminator([input_image, target], training=True)
            disc_generated_output = discriminator([input_image, gen_output], training=True)

            gen_loss = generator_loss(disc_generated_output, gen_output, target)
            disc_loss = discriminator_loss(disc_real_output, disc_generated_output)

        generator_gradients = gen_tape.gradient(gen_loss, generator.trainable_variables)
        discriminator_gradients = disc_tape.gradient(disc_loss, discriminator.trainable_variables)

        generator_optimizer.apply_gradients(zip(generator_gradients, generator.trainable_variables))
        discriminator_optimizer.apply_gradients(zip(discriminator_gradients, discriminator.trainable_variables))

    def train(dataset, epochs):
        for epoch in range(epochs):
            start = time.time()

            for input_image, target in dataset:
                train_step(input_image, target)

            for inp, tar in test_dataset.take(1):
                generate_images(epoch, generator, inp, tar, store_produce_image_dir)

            # saving (checkpoint) the model every 5 epochs
            if (epoch + 1) % 5 == 0:
                checkpoint.save(file_prefix=checkpoint_prefix)

            print('Time taken for epoch {} is {} sec\n'.format(epoch + 1, time.time() - start))

    # prepare data
    train_dataset, test_dataset = download_and_processing_pix2pix_dataset(data_dir_or_predefined_task_name, BATCH_SIZE)

    # create model
    generator = Generator()
    discriminator = Discriminator()

    generator_optimizer = tf.keras.optimizers.Adam(2e-4, beta_1=0.5)
    discriminator_optimizer = tf.keras.optimizers.Adam(2e-4, beta_1=0.5)

    checkpoint_prefix = os.path.join(checkpoint_dir, "ckpt")
    checkpoint = tf.train.Checkpoint(generator_optimizer=generator_optimizer,
                                     discriminator_optimizer=discriminator_optimizer,
                                     generator=generator,
                                     discriminator=discriminator)

    ckpt_manager = tf.train.CheckpointManager(checkpoint, checkpoint_dir, max_to_keep=10)

    # if a checkpoint exists, restore the latest checkpoint.
    if ckpt_manager.latest_checkpoint:
        checkpoint.restore(ckpt_manager.latest_checkpoint)
        print('Latest checkpoint restored!')

    train(train_dataset, EPOCHS)


if __name__ == "__main__":
    print("You can choose a task_name from predefined_task_name_list!")
    print(predefined_task_name_list)
    # data_dir_or_predefined_task_name = "/home/b418a/.keras/datasets/edges2shoes/"
    data_dir_or_predefined_task_name = "edges2shoes"

    if len(sys.argv) == 2:
        data_dir_or_predefined_task_name = sys.argv[1]
    print(f"You choose data_dir_or_predefined_task_name is {data_dir_or_predefined_task_name}")

    EPOCHS = 200
    BATCH_SIZE = 10

    store_produce_image_dir = "train_produce_images"
    checkpoint_dir = "./checkpoints/train"


    main(data_dir_or_predefined_task_name, EPOCHS, BATCH_SIZE, store_produce_image_dir, checkpoint_dir)
