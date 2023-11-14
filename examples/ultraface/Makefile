.PHONY: check check-no-opt clean

ultraface.onnx:
	wget -O $@ 'https://github.com/onnx/models/raw/main/vision/body_analysis/ultraface/models/version-RFB-640.onnx'

ultraface-main.onnx: ultraface.onnx
	onnigiri $^ -o $@ --from input --to 314

ultraface-post.onnx: ultraface.onnx
	onnigiri $^ -o $@ --from 314 --to boxes scores

ultraface-main-no-opt.onnx: ultraface.onnx
	onnigiri $^ -o $@ --from input --to 314 --no-optimization

ultraface-post-no-opt.onnx: ultraface.onnx
	onnigiri $^ -o $@ --from 314 --to boxes scores --no-optimization

check: ultraface.onnx ultraface-main.onnx ultraface-post.onnx
	python ../check_model.py ultraface $^

check-no-opt: ultraface.onnx ultraface-main-no-opt.onnx ultraface-post-no-opt.onnx
	python ../check_model.py ultraface $^

clean:
	rm -rf *.onnx
