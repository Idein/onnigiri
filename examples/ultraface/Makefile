.PHONY: check clean

ultraface.onnx:
	wget -O $@ 'https://github.com/onnx/models/raw/main/vision/body_analysis/ultraface/models/version-RFB-640.onnx'

ultraface-main.onnx: ultraface.onnx
	onnigiri $^ -o $@ --from input --to 314

ultraface-post.onnx: ultraface.onnx
	onnigiri $^ -o $@ --from 314 --to boxes scores

check: ultraface.onnx ultraface-main.onnx ultraface-post.onnx
	python ../check_model.py ultraface $^

clean:
	rm -rf *.onnx
