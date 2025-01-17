import os
import sys
import pathlib
import zipfile
from fnmatch import fnmatch
from PIL import Image, ImageDraw, ImageFont


def zip_directory(folder_path, zip_path):
    with zipfile.ZipFile(zip_path, mode='w') as zipf:
        len_dir_path = len(folder_path)
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, file_path[len_dir_path:])


# Paste root path to directory with test that contains all subdirectories and files to be compressed
### THE ONLY INPUT THAT NEEDS TO BE CHANGED PER NEW JOB ###
#root = r'N:\Common\B_lab\Monica Wiberg\TCS-2751 Slitstyrka 430GT 2'
root = sys.argv[1]
image_quality = 30 # Retained image quality, in %

# Main location for exporting compressed images to
target_path = 'C:\Image Compression Exports'
try:
    os.mkdir(target_path)
except:
    print(f'Directory already exists')
print(f'root path: {root}\ntarget path: {target_path}')


'''
Create folder in main location for export
'''
# Get name of parent folder
root_subdir = pathlib.PurePath(root).name

# Create new subdirectory for current job
target_path = target_path + '/' + root_subdir + '_comp'
try:
    os.mkdir(target_path)
except:
    print(f'Directory already exists')


'''
Image compression part
'''
pattern = "*.tif"
patterns = ['*.tif', '*.bmp', '*.jpg', '*.png']

n = 1 # Variable to count number of files
i = 1 # Loop variable to count how many files have been processed

for pattern in patterns:
    for path, subdirs, files in os.walk(root):
        for file in files:
            if fnmatch(file, pattern):
                n += 1
        


for pattern in patterns:
    # Loop to go through all subdirectories and files in root location, compress images, and then save compressed images to export location
    for path, subdirs, files in os.walk(root):
        target_subdir_path = path.replace(root, target_path)
        new_path = target_subdir_path

        try:
            os.mkdir(new_path)
        except:
            pass

        for name in files:

            if fnmatch(name, pattern):
                file_path = os.path.join(path, name)

                im = Image.open(file_path)
                new_name = name.replace(pattern[1:], '.jpg')
                try:
                    os.mkdir(new_path)
                except:
                    pass
                

                i += 1
                image_path = new_path + '/' + new_name
                '''
                DRAW METHOD
                '''

                # DRAW HERE #
                draw = ImageDraw.Draw(im)
                im_text = file_path
                font = ImageFont.truetype("segoeui.ttf", 30)
                position = (10, 0)
                left, top, right, bottom = draw.textbbox(position, im_text, font=font)

                bbox = draw.textbbox(position, im_text, font=font)
                draw.rectangle((left-20, top-20, right+10, bottom+3), fill='black')
                draw.text(position, im_text, font=font, fill='white')
                '''
                END DRAW
                '''

                im.save(image_path, optimize=True, quality=30)
                
                os.system('cls||clear')
                print(f'{int(100*i/n)}% Completed \t Processed images {i}/{n} \t')

# Create a zip archive with the compressed directories and images
zip_directory(target_path, target_path+'.zip')
