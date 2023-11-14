# onnigiri
onnx-divider

The purpose of this package is to create subgraphs by partitioning computational graphs in order to facilitate the development of applications.

One of the problems in developing applications using deep learning models is that the DL model is not applicable by itself.
For example, they may be have unnecessary nodes and some nodes are not supported some DL tools.
This tool enable us to edit an onnx model freely and easily.

## Installation
From [PyPI](https://pypi.org/project/onnigiri/):

```
$ pip3 install onnigiri
```

From [Dockerhub](https://hub.docker.com/repository/docker/idein/onnigiri)

```
$ docker pull idein/onnigiri:20231114
```


## Usage
[SSD](https://github.com/onnx/models/tree/main/vision/object_detection_segmentation/ssd)

```
$ onnigiri ssd-10.onnx -o ssd-10-main.onnx --from image --to Transpose_472 Transpose_661
$ onnigiri ssd-10.onnx -o ssd-10-post.onnx --from Transpose_472 Transpose_661 --to bboxes labels scores
```

With docker:

```
$ docker run --rm -it -u $UID:$GID -v $(pwd):/work idein/onnigiri:20221014 ssd-10.onnx -o ssd-10-main.onnx --from image --to Transpose_472 Transpose_661
$ docker run --rm -it -u $UID:$GID -v $(pwd):/work idein/onnigiri:20221014 ssd-10.onnx -o ssd-10-post.onnx  --from Transpose_472 Transpose_661 --to bboxes labels scores
```

[UltraFace](https://github.com/onnx/models/tree/main/vision/body_analysis/ultraface)

```
$ onnigiri version-RFB-640.onnx -o version-RFB-640-main.onnx --from input --to 460 scores
$ onnigiri version-RFB-640.onnx -o version-RFB-640-post.onnx --from 460 --to boxes
```

[tiny-yolov3](https://github.com/onnx/models/tree/main/vision/object_detection_segmentation/tiny-yolov3)

```
$ onnigiri tiny-yolov3-11.onnx --fix-input-shape 'input_1' '1,3,256,256' 'image_shape' '1,2' -o tiny-yolov3-11-main.onnx --from input_1 --to 'TFNodes/yolo_evaluation_layer_1/Reshape_3:0' 'model_1/leaky_re_lu_10/LeakyRelu:0' 'model_1/leaky_re_lu_5/LeakyRelu:0'
$ onnigiri tiny-yolov3-11.onnx --fix-input-shape 'input_1' '1,3,256,256' 'image_shape' '1,2' -o tiny-yolov3-11-post.onnx --from image_shape 'TFNodes/yolo_evaluation_layer_1/Reshape_3:0' 'model_1/leaky_re_lu_10/LeakyRelu:0' 'model_1/leaky_re_lu_5/LeakyRelu:0' --to 'yolonms_layer_1' 'yolonms_layer_1:1' 'yolonms_layer_1:2'
```

## Q&A

- How to get the name of values?

Use [Netron](https://netron.app).

- Why is the extracted subgraph different from the original subgraph?

onnigiri apply [onnx-simplifier](https://github.com/daquexian/onnx-simplifier) before extraction. You can disable the graph optimization by the onnx-simplifier using the `--no-optimization` option.

## Development Guide

```
$ poetry install
```

### Build docker image

```
$ nix build '.#dockerimage' -o image
$ docker load < ./image
```

## Related project

- [onnion](https://github.com/Idein/onnion)
