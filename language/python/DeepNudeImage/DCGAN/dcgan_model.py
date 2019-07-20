import tensorflow as tf
import matplotlib.pyplot as plt


class Generator(tf.keras.Model):

    def __init__(self):
        super(Generator, self).__init__()
        self.fc_a = tf.keras.layers.Dense(53 * 43 * 128, use_bias=False)
        self.Conv2DT_a = tf.keras.layers.Conv2DTranspose(128, (5, 5), strides=(1, 1), padding='same', use_bias=False)
        self.Conv2DT_b = tf.keras.layers.Conv2DTranspose(64, (5, 5), strides=(2, 2), padding='valid', use_bias=False)
        self.Conv2DT_c = tf.keras.layers.Conv2DTranspose(3, (5, 5), strides=(2, 2),
                                                         padding='same', use_bias=False, activation='tanh')

        self.BN_a = tf.keras.layers.BatchNormalization()
        self.BN_b = tf.keras.layers.BatchNormalization()
        self.BN_c = tf.keras.layers.BatchNormalization()
        self.LeckyReLU_a = tf.keras.layers.LeakyReLU()
        self.LeckyReLU_b = tf.keras.layers.LeakyReLU()
        self.LeckyReLU_c = tf.keras.layers.LeakyReLU()

    def call(self, random_noise, training=False):
        # random_noise (batch_size, 53 * 43 * 256)
        # x (batch_size, 53 * 43 * 128)
        x = self.fc_a(random_noise)
        x = self.BN_a(x, training=training)
        x = self.LeckyReLU_a(x)

        # (batch_size, 53, 43, 128)
        x = tf.keras.layers.Reshape((53, 43, 128))(x)

        # (batch_size, 53, 43, 128)
        x = self.Conv2DT_a(x)
        x = self.BN_b(x, training=training)
        x = self.LeckyReLU_b(x)

        # (batch_size, 109, 89, 64)
        x = self.Conv2DT_b(x)
        x = self.BN_c(x, training=training)
        x = self.LeckyReLU_c(x)

        # (batch_size, 218, 178, 3)
        generated_image = self.Conv2DT_c(x)

        return generated_image


class Discriminator(tf.keras.Model):

    def __init__(self):
        super(Discriminator, self).__init__()
        self.Conv2D_a = tf.keras.layers.Conv2D(64, (5, 5), strides=(2, 2), padding='same')
        self.Conv2D_b = tf.keras.layers.Conv2D(128, (5, 5), strides=(2, 2), padding='same')
        self.LeckyReLU_a = tf.keras.layers.LeakyReLU()
        self.LeckyReLU_b = tf.keras.layers.LeakyReLU()
        self.Dropout_a = tf.keras.layers.Dropout(0.3)
        self.Dropout_b = tf.keras.layers.Dropout(0.3)
        self.Flatten = tf.keras.layers.Flatten()
        self.dense = tf.keras.layers.Dense(1)

    def call(self, image, training=False):
        # image (batch_size, 218, 178, 3)
        x = self.Conv2D_a(image)
        x = self.LeckyReLU_a(x)
        x = self.Dropout_a(x, training=training)

        x = self.Conv2D_b(x)
        x = self.LeckyReLU_b(x)
        x = self.Dropout_b(x, training=training)

        x = self.Flatten(x)
        x = self.dense(x)
        return x

# This method returns a helper function to compute cross entropy loss
cross_entropy = tf.keras.losses.BinaryCrossentropy(from_logits=True)

def discriminator_loss(real_output, fake_output):
    real_loss = cross_entropy(tf.ones_like(real_output), real_output)
    fake_loss = cross_entropy(tf.zeros_like(fake_output), fake_output)
    total_loss = real_loss + fake_loss
    return total_loss


def generator_loss(fake_output):
    return cross_entropy(tf.ones_like(fake_output), fake_output)

def max_min_normal_matrix(image_matrix):
    image_matrix_min = image_matrix.min()
    image_matrix_max = image_matrix.max()
    image_matrix_normal = (image_matrix - image_matrix_min) / (image_matrix_max - image_matrix_min)
    return image_matrix_normal

if __name__ == "__main__":
    generator = Generator()
    noise = tf.random.normal([16, 100])
    print(f"Inputs noise.shape {noise.shape}")
    generated_image = generator(noise, training=False)
    #generator.summary()
    print(f"Pass by ------------ ----generator----------------------")
    print(f"Outputs generated_image.shape {generated_image.shape}")
    plt.imshow(generated_image[0, :, :, 0], cmap='gray')
    plt.show()
    plt.savefig("generated_image_test.png")
    discriminator = Discriminator()
    print(f"Pass by ------------ ----discriminator----------------------")
    decision = discriminator(generated_image, training=False)
    print(f"Outputs decision.shape {decision.shape}")
    #discriminator.summary()
    print(f"Outputs decision \n{decision}")

    predictions = generated_image

    fig = plt.figure(figsize=(4, 4))

    for i in range(predictions.shape[0]):
        plt.subplot(4, 4, i + 1)
        plt.imshow(max_min_normal_matrix(predictions[i].numpy()))
        plt.axis('off')
    save_image_path = 'image_at_epoch_{:04d}.png'.format(1)
    plt.savefig(save_image_path)

