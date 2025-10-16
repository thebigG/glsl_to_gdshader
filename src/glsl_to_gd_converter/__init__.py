import sys, os

from src.glsl_to_gd_converter.glsl_to_godot import glsl_to_godot

def main():
    if len(sys.argv) < 2:
        print("Usage: glsl_to_godot.py <input.glsl> [shader_type]")
        print("shader_type: canvas_item | spatial | sky | particles")
        sys.exit(1)

    infile = sys.argv[1]
    shader_type = sys.argv[2] if len(sys.argv) > 2 else "canvas_item"

    with open(infile, "r") as f:
        glsl_code = f.read()

    godot_code = glsl_to_godot(glsl_code, shader_type)

    outfile = os.path.splitext(infile)[0] + ".gdshader"
    with open(outfile, "w") as f:
        f.write(godot_code)

    print(f"✅ Converted {infile} → {outfile} (type={shader_type})")

if __name__ == "__main__":
    main()