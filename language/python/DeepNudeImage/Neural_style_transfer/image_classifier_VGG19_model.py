import tensorflow as tf
import numpy as np


class ImageClassifierBaseOnVGG19(object):
    """https://keras.io/applications/#vgg19"""
    def __init__(self):
        self.VGG19 = tf.keras.applications.VGG19(include_top=True, weights='imagenet')
        self.labels_path = tf.keras.utils.get_file(
            'ImageNetLabels.txt', 'https://storage.googleapis.com/download.tensorflow.org/data/ImageNetLabels.txt')
        self.imagenet_labels = np.array(open(self.labels_path).read().splitlines())

    def load_img(self, path_to_img):
        """Define a function to load an image and limit its maximum dimension to 512 pixels."""
        max_dim = 512
        img = tf.io.read_file(path_to_img)
        img = tf.image.decode_image(img, channels=3)
        img = tf.image.convert_image_dtype(img, tf.float32)

        shape = tf.cast(tf.shape(img)[:-1], tf.float32)
        long_dim = max(shape)
        scale = max_dim / long_dim

        new_shape = tf.cast(shape * scale, tf.int32)

        img = tf.image.resize(img, new_shape)
        img = img[tf.newaxis, :]
        return img

    def classify(self, image_path, top_k=10):
        image = self.load_img(image_path)
        x = tf.keras.applications.vgg19.preprocess_input(image * 255)
        x = tf.image.resize(x, (224, 224))  # The default input size for VGG19 model is 224x224.
        results = self.VGG19(x)
        decode_predictions = tf.keras.applications.vgg19.decode_predictions(results.numpy())
        predict_img_label_list = self.imagenet_labels[np.argsort(results)[0, ::-1][:top_k] + 1]
        return predict_img_label_list, decode_predictions


if __name__ == "__main__":
    img_classifier = ImageClassifierBaseOnVGG19()
    image_path = tf.keras.utils.get_file(fname='samoyed_dog.jpg',
                                         origin='https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1561387878331&di=033973e3a9e7fb2581914e5409055b8c&imgtype=0&src=http%3A%2F%2Fgss0.baidu.com%2F-vo3dSag_xI4khGko9WTAnF6hhy%2Fzhidao%2Fpic%2Fitem%2Fd043ad4bd11373f08779bd0ba60f4bfbfaed04db.jpg',
                                         cache_dir='.')

    predict_img_label_list, decode_predictions = img_classifier.classify(image_path, top_k=5)
    print(f"predict_img_label_list {predict_img_label_list}")
    print(f"decode_predictions {decode_predictions}")
