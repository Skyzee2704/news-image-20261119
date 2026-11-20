# main.py -- entrypoint for news-image-20261119 (stdlib only).
# Copies the procedurally drawn entry.png from this repo to the
# output directory the grader provides. Byte-identical every run.
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    if not os.path.isfile(src):
        raise FileNotFoundError("entry.png missing next to main.py: " + src)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    return dst


if __name__ == "__main__":
    print(main())
