import re, sys, os
import argparse


def parse_args():
    parser = argparse.ArgumentParser(
        description="Convert GLSL shaders to Godot shader format."
    )
    parser.add_argument(
        "input",
        metavar="input.glsl",
        help="Path to the input GLSL shader file."
    )
    parser.add_argument(
        "shader_type",
        nargs="?",
        default=None,
        choices=["canvas_item", "spatial", "sky", "particles"],
        help="Type of Godot shader to generate (default: canvas_item)."
    )

    args = parser.parse_args()
    return args



def convert_glsl_to_godot(glsl_code, shader_type):
    # Remove GLSL version line
    code = re.sub(r"#version\s+\d+\s*\n", "", glsl_code)

    # Replace GLSL builtins
    replacements = {
        r"\bgl_FragColor\b": "COLOR",
        r"\bgl_Position\b": "POSITION",
        r"\btexture2D\b": "texture",
        r"\btextureCube\b": "texture",
        r"\bvec4\s*\(": "vec4(",
    }

    for pattern, repl in replacements.items():
        code = re.sub(pattern, repl, code)

    # Replace 'uniform' declarations (leave as-is but ensure formatting)
    code = re.sub(r"\buniform\s+sampler2D\b", "uniform sampler2D", code)

    # Remove precision qualifiers (not needed in Godot)
    code = re.sub(r"precision\s+\w+\s+\w+;", "", code)

    # Remove 'in' and 'out' qualifiers (Godot uses 'varying')
    code = re.sub(r"\b(in|out)\b\s+(\w+)\s+", r"varying \2 ", code)

    # Add shader_type header if specified
    if shader_type is None:
        return code.strip() + "\n"
    else:
        header = f"shader_type {shader_type};\n\n"
        return header + code.strip() + "\n"


def main():

    args = parse_args()

    infile = args.input
    shader_type = args.shader_type

    with open(infile, "r") as f:
        glsl_code = f.read()

    godot_code = convert_glsl_to_godot(glsl_code, shader_type)

    # If no shader type specified, save as .gdshaderinc
    # As per Godot conventions for includes without shader_type (https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/shader_preprocessor.html#include)
    if shader_type is None:
        outfile = os.path.splitext(infile)[0] + ".gdshaderinc"
    else:
        outfile = os.path.splitext(infile)[0] + f"_{shader_type}.gdshader"

    with open(outfile, "w") as f:
        f.write(godot_code)

    print(f"✅ Converted {infile} → {outfile} (type={shader_type})")

if __name__ == "__main__":
    main()



