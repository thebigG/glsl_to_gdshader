#!/usr/bin/env python3
import sys, re, os

def glsl_to_godot(glsl_code, shader_type="canvas_item"):
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



