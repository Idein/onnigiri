import argparse
import sys
import tempfile
from typing import Dict, List

import onnx
from onnxsim import simplify


def has_fixed_shape(shape: onnx.TensorShapeProto) -> bool:
    return all([s.HasField("dim_value") for s in shape.dim])


def check_inputs(inputs: List[onnx.ValueInfoProto]) -> None:
    invalid_inputs = []

    for i in inputs:
        if not has_fixed_shape(i.type.tensor_type.shape):
            invalid_inputs.append(i)

    if len(invalid_inputs) != 0:
        names = " ".join([i.name for i in invalid_inputs])
        print(f"Error: Fix the shape of the inputs by --fix-input-shape option: {names}", file=sys.stderr)
        sys.exit(1)


def fix_input_shapes(shapes: Dict[str, List[int]], model: onnx.ModelProto) -> None:
    for i in model.graph.input:
        if i.name in shapes:
            i.type.tensor_type.shape.ClearField("dim")
            for d in shapes[i.name]:
                dim = i.type.tensor_type.shape.dim.add()
                dim.dim_value = d


def collect_unknown_value(graph: onnx.GraphProto) -> List[str]:
    value_names = [i.name for i in graph.input]
    unknown_names = []
    value_names = value_names + [i.name for i in graph.initializer]
    for n in graph.node:
        for i in n.input:
            if i not in value_names:
                unknown_names.append(i)
        value_names = value_names + list(n.output)
    return unknown_names


def lookup_initializer(name: str, initializer: List[onnx.TensorProto]) -> onnx.TensorProto:
    for i in initializer:
        if i.name == name:
            return i

    raise Exception(f"Error: not found {name}")


def fix_subgraph(graph: onnx.GraphProto, initializer: List[onnx.TensorProto]) -> None:
    unknown_names = collect_unknown_value(graph)
    for name in unknown_names:
        v = lookup_initializer(name, initializer)
        graph.initializer.insert(0, v)


def fix_subgraphs(graph: onnx.GraphProto) -> None:
    for n in graph.node:
        sub_graphs = [attr.g for attr in n.attribute if attr.HasField("g")]
        if len(sub_graphs) != 0:
            for g in sub_graphs:
                fix_subgraph(g, graph.initializer)


def onnigiri(
    input_path: str, output_path: str, input_names: List[str], output_names: List[str], shapes: Dict[str, List[int]]
) -> None:
    model = onnx.load(input_path)
    if len(shapes) != 0:
        fix_input_shapes(shapes, model)
    check_inputs(model.graph.input)

    simplified_model, check = simplify(model)
    assert check, "Error: Simplified ONNX model could not be validated"

    fix_subgraphs(simplified_model.graph)

    with tempfile.NamedTemporaryFile() as tmp:
        onnx.save(simplified_model, tmp.name)
        onnx.utils.extract_model(tmp.name, output_path, input_names, output_names)


def parse_shapes(args: List[str]) -> Dict[str, List[int]]:
    shapes = dict()
    if len(args) % 2 != 0:
        sys.exit("Error: the number of argumets of --fix-input-shape must be even.")
    for idx in range(len(args) // 2):
        shapes[args[2 * idx]] = [int(x) for x in args[2 * idx + 1].split(",")]
    return shapes


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", help="Input ONNX path")
    parser.add_argument("-o", "--output", dest="output_path", required=True, help="Output ONNX path")
    parser.add_argument("--from", nargs="+", dest="input_names", help="Names of input value")
    parser.add_argument("--to", nargs="+", dest="output_names", help="Names of output value")
    parser.add_argument("--fix-input-shape", nargs="+", dest="shapes", default=[], help="Pairs of the name and shape of inputs")
    args = parser.parse_args()
    onnigiri(args.input_path, args.output_path, args.input_names, args.output_names, parse_shapes(args.shapes))


if __name__ == "__main__":
    main()
