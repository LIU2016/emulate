import tensorflow as tf
import matplotlib.pyplot as plt
import os
import time

from image_style_transfer_model import StyleContentModel


def load_img(path_to_img):
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


class ImageTransferBaseOnVGG19(object):

    def __init__(self, style_layers=None, content_layers=None, show_all_optional_layer_name=False, learning_rate=0.02,
                 beta_1=0.99, epsilon=1e-1):
        self.extractor = StyleContentModel(style_layers, content_layers, show_all_optional_layer_name)
        self.opt = tf.optimizers.Adam(learning_rate, beta_1, epsilon)

    def clip_0_1(self, image):
        return tf.clip_by_value(image, clip_value_min=0.0, clip_value_max=1.0)

    def VGG19_imshow(self, image, title=None, produce_image_file=None):
        if len(image.shape) > 3:
            image = tf.squeeze(image, axis=0)
        if title:
            plt.title(title)
        plt.imshow(image)
        plt.savefig(os.path.join(produce_image_file, title + ".png"))
        plt.close()

    @tf.function()
    def train_step(self, produce_image, total_variation_weight=1e8):
        with tf.GradientTape() as tape:
            outputs = self.extractor(produce_image)
            loss = self.style_content_loss(outputs)
            loss += total_variation_weight * self.total_variation_loss(produce_image)

        grad = tape.gradient(loss, produce_image)
        self.opt.apply_gradients([(grad, produce_image)])
        produce_image.assign(self.clip_0_1(produce_image))

    def transfer(self, content_image, style_image, produce_image_file="produce_images", epochs=5, steps_per_epoch=100):
        if not os.path.exists(produce_image_file):
            os.mkdir(produce_image_file)
        self.content_image = content_image
        self.style_targets = self.extractor(style_image)['style']
        self.content_targets = self.extractor(content_image)['content']

        # Define a tf.Variable to contain the image to optimize.
        # To make this quick, initialize it with the content image
        # (the tf.Variable must be the same shape as the content image):
        produce_image = tf.Variable(self.content_image)

        start = time.time()
        step = 0
        for n in range(epochs):
            for m in range(steps_per_epoch):
                step += 1
                self.train_step(produce_image)
                tf.print(".", end='')
            self.VGG19_imshow(produce_image.read_value(),
                              title=f"{step}_steps", produce_image_file=produce_image_file)
        end = time.time()
        tf.print("Total time: {:.1f}".format(end - start))

    def style_content_loss(self, outputs, style_weight=1e-2, content_weight=1e4):
        style_outputs = outputs['style']
        content_outputs = outputs['content']
        style_loss = tf.add_n([tf.reduce_mean((style_outputs[name] - self.style_targets[name]) ** 2)
                               for name in style_outputs.keys()])
        style_loss *= style_weight / self.extractor.num_style_layers

        content_loss = tf.add_n([tf.reduce_mean((content_outputs[name] - self.content_targets[name]) ** 2)
                                 for name in content_outputs.keys()])
        content_loss *= content_weight / self.extractor.num_content_layers
        loss = style_loss + content_loss
        return loss

    def total_variation_loss(self, image):
        def high_pass_x_y(image):
            x_var = image[:, :, 1:, :] - image[:, :, :-1, :]
            y_var = image[:, 1:, :, :] - image[:, :-1, :, :]
            return x_var, y_var

        x_deltas, y_deltas = high_pass_x_y(image)
        return tf.reduce_mean(x_deltas ** 2) + tf.reduce_mean(y_deltas ** 2)


if __name__ == "__main__":
    content_image_url = "https://raw.githubusercontent.com/ckmarkoh/neuralart_tensorflow/master/images/Taipei101.jpg"
    style_image_url = "https://raw.githubusercontent.com/ckmarkoh/neuralart_tensorflow/master/images/StarryNight.jpg"

    produce_image_file = "produce_images"
    epochs = 10
    steps_per_epoch = 100

    content_path = tf.keras.utils.get_file(fname='content.jpg', origin=content_image_url, cache_dir='.')
    style_path = tf.keras.utils.get_file(fname='style.jpg', origin=style_image_url, cache_dir='.')

    content_image = load_img(content_path)
    style_image = load_img(style_path)

    img_transfer = ImageTransferBaseOnVGG19()
    img_transfer.transfer(content_image, style_image, produce_image_file,
                          epochs, steps_per_epoch)
