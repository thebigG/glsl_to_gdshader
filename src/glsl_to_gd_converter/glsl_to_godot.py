import re, sys, os

def convert_glsl_to_godot(glsl_code, shader_type="canvas_item"):
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

    # Add shader_type header
    header = f"shader_type {shader_type};\n\n"
    return header + code.strip() + "\n"


def main():
    if len(sys.argv) < 2:
        print("Usage: glsl_to_godot.py <input.glsl> [shader_type]")
        print("shader_type: canvas_item | spatial | sky | particles")
        sys.exit(1)

    infile = sys.argv[1]
    shader_type = sys.argv[2] if len(sys.argv) > 2 else "canvas_item"

    with open(infile, "r") as f:
        glsl_code = f.read()

    godot_code = convert_glsl_to_godot(glsl_code, shader_type)

    outfile = os.path.splitext(infile)[0] + ".gdshader"
    with open(outfile, "w") as f:
        f.write(godot_code)

    print(f"✅ Converted {infile} → {outfile} (type={shader_type})")

if __name__ == "__main__":
    main()



