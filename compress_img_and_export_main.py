import os
import sys
import pathlib
import zipfile
from fnmatch import fnmatch
from PIL import Image, ImageDraw, ImageFont
from tqdm import tqdm


def zip_directory(folder_path, zip_path):
    with zipfile.ZipFile(zip_path, mode='w') as zipf:
        len_dir_path = len(folder_path)
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, file_path[len_dir_path:])


# Input arguments
if len(sys.argv) < 2:
    print("Usage: python compress_images.py <root_directory>")
    sys.exit(1)

root = sys.argv[1]
image_quality = 30  # Retained image quality, in %

# Main export path
target_path = r'C:\Image Compression Exports'
os.makedirs(target_path, exist_ok=True)
print(f'Root path: {root}\nTarget path: {target_path}')

# Create folder for this specific job
root_subdir = pathlib.PurePath(root).name
target_path = os.path.join(target_path, root_subdir + '_comp')
os.makedirs(target_path, exist_ok=True)

# File patterns to match
patterns = ['*.tif', '*.bmp', '*.jpg', '*.png']

# Count total number of images
file_list = []
for pattern in patterns:
    for path, _, files in os.walk(root):
        for file in files:
            if fnmatch(file, pattern):
                file_list.append(os.path.join(path, file))

n = len(file_list)
if n == 0:
    print("No matching image files found.")
    sys.exit(0)

# Start compression with progress bar
with tqdm(total=n, desc="Compressing images", unit="img", ncols=80, colour='cyan') as pbar:
    for file_path in file_list:
        rel_dir = os.path.dirname(file_path).replace(root, target_path)
        os.makedirs(rel_dir, exist_ok=True)

        name = os.path.basename(file_path)
        ext = os.path.splitext(name)[1]
        new_name = name.replace(ext, '.jpg')
        image_path = os.path.join(rel_dir, new_name)

        try:
            im = Image.open(file_path)

            # DRAW text overlay
            draw = ImageDraw.Draw(im)
            im_text = file_path
            font = ImageFont.truetype("segoeui.ttf", 30)
            position = (10, 0)
            left, top, right, bottom = draw.textbbox(position, im_text, font=font)
            draw.rectangle((left - 20, top - 20, right + 10, bottom + 3), fill='black')
            draw.text(position, im_text, font=font, fill='white')

            # Save compressed image
            im.save(image_path, optimize=True, quality=image_quality)
        except Exception as e:
            tqdm.write(f"Error processing {file_path}: {e}")

        pbar.update(1)

# Create zip archive
zip_directory(target_path, target_path + '.zip')
print(f"\n✅ Compression complete. Zip archive created at:\n{target_path + '.zip'}")
