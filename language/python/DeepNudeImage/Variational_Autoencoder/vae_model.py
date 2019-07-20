import tensorflow as tf

class CVAE(tf.keras.Model):
    def __init__(self, latent_dim):
        super(CVAE, self).__init__()
        self.latent_dim = latent_dim
        self.inference_net = tf.keras.Sequential(
            [
                tf.keras.layers.InputLayer(input_shape=(218, 178, 3)),
                tf.keras.layers.Conv2D(
                    filters=32, kernel_size=3, strides=(2, 2), activation='relu'),
                tf.keras.layers.Conv2D(
                    filters=64, kernel_size=3, strides=(2, 2), activation='relu'),
                tf.keras.layers.Flatten(),
                # No activation
                tf.keras.layers.Dense(latent_dim + latent_dim),
            ]
        )

        self.generative_net = tf.keras.Sequential(
            [
                tf.keras.layers.InputLayer(input_shape=(latent_dim,)),
                tf.keras.layers.Dense(units=54 * 44 * 32, activation=tf.nn.relu),
                tf.keras.layers.Reshape(target_shape=(54, 44, 32)),
                tf.keras.layers.Conv2DTranspose(
                    filters=64,
                    kernel_size=3,
                    strides=(2, 2),
                    activation='relu'),
                tf.keras.layers.Conv2DTranspose(
                    filters=32,
                    kernel_size=3,
                    strides=(2, 2),
                    padding="SAME",
                    activation='relu'),
                # No activation
                tf.keras.layers.Conv2DTranspose(
                    filters=3, kernel_size=3, strides=(1, 1), padding="SAME"),
            ]
        )

    def sample(self, eps=None):
        if eps is None:
            eps = tf.random.normal(shape=(100, self.latent_dim))
        return self.decode(eps, apply_sigmoid=True)

    def encode(self, x):
        mean, logvar = tf.split(self.inference_net(x), num_or_size_splits=2, axis=1)
        return mean, logvar

    def reparameterize(self, mean, logvar):
        eps = tf.random.normal(shape=mean.shape)
        return eps * tf.exp(logvar * .5) + mean

    def decode(self, z, apply_sigmoid=False):
        logits = self.generative_net(z)
        if apply_sigmoid:
            probs = tf.sigmoid(logits)
            return probs

        return logits


if __name__ == "__main__":
    BATCH_SIZE = 10
    IMG_HEIGHT = 218
    IMG_WIDTH = 178
    INPUT_CHANNELS = 3
    latent_dim = 100

    vae = CVAE(latent_dim)

    input_x = tf.random.normal([BATCH_SIZE, IMG_HEIGHT, IMG_WIDTH, INPUT_CHANNELS])
    print(f"Inputs input_x.shape {input_x.shape}")

    print("Pass by vae.encode".center(100, "-"))
    mean, logvar = vae.encode(input_x)
    print(f"Output mean.shape {mean.shape}, logvar.shape {logvar.shape}")

    print("Pass by vae.reparameterize".center(100, "-"))
    z = vae.reparameterize(mean, logvar)
    print(f"Output z.shape {z.shape}")

    print("Pass by vae.reparameterize".center(100, "-"))
    x_logit = vae.decode(z)
    print(f"Output x_logit.shape {x_logit.shape}")
