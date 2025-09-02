#!/usr/bin/env python3

import shutil
import os
import sys
from PIL import Image
import imagehash


def calculate_similarity(hash1, hash2):
    hamming_distance = hash1 - hash2

    max_distance = 64
    similarity = (1 - hamming_distance / max_distance) * 100

    return similarity


def dhash(filepath):
    try:
        with Image.open(filepath) as img:
            if img.mode != "RGB":
                img = img.convert("RGB")

            return imagehash.dhash(img)
    except Exception as e:
        print(f"Error processing {filepath}: {e}", file=sys.stderr)
        return None


def main():
    REFERENCE_IMAGE = "peukku.png"
    SIMILARITY_THRESHOLD = 78.8

    emojis_dir = "emojis"
    images_dir = "peukkus"

    if not os.path.exists(emojis_dir):
        print(f"Error: '{emojis_dir}' not found")
        sys.exit(1)

    if not os.path.exists(REFERENCE_IMAGE):
        print(f"Error: missing '{REFERENCE_IMAGE}'")
        sys.exit(1)

    if not os.path.exists(images_dir):
        os.mkdir(images_dir)

    reference_hash = dhash(REFERENCE_IMAGE)
    if reference_hash is None:
        print("Failed to process reference image!")
        sys.exit(1)

    print(f"Reference hash: {reference_hash}")

    similar_emojis = []

    for filename in sorted(os.listdir(emojis_dir)):
        if filename.lower().endswith(".png"):
            filepath = os.path.join(emojis_dir, filename)

            file_hash = dhash(filepath)

            if file_hash is not None:
                similarity = calculate_similarity(reference_hash, file_hash)

                print(f"{filename}: {similarity:.1f}%")

                if similarity >= SIMILARITY_THRESHOLD:
                    shortcode = os.path.splitext(filename)[0]
                    shutil.copyfile(filepath, f"{images_dir}/{shortcode}.png")
                    similar_emojis.append((shortcode, similarity))

    similar_emojis.sort(key=lambda x: x[1], reverse=True)

    html_content = """<!DOCTYPE html>
<html lang=fi>
<head>
    <title>Only Peukkus. Nothing else.</title>
    <style>body, code { font-family: Tahoma, Verdana; }</style>
    <link rel="icon" type="image/x-icon" href="favicon.ico">
    <link rel="shortcut icon" href="favicon.ico">
    <link rel="icon" type="image/png" href="op-logo.png">
    <meta charset="UTF-8">
</head>
<body>
    <img height=44 src=op-logo.png alt="Only Peukkus">
    <p>listing only thumb up emojis. <a href=https://github.com/jrasanen/onlypeukkus>repo</a>.</p>
    <ul>
"""

    for shortcode, similarity in similar_emojis:
        html_content += f"        <li><img alt={shortcode} height=44 width=44 src=peukkus/{shortcode}.png><code>:{shortcode}:</code></li>\n"

    html_content += """    </ul>
</body>
</html>"""

    with open("index.html", "w") as f:
        f.write(html_content)

    print(
        f"Generated index.html with {len(similar_emojis)} emojis with ≥{SIMILARITY_THRESHOLD}% similarity",
        file=sys.stderr,
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
