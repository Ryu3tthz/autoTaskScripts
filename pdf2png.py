from pdf2image import convert_from_path
import os
pdf_path = 'a.pdf'
output_dir = 'output_images'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
images = convert_from_path(pdf_path)

for i, image in enumerate(images):
    image_path = os.path.join(output_dir, f'page_{i+1}.png')
    image.save(image_path, 'PNG')
