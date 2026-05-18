#!/usr/bin/env python3
"""通过 Codex CLI (ChatGPT Plus) 免费生图，支持参考图修改。"""
import os, sys, shutil, subprocess
from datetime import datetime

CODEX_BIN = "/Applications/Codex.app/Contents/Resources/codex"
GEN_DIR = os.path.expanduser("~/.codex/generated_images")


def list_images():
    imgs = []
    if os.path.isdir(GEN_DIR):
        for root, _, files in os.walk(GEN_DIR):
            for f in files:
                if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp", ".gif")):
                    fp = os.path.join(root, f)
                    imgs.append((fp, os.path.getmtime(fp)))
    return imgs


def generate(prompt, size="1024x1024", output_dir=None, image=None):
    if image:
        full_prompt = f"我有一张现有图片在 {image}，请参考它的设计风格和布局，但根据以下正确产品信息修正内容后重新生成一张：{prompt}"
    else:
        full_prompt = f"生成一张信息图: {prompt}。图片尺寸 {size}。"

    print(f"生成中: {prompt[:80]}...", file=sys.stderr)

    before = {fp for fp, _ in list_images()}

    cmd = [CODEX_BIN, "exec", full_prompt, "--skip-git-repo-check"]

    result = subprocess.run(
        cmd, capture_output=True, text=True, timeout=900,
        env={**os.environ, "HOME": os.environ.get("HOME", os.path.expanduser("~"))},
    )

    if result.returncode != 0:
        raise Exception(f"codex 失败 (exit={result.returncode})")

    after = list_images()
    new_imgs = [(fp, mt) for fp, mt in after if fp not in before]
    if not new_imgs:
        raise Exception("未找到新图片")

    new_imgs.sort(key=lambda x: x[1], reverse=True)
    image_path = new_imgs[0][0]

    output_dir = output_dir or os.getcwd()
    ext = os.path.splitext(image_path)[1] or ".png"
    filename = f"codex-image-{datetime.now().strftime('%Y%m%d-%H%M%S')}{ext}"
    dest = os.path.join(output_dir, filename)
    shutil.copy2(image_path, dest)
    return dest


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate.py '<prompt>' [size] [output_dir] [--image <path>]")
        sys.exit(1)

    prompt = sys.argv[1]
    size = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith("--") else "1024x1024"
    output_dir = sys.argv[3] if len(sys.argv) > 3 and not sys.argv[3].startswith("--") else os.getcwd()
    image = None
    if "--image" in sys.argv:
        idx = sys.argv.index("--image")
        if idx + 1 < len(sys.argv):
            image = sys.argv[idx + 1]

    try:
        path = generate(prompt, size, output_dir, image)
        print(f"SUCCESS:{path}")
    except Exception as e:
        print(f"ERROR:{e}")
        sys.exit(1)
