import sys

import numpy as np
import onnx
import onnxruntime


def make_sess(path: str) -> onnxruntime.InferenceSession:
    sess_opts = onnxruntime.SessionOptions()
    sess_opts.log_severity_level = 3
    return onnxruntime.InferenceSession(path, sess_options=sess_opts, providers=["CPUExecutionProvider"])


if __name__ == "__main__":
    assert len(sys.argv) == 5
    target_dir = sys.argv[1]
    origin = sys.argv[2]
    pre = sys.argv[3]
    post = sys.argv[4]

    pre_model = onnx.load(pre)
    post_model = onnx.load(post)
    internal_names = [v.name for v in pre_model.graph.output]
    output_names = [v.name for v in post_model.graph.output]

    inputs = dict()
    input_values = list()
    for i in pre_model.graph.input:
        shape = list()
        for d in i.type.tensor_type.shape.dim:
            shape.append(d.dim_value)
        dtype = onnx.helper.tensor_dtype_to_np_dtype(i.type.tensor_type.elem_type)
        if len(shape) != 0:
            v = np.random.randn(*shape).astype(dtype)
            inputs[i.name] = v
            input_values.append(v)

    pre_sess = make_sess(pre)
    internal_values = pre_sess.run(internal_names, inputs)
    vs = dict()
    for k, v in zip(internal_names, internal_values):
        vs[k] = v
    post_sess = make_sess(post)
    outputs = post_sess.run(output_names, vs)

    sess = make_sess(origin)
    expeced = sess.run(output_names, inputs)

    for a, b in zip(expeced, outputs):
        print("check")
        assert np.all(abs(a - b) < 1e-4)

    print("pass")
