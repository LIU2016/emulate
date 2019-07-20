# Cycle-Consistent Adversarial Networks (CycleGAN)
> If you have interesting ideas or data, please contact me quickly at wangzichaochaochao@gmail.com .

![](https://github.com/yuanxiaosc/DeepNude-an-Image-to-Image-technology/raw/master/paper_images/2017_Zhu_CycleGAN_examples_horse2zebra.gif)
**horse2zebra 马变斑马**

CycleGAN uses a cyclic consistency loss function to facilitate model training without pairing data. For example, you only need to prepare thousands of photos of the source dataset and thousands of photos of the target dataset, and then CycleGAN (through the training model) can learn the relationship between the source image set apple and the target image set orange. Entering the apple after the training CycleGAN can generate oranges, and vice versa. The main advantage of CycleGAN is that it can learn the relationship between the source image set and the target image set without one-to-one mapping between the source image set apple and the target image set orange.

Here, the CycleGAN neural network model is used to realize the four functions of photo style conversion, photo effect enhancement, landscape season change, and object conversion.

CycleGAN使用循环一致性损失函数来促使模型训练，而无需配对数据。比如，只需要准备源数据集几千张苹果的照片和目标数据集几千张橘子的照片，然后CycleGAN（通过训练模型）就可以学习源图片集苹果和目标图片集橘子的之间的关系。给训练后的CycleGAN输入苹果就可以生成橘子，反之亦然。CycleGAN的主要优点是可以不需要在源图片集苹果和目标图片集橘子之间进行一对一对应，就能学习源图片集和目标图片集的关系。

这儿，使用CycleGAN神经网络模型实现照片风格转换、照片效果增强、照片中风景季节变换、物体转换四大功能。

---

## 代码用法 Code usage

You can use your own data or directly use the data of a predefined task.

你可以使用自己的数据或者直接使用预定义任务的数据。

```
predefined_cyclegan_task_name_list = [
"apple2orange", "summer2winter_yosemite", "horse2zebra", "monet2photo",
"cezanne2photo", "ukiyoe2photo", "vangogh2photo", "maps", "cityscapes",
"facades", "iphone2dslr_flower"]
```

### Require

+ python 3+, e.g. python==3.6
+ tensorflow version 2, e.g. tensorflow==2.0.0-beta1
+ tensorflow-datasets

### Train Model

```python
python train_image2text_model.py data_dir_or_predefined_task_name
```

### Model Inference

```python
python inference_by_image2text_model.py data_dir_or_predefined_task_name
```

---

## 预定义任务名称 Task Name

You can use the following data_dir_or_predefined_task_name parameters directly, or you can define new tasks yourself.

可以直接选用以下 data_dir_or_predefined_task_name 参数，也可以自行定义新的任务。

```
python train_image2text_model.py apple2orange
```


### 1. 照片风格转换   Style Transfer

|任务名称|task_name|
|-|-|
|莫奈风格2照片|  monet2photo|
|梵高风格2照片|  vangogh2photo|
|塞尚风格2照片|  cezanne2photo|
|浮世绘风格2照片|  ukiyoe2photo|

![](https://junyanz.github.io/CycleGAN/images/photo2painting.jpg)


### 2. 照片效果增强：虚化背景  Photo Enhancement: Narrow depth of field

|任务名称|task_name|
|-|-|
|智能手机效果2单反相机| iphone2dslr_flower|

![](https://junyanz.github.io/CycleGAN/images/photo_enhancement.jpg)


### 3. 照片风景季节变换 Season Transfer

|任务名称|task_name|
|-|-|
|夏天2冬天| summer2winter_yosemite|

![](https://junyanz.github.io/CycleGAN/images/season.jpg)


### 4. 物体转换 Object Transfiguration

|任务名称|task_name|
|-|-|
|马2斑马| horse2zebra|
|苹果2橘子| apple2orange|

![](https://junyanz.github.io/CycleGAN/images/objects.jpg)

### 5. 其它 other

|任务名称|task_name|
|-|-|
|类标2街景图| cityscapes|
|类标2建筑物立面图| facades|
|地图2航拍图| maps|



## 使用自己的数据 Use your own data

Give an example 举例：

[apple2orange_example](apple2orange_example)

```
apple2orange
│
│  
├─testA
│      nfew3261_apple.jpg
│      n073f461_apple.jpg
│      rrrrg461_apple.jpg
│      
├─testB
│      rtrt912_orange.jpg
│      n0gferf_orange.jpg
│      trgerw3_orange.jpg
│      
├─trainA
│      5gr40461_apple.jpg
│      tfdvd441_apple.jpg
│      nfew4046_apple.jpg
│      
└─trainB
       yy49192_orange.jpg
       hgfhfp7_orange.jpg
       osfs323_orange.jpg
```



If the data folder path(apple2orange_example) is /home/b418a/.keras/datasets/apple2orange


```
python train_image2text_model.py /home/b418a/.keras/datasets/apple2orange
```

> See the load_cyclegan_image_dataset_from_data_folder function in dataset_utils.py for details.

```
def load_cyclegan_image_dataset_from_data_folder(data_dir):
    """There is a need for a data folder, the data file contains four subfolders
     trainA, trainB, testA, testB. The four subfolders respectively store the
     source image set used for training, the target image set used for training,
     the source image set used for the test, and the target image set used for the test."""
```
