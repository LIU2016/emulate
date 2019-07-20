# Future

In fact, we don't need Image-to-Image. We can use [GANs](https://arxiv.org/abs/1406.2661) to generate images directly from random values or generate images from text.

## 1. [Obj-GAN](https://github.com/jamesli1618/Obj-GAN)

The new AI technology Obj-GAN developed by Microsoft Research AI understands natural language descriptions, sketches, composite images, and then refines the details based on individual words provided by sketch frames and text. In other words, the network can generate images of the same scene based on textual descriptions that describe everyday scenes.

微软人工智能研究院（Microsoft Research AI）开发的新 AI 技术Obj-GAN可以理解自然语言描述、绘制草图、合成图像，然后根据草图框架和文字提供的个别单词细化细节。换句话说，这个网络可以根据描述日常场景的文字描述生成同样场景的图像。

**效果**

![](https://raw.githubusercontent.com/jamesli1618/Obj-GAN/master/step_vis.png)

**模型**

![](https://raw.githubusercontent.com/jamesli1618/Obj-GAN/master/framework.png)


## 2. [StoryGAN](https://github.com/yitong91/StoryGAN)

[Advanced version of the pen: just one sentence, one story, you can generate a picture](https://www.microsoft.com/en-us/research/blog/a-picture-from-a-dozen-words-a-drawing-bot-for-realizing-everyday-scenes-and-even-stories/).
> Microsoft's new research proposes a new GAN, ObjGAN, which can generate complex scenes based on textual descriptions. They also proposed another GAN, StoryGAN, which can draw a story. Enter the text of a story and output the "picture book".

[进阶版神笔：只需一句话、一个故事，即可生成画面](https://www.jiqizhixin.com/articles/2019-06-29)
> 微软新研究提出新型 GAN——ObjGAN，可根据文字描述生成复杂场景。他们还提出另一个可以画故事的 GAN——StoryGAN，输入一个故事的文本，即可输出「连环画」。

当前最优的文本到图像生成模型可以基于单句描述生成逼真的鸟类图像。然而，文本到图像生成器远远不止仅对一个句子生成单个图像。给定一个多句段落，生成一系列图像，每个图像对应一个句子，完整地可视化整个故事。

**效果**

![](https://www.microsoft.com/en-us/research/uploads/prod/2019/06/drawing-bot-figure-3.png)

---

The most commonly used image-to-image technology should be Beauty App, so why don't we develop a smarter Beauty Camera?

现在用得最多的Image-to-Image技术应该就是美颜APP了，所以我们为什么不开发一个更加智能的美颜相机呢？
