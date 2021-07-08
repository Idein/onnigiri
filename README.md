# onnigiri
onnx-divider

## Installation

```
$ pip3 install onnigiri
```

## Usage
[SSD](https://github.com/onnx/models/tree/master/vision/object_detection_segmentation/ssd)

```
$ onnigiri ssd-10.onnx -o ssd-10-main.onnx --from image --to Transpose_472 Transpose_661
$ onnigiri ssd-10.onnx -o ssd-10-post.onnx --from Transpose_472 Transpose_661 --to bboxes labels scores
```

[UltraFace](https://github.com/onnx/models/tree/master/vision/body_analysis/ultraface)

```
$ onnigiri version-RFB-640.onnx -o version-RFB-640-main.onnx --from input --to 460 scores
$ onnigiri version-RFB-640.onnx -o version-RFB-640-post.onnx --from 460 --to boxes
```

[tiny-yolov3](https://github.com/onnx/models/tree/master/vision/object_detection_segmentation/tiny-yolov3)

```
$ onnigiri tiny-yolov3-11.onnx --fix-input-shape 'input_1' '1,3,256,256' 'image_shape' '1,2' -o tiny-yolov3-11-main.onnx --from input_1 --to 'TFNodes/yolo_evaluation_layer_1/Reshape_3:0' 'model_1/leaky_re_lu_10/LeakyRelu:0' 'model_1/leaky_re_lu_5/LeakyRelu:0'
$ onnigiri tiny-yolov3-11.onnx --fix-input-shape 'input_1' '1,3,256,256' 'image_shape' '1,2' -o tiny-yolov3-11-post.onnx --from image_shape 'TFNodes/yolo_evaluation_layer_1/Reshape_3:0' 'model_1/leaky_re_lu_10/LeakyRelu:0' 'model_1/leaky_re_lu_5/LeakyRelu:0' --to 'yolonms_layer_1' 'yolonms_layer_1:1' 'yolonms_layer_1:2'
```

## Development Guide

```
$ nix-shell
$ poetry install
```
