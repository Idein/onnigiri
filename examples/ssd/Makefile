.PHONY: check clean

ssd-10.onnx:
	wget -O $@ https://github.com/onnx/models/raw/main/archive/vision/object_detection_segmentation/ssd/model/ssd-10.onnx

ssd-10-main.onnx: ssd-10.onnx
	onnigiri ssd-10.onnx -o ssd-10-main.onnx --from image --to Transpose_472 Transpose_661

ssd-10-post.onnx: ssd-10.onnx
	onnigiri $^ -o $@ --from Transpose_472 Transpose_661 --to bboxes labels scores

check: ssd-10.onnx ssd-10-main.onnx ssd-10-post.onnx
	python ../check_model.py ssd $^

clean:
	rm -rf *.onnx
