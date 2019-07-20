import tensorflow as tf

import os
import sys
import matplotlib.pyplot as plt

predefined_task_name_list = ["cityscapes", "edges2handbags", "edges2shoes", "facades", "maps"]


def load_predefined_image_data_by_task_name(task_name):
    """Data from https://people.eecs.berkeley.edu/~tinghuiz/projects/pix2pix/datasets/
    View sample images here, https://github.com/yuanxiaosc/DeepNude-an-Image-to-Image-technology/tree/master/Pix2Pix"""

    if task_name in predefined_task_name_list:
        _URL = f'https://people.eecs.berkeley.edu/~tinghuiz/projects/pix2pix/datasets/{task_name}.tar.gz'
        path_to_zip = tf.keras.utils.get_file('edges2shoes.tar.gz', origin=_URL, extract=True)
        PATH = os.path.join(os.path.dirname(path_to_zip), 'edges2shoes/')
        print(f"Store {task_name} raw data to {PATH}")
    else:
        raise ValueError(f"Predefined tasks do not include this {task_name} task!")
    return PATH


def load(image_file):
    image = tf.io.read_file(image_file)
    image = tf.image.decode_jpeg(image)

    w = tf.shape(image)[1]

    w = w // 2

    input_image = image[:, :w, :]
    real_image = image[:, w:, :]

    input_image = tf.cast(input_image, tf.float32)
    real_image = tf.cast(real_image, tf.float32)

    return input_image, real_image


def download_and_processing_pix2pix_dataset(data_dir_or_predefined_task_name=None,
                                            BATCH_SIZE=1, BUFFER_SIZE=1000,
                                            IMG_HEIGHT=256, IMG_WIDTH=256):

    def resize(input_image, real_image, height, width):
        input_image = tf.image.resize(input_image, [height, width],
                                      method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
        real_image = tf.image.resize(real_image, [height, width],
                                     method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)

        return input_image, real_image

    # normalizing the images to [-1, 1]
    def normalize(input_image, real_image):
        input_image = (input_image / 127.5) - 1
        real_image = (real_image / 127.5) - 1

        return input_image, real_image

    def load_image_train(image_file):
        input_image, real_image = load(image_file)
        input_image, real_image = random_jitter(input_image, real_image)
        input_image, real_image = normalize(input_image, real_image)

        return input_image, real_image

    def load_image_test(image_file):
        input_image, real_image = load(image_file)
        input_image, real_image = resize(input_image, real_image,
                                         IMG_HEIGHT, IMG_WIDTH)
        input_image, real_image = normalize(input_image, real_image)

        return input_image, real_image

    def random_crop(input_image, real_image):
        stacked_image = tf.stack([input_image, real_image], axis=0)
        cropped_image = tf.image.random_crop(
            stacked_image, size=[2, IMG_HEIGHT, IMG_WIDTH, 3])

        return cropped_image[0], cropped_image[1]

    @tf.function()
    def random_jitter(input_image, real_image):
        # resizing to 286 x 286 x 3
        input_image, real_image = resize(input_image, real_image, 286, 286)

        # randomly cropping to 256 x 256 x 3
        input_image, real_image = random_crop(input_image, real_image)

        if tf.random.uniform(()) > 0.5:
            # random mirroring
            input_image = tf.image.flip_left_right(input_image)
            real_image = tf.image.flip_left_right(real_image)

        return input_image, real_image

    if data_dir_or_predefined_task_name in predefined_task_name_list:
        PATH = load_predefined_image_data_by_task_name(data_dir_or_predefined_task_name)
        print("prepare data from task_name")
    elif os.path.exists(data_dir_or_predefined_task_name):
        PATH = data_dir_or_predefined_task_name
        print("prepare data from data_dir")
    else:
        raise ValueError("Task_name error and data_dir does not exist!")

    train_dataset = tf.data.Dataset.list_files(PATH + 'train/*.jpg')
    train_dataset = train_dataset.shuffle(BUFFER_SIZE)
    train_dataset = train_dataset.map(load_image_train,
                                      num_parallel_calls=tf.data.experimental.AUTOTUNE)

    train_dataset = train_dataset.batch(BATCH_SIZE)

    test_dataset = tf.data.Dataset.list_files(PATH + 'val/*.jpg')

    # shuffling so that for every epoch a different image is generated
    # to predict and display the progress of our model.
    train_dataset = train_dataset.shuffle(BUFFER_SIZE)
    test_dataset = test_dataset.map(load_image_test)
    test_dataset = test_dataset.batch(BATCH_SIZE)

    return train_dataset, test_dataset


def check_one_dataset_info(data_dir_or_predefined_task_name, store_sample_image_path='check_dataset'):
    if not os.path.exists(store_sample_image_path):
        os.mkdir(store_sample_image_path)
    train_dataset, test_dataset = download_and_processing_pix2pix_dataset(data_dir_or_predefined_task_name)
    i = 0
    for sample_inp, sample_re in train_dataset.take(3):
        inp, re = sample_inp, sample_re
        # casting to int for matplotlib to show the image
        plt.figure()
        plt.imshow(inp[0] * 0.5 + 0.5)
        plt.savefig(os.path.join(store_sample_image_path, f"{i}_example_input.png"))
        plt.figure()
        plt.imshow(re[0] * 0.5 + 0.5)
        plt.savefig(os.path.join(store_sample_image_path, f"{i}_example_target.png"))
        i += 1


if __name__ == "__main__":
    print("You can choose a task_name from predefined_task_name_list!")
    print(predefined_task_name_list)
    #data_dir_or_predefined_task_name = "/home/b418a/.keras/datasets/edges2shoes/"
    data_dir_or_predefined_task_name = "edges2shoes"

    if len(sys.argv) == 2:
        data_dir_or_predefined_task_name = sys.argv[1]
    print(f"You choose data_dir_or_predefined_task_name is {data_dir_or_predefined_task_name}")

    check_one_dataset_info(data_dir_or_predefined_task_name, store_sample_image_path="check_dataset")

    train_dataset, test_dataset = download_and_processing_pix2pix_dataset(data_dir_or_predefined_task_name)
    for image_input_batch, image_target_batch in train_dataset.take(1):
        print(f"image_input_batch.shape: {image_input_batch.shape}")
        print(f"image_target_batch.shape: {image_target_batch.shape}")
        print("")
