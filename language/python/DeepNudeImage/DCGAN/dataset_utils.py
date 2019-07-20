import tensorflow as tf
import glob
import os


def get_celebface_dataset(celebface_data_dir, new_height=218, new_width=178, BATCH_SIZE=128, BUFFER_SIZE=200000):
    if not os.path.exists(celebface_data_dir):
        print("download data from https://www.kaggle.com/jessicali9530/celeba-dataset/home")
        raise ValueError("Not found celebface_data_dir")

    def load_image(image_path):
        img = tf.io.read_file(image_path)
        img = tf.image.decode_jpeg(img, channels=3)
        img = tf.image.resize(img, (new_height, new_width))
        img = (img / 127.5) - 1
        return img

    filenames = glob.glob(os.path.join(celebface_data_dir, "*.jpg"))
    filenames = sorted(filenames)
    celebface_image_path_dataset = tf.data.Dataset.from_tensor_slices(filenames)
    celebface_image_dataset = celebface_image_path_dataset.map(load_image,
                                                               num_parallel_calls=tf.data.experimental.AUTOTUNE)

    # Batch and shuffle the data
    celebface_image_dataset = celebface_image_dataset.shuffle(BUFFER_SIZE).batch(BATCH_SIZE)
    celebface_image_dataset = celebface_image_dataset.prefetch(buffer_size=tf.data.experimental.AUTOTUNE)

    return celebface_image_dataset


if __name__ == "__main__":
    celebface_data_dir = "/home/b418a/.keras/datasets/celeba-dataset/img_align_celeba"
    celebface_image_dataset = get_celebface_dataset(celebface_data_dir, new_height=218, new_width=178,
                                                    BATCH_SIZE=128, BUFFER_SIZE=20000)
    for batch_image in celebface_image_dataset.take(3):
        print(f"batch_image.shape {batch_image.shape}")
        # print(f"batch_image.numpy() {batch_image.numpy()}")
        print(f"batch_image[0, :, :, 0].numpy() \n{batch_image[0, :, :, 0].numpy()}")
