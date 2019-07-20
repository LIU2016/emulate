import tensorflow as tf
import matplotlib.pyplot as plt

def load_raw_img(path_to_img):
    img = tf.io.read_file(path_to_img)
    img = tf.image.decode_image(img, channels=3)
    img = tf.image.convert_image_dtype(img, tf.float32)
    img = img[tf.newaxis, :]
    return img

def load_img_and_reshape(path_to_img):
    max_dim = 512
    img = tf.io.read_file(path_to_img)
    img = tf.image.decode_image(img, channels=3)
    img = tf.image.convert_image_dtype(img, tf.float32)

    shape = tf.cast(tf.shape(img)[:-1], tf.float32)
    tf.print(f"raw_img_shape {shape}")
    long_dim = max(shape)
    scale = max_dim / long_dim

    new_shape = tf.cast(shape * scale, tf.int32)
    tf.print(f"new_shape {new_shape}")
    img = tf.image.resize(img, new_shape)
    img = img[tf.newaxis, :]
    return img


def imshow(image, title=None):
    if len(image.shape) > 3:
        image = tf.squeeze(image, axis=0)

    plt.imshow(image)
    #if title:
    #    plt.title(title)
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())
    plt.subplots_adjust(top=1, bottom=0, left=0, right=1, hspace=0, wspace=0)
    plt.margins(0, 0)
    plt.axis('off')
    plt.savefig(f"{title}.png")
    plt.close()


def recovery_to_raw_image_shape(path_to_raw_img, path_to_produce_img):
    raw_img = tf.io.read_file(path_to_raw_img)
    raw_img = tf.image.decode_image(raw_img, channels=3)
    tf.print(f"raw_img_shape {tf.shape(raw_img)[:-1]}")

    produce_img = tf.io.read_file(path_to_produce_img)
    produce_img = tf.image.decode_image(produce_img, channels=3)
    produce_img = tf.image.convert_image_dtype(produce_img, tf.float32)
    tf.print(f"produce_img_shape {tf.shape(produce_img)[:-1]}")
    produce_img = tf.image.resize(produce_img, tf.shape(raw_img)[:-1])
    tf.print(f"recovery produce_img_shape {tf.shape(produce_img)[:-1]}")
    produce_img = produce_img[tf.newaxis, :]
    return produce_img

content_path = "/home/b418a/disk1/pycharm_room/yuanxiao/my_lenovo_P50s/Neural_style_transfer/datasets/content.jpg"
path_to_produce_img = "/home/b418a/disk1/pycharm_room/yuanxiao/my_lenovo_P50s/Neural_style_transfer/Reshape Content Image.png"

raw_content_image = load_raw_img(content_path)
imshow(raw_content_image, 'Raw Content Image')

reshape_content_image = load_img_and_reshape(content_path)
imshow(reshape_content_image, 'Reshape Content Image')

recovery_content_image = recovery_to_raw_image_shape(content_path, path_to_produce_img)
imshow(recovery_content_image, 'recovery Content Image')