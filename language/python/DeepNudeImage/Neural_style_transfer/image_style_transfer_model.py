import tensorflow as tf

class StyleContentModel(tf.keras.models.Model):
    def __init__(self, style_layers=None, content_layers=None, show_all_optional_layer_name=False):
        super(StyleContentModel, self).__init__()

        if style_layers is None:
            # Style layer of interest
            style_layers = ['block1_conv1',
                            'block2_conv1',
                            'block3_conv1',
                            'block4_conv1',
                            'block5_conv1']
        if content_layers is None:
            # Content layer where will pull our feature maps
            content_layers = ['block5_conv2']

        self.vgg = self.vgg_layers(style_layers + content_layers, show_all_optional_layer_name)
        self.style_layers = style_layers
        self.content_layers = content_layers
        self.num_style_layers = len(style_layers)
        self.num_content_layers = len(content_layers)
        self.vgg.trainable = False


    def vgg_layers(self, layer_names, show_all_optional_layer_name):
        """ Creates a vgg model that returns a list of intermediate output values."""
        # Load our model. Load pretrained VGG, trained on imagenet data
        vgg = tf.keras.applications.VGG19(include_top=False, weights='imagenet')
        vgg.trainable = False
        if show_all_optional_layer_name:
            for layer in self.vgg.layers:
                print(layer.name)

        outputs = [vgg.get_layer(name).output for name in layer_names]

        model = tf.keras.Model([vgg.input], outputs)
        return model

    def gram_matrix(self, input_tensor):
        result = tf.linalg.einsum('bijc,bijd->bcd', input_tensor, input_tensor)
        input_shape = tf.shape(input_tensor)
        num_locations = tf.cast(input_shape[1] * input_shape[2], tf.float32)
        return result / (num_locations)

    def call(self, inputs):
        "Expects float input in [0,1]"
        inputs = inputs * 255.0
        preprocessed_input = tf.keras.applications.vgg19.preprocess_input(inputs)
        outputs = self.vgg(preprocessed_input)
        style_outputs, content_outputs = (outputs[:self.num_style_layers],
                                          outputs[self.num_style_layers:])

        style_outputs = [self.gram_matrix(style_output)
                         for style_output in style_outputs]

        content_dict = {content_name: value
                        for content_name, value
                        in zip(self.content_layers, content_outputs)}

        style_dict = {style_name: value
                      for style_name, value
                      in zip(self.style_layers, style_outputs)}

        return {'content': content_dict, 'style': style_dict}



if __name__=="__main__":
    extractor = StyleContentModel()
    import numpy as np
    fack_image = tf.constant(np.random.random(size=(1, 244, 244, 3)), dtype=tf.float32)
    #fack_image = tf.keras.applications.vgg19.preprocess_input(fack_image)
    results = extractor(tf.constant(fack_image))

    style_results = results['style']

    print('Styles:')
    for name, output in sorted(results['style'].items()):
        print("  ", name)
        print("    shape: ", output.numpy().shape)
        # print("    min: ", output.numpy().min())
        # print("    max: ", output.numpy().max())
        # print("    mean: ", output.numpy().mean())
        print()

    print("Contents:")
    for name, output in sorted(results['content'].items()):
        print("  ", name)
        print("    shape: ", output.numpy().shape)
        # print("    min: ", output.numpy().min())
        # print("    max: ", output.numpy().max())
        # print("    mean: ", output.numpy().mean())
