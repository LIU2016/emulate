import tensorflow as tf
import matplotlib.pyplot as plt
import sys
import os
import time
from dataset_utils import download_and_processing_cyclegan_dataset, predefined_cyclegan_task_name_list
from cyclegan_model import unet_generator, discriminator, \
    generator_loss, discriminator_loss, calc_cycle_loss, identity_loss


def generate_images(epoch, model, test_input, store_produce_image_dir):
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
    save_image_path = os.path.join(store_produce_image_dir, 'image_at_epoch_{:04d}.png'.format(epoch))
    plt.savefig(save_image_path)
    #plt.show()
    plt.close(fig)


def main(data_dir_or_predefined_task_name="apple2orange", EPOCHS=200, BATCH_SIZE=1, OUTPUT_CHANNELS=3,
         store_produce_image_dir="train_produce_images", checkpoint_path = "./checkpoints/train"):

    @tf.function
    def train_step(real_x, real_y):
        # persistent is set to True because gen_tape and disc_tape is used more than
        # once to calculate the gradients.
        with tf.GradientTape(persistent=True) as gen_tape, tf.GradientTape(
                persistent=True) as disc_tape:
            # Generator G translates X -> Y
            # Generator F translates Y -> X.

            fake_y = generator_g(real_x, training=True)
            cycled_x = generator_f(fake_y, training=True)

            fake_x = generator_f(real_y, training=True)
            cycled_y = generator_g(fake_x, training=True)

            # same_x and same_y are used for identity loss.
            same_x = generator_f(real_x, training=True)
            same_y = generator_g(real_y, training=True)

            disc_real_x = discriminator_x(real_x, training=True)
            disc_real_y = discriminator_y(real_y, training=True)

            disc_fake_x = discriminator_x(fake_x, training=True)
            disc_fake_y = discriminator_y(fake_y, training=True)

            # calculate the loss
            gen_g_loss = generator_loss(disc_fake_y)
            gen_f_loss = generator_loss(disc_fake_x)

            # Total generator loss = adversarial loss + cycle loss
            total_gen_g_loss = gen_g_loss + calc_cycle_loss(real_x, cycled_x) + identity_loss(real_x, same_x)
            total_gen_f_loss = gen_f_loss + calc_cycle_loss(real_y, cycled_y) + identity_loss(real_y, same_y)

            disc_x_loss = discriminator_loss(disc_real_x, disc_fake_x)
            disc_y_loss = discriminator_loss(disc_real_y, disc_fake_y)

        # Calculate the gradients for generator and discriminator
        generator_g_gradients = gen_tape.gradient(total_gen_g_loss,
                                                  generator_g.trainable_variables)
        generator_f_gradients = gen_tape.gradient(total_gen_f_loss,
                                                  generator_f.trainable_variables)

        discriminator_x_gradients = disc_tape.gradient(
            disc_x_loss, discriminator_x.trainable_variables)
        discriminator_y_gradients = disc_tape.gradient(
            disc_y_loss, discriminator_y.trainable_variables)

        # Apply the gradients to the optimizer
        generator_g_optimizer.apply_gradients(zip(generator_g_gradients,
                                                  generator_g.trainable_variables))

        generator_f_optimizer.apply_gradients(zip(generator_f_gradients,
                                                  generator_f.trainable_variables))

        discriminator_x_optimizer.apply_gradients(
            zip(discriminator_x_gradients,
                discriminator_x.trainable_variables))

        discriminator_y_optimizer.apply_gradients(
            zip(discriminator_y_gradients,
                discriminator_y.trainable_variables))

    # prepare data
    trainA_dataset, trainB_dataset, _, _ = download_and_processing_cyclegan_dataset(data_dir_or_predefined_task_name, BATCH_SIZE)

    # create model
    # B = generator_g(A), A = generator_f(B)
    generator_g = unet_generator(OUTPUT_CHANNELS, norm_type='instancenorm')
    generator_f = unet_generator(OUTPUT_CHANNELS, norm_type='instancenorm')

    discriminator_x = discriminator(norm_type='instancenorm', target=False)
    discriminator_y = discriminator(norm_type='instancenorm', target=False)

    generator_g_optimizer = tf.keras.optimizers.Adam(2e-4, beta_1=0.5)
    generator_f_optimizer = tf.keras.optimizers.Adam(2e-4, beta_1=0.5)

    discriminator_x_optimizer = tf.keras.optimizers.Adam(2e-4, beta_1=0.5)
    discriminator_y_optimizer = tf.keras.optimizers.Adam(2e-4, beta_1=0.5)

    ckpt = tf.train.Checkpoint(generator_g=generator_g,
                               generator_f=generator_f,
                               discriminator_x=discriminator_x,
                               discriminator_y=discriminator_y,
                               generator_g_optimizer=generator_g_optimizer,
                               generator_f_optimizer=generator_f_optimizer,
                               discriminator_x_optimizer=discriminator_x_optimizer,
                               discriminator_y_optimizer=discriminator_y_optimizer)

    ckpt_manager = tf.train.CheckpointManager(ckpt, checkpoint_path, max_to_keep=5)

    # if a checkpoint exists, restore the latest checkpoint.
    if ckpt_manager.latest_checkpoint:
        ckpt.restore(ckpt_manager.latest_checkpoint)
        print('Latest checkpoint restored!!')

    # train model
    for epoch in range(EPOCHS):
        start = time.time()

        n = 0
        for image_x, image_y in tf.data.Dataset.zip((trainA_dataset, trainB_dataset)):
            train_step(image_x, image_y)
            if n % 10 == 0:
                print('.', end='')
            n += 1

        # Using a consistent image (sample_A) so that the progress of the model
        # is clearly visible.
        generate_images(epoch, generator_g, image_x, store_produce_image_dir)

        if (epoch + 1) % 10 == 0:
            ckpt_save_path = ckpt_manager.save()
            print('Saving checkpoint for epoch {} at {}'.format(epoch + 1, ckpt_save_path))

        print('Time taken for epoch {} is {} sec\n'.format(epoch + 1, time.time() - start))


if __name__=="__main__":
    print("You can choose a task_name from predefined_cyclegan_task_name_list!")
    print(predefined_cyclegan_task_name_list)
    # task_name and data_dir only need to provide one of them
    #data_dir_or_predefined_task_name = "/home/b418a/.keras/datasets/apple2orange"
    data_dir_or_predefined_task_name = "apple2orange"

    EPOCHS = 200
    BATCH_SIZE = 10
    OUTPUT_CHANNELS = 3
    store_produce_image_dir = "train_produce_images"
    checkpoint_path = "./checkpoints/train"

    if len(sys.argv) == 2:
        data_dir_or_predefined_task_name = sys.argv[1]
    print(f"You choose data_dir_or_predefined_task_name is {data_dir_or_predefined_task_name}")

    main(data_dir_or_predefined_task_name, EPOCHS, BATCH_SIZE, OUTPUT_CHANNELS, store_produce_image_dir, checkpoint_path)
