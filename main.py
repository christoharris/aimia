from PIL import Image, ImageChops, ImageOps, ImageDraw
import streamlit as st
import math

# configure the page
st.set_page_config(page_title='Symmetry')
st.title('Symmetry')
st.write('Upload an image and choose the type of symmetry')
file = st.file_uploader('Enter Image', type=['jpg', 'png'])

def square(upload):

    # initiate image variable
    image1 = upload

    # flip image horizontally
    image2 = image1.transpose(Image.FLIP_LEFT_RIGHT)
    
    # creates a canvas with dimensional integrity and stores into variable 'combined'
    combined = Image.new("RGB", (image1.width + image2.width, image1.height))

    # pastes the image into the canvas at the origin
    combined.paste(image1, (0, 0))

    # pastes the reflected image into the canvas
    combined.paste(image2, (image1.width, 0))

    # flips the canvas 'combined' and stores the vertical transformation into the variable flipped_combined
    flipped_combined = combined.transpose(Image.FLIP_TOP_BOTTOM)

    # creates a canvas for the vertical transformation and orignal combined variable to be pasted into
    new_combined = Image.new("RGB", (combined.width, combined.height * 2))

    # Paste the original combined image at the top
    new_combined.paste(combined, (0, 0))

    # Paste the vertical transformation at the bottom of new canvas, final four square product.
    new_combined.paste(flipped_combined, (0, combined.height))

    return new_combined

def radial(upload, num_segments):
    # initiate image variable
    image = upload.convert("RGBA")  # Convert the image to RGBA mode

    # calculate the dimensions of the output image
    output_size = int(math.sqrt(image.width ** 2 + image.height ** 2))
    output_image = Image.new("RGBA", (output_size, output_size), (255, 255, 255, 0))  # Create a transparent output image

    # calculate the center of the output image
    center_x = output_size // 2
    center_y = output_size // 2

    # loop through each segment
    for i in range(num_segments):
        # calculate the rotation angle for the current segment
        angle = i * (360 / num_segments)

        # rotate the image
        rotated_image = image.rotate(angle, expand=True)

        # calculate the position to paste the rotated image
        paste_x = center_x - rotated_image.width // 2
        paste_y = center_y - rotated_image.height // 2

        # create a mask for the rotated image
        mask = rotated_image.split()[-1]  # Get the alpha channel as the mask

        # paste the rotated image onto the output image using the mask
        output_image.paste(rotated_image, (paste_x, paste_y), mask)

    return output_image


def distort_symmetry(upload, distortion_level):
    # initiate image variable
    image = upload.convert("RGBA")

    # apply distortion to the image
    distorted_images = []
    for i in range(int(distortion_level)):
        distorted_image = image.copy()
        distorted_image = distorted_image.resize((int(distorted_image.width * (1 - i * 0.1)), int(distorted_image.height * (1 - i * 0.1))))
        distorted_image = distorted_image.resize(image.size, Image.LANCZOS)
        distorted_images.append(distorted_image)

    # create a mask for the distorted image
    mask = Image.new("L", image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, image.width, image.height), fill=255)

    # create the output image
    output_image = Image.new("RGBA", image.size)

    # paste the distorted images and their mirrored versions
    for i, distorted_image in enumerate(distorted_images):
        # apply the mask to the distorted image
        distorted_image.putalpha(mask)

        # create a mirrored version of the distorted image
        mirrored_image = ImageOps.mirror(distorted_image)

        # calculate the positions to paste the images
        offset = i * (image.width // (2 * distortion_level))
        output_image.paste(distorted_image, (offset, 0), distorted_image)
        output_image.paste(mirrored_image, (image.width - offset - distorted_image.width, 0), mirrored_image)

    return output_image

def circular_symmetry(upload, num_rectangles):
    # initiate image variable
    image = upload.convert("RGBA")

    # calculate the size of each rectangle
    rect_width = image.width // num_rectangles
    rect_height = image.height

    # create the output image
    output_size = int(math.sqrt(2) * max(image.width, image.height))
    output_image = Image.new("RGBA", (output_size, output_size))

    # calculate the center of the output image
    center_x = output_size // 2
    center_y = output_size // 2

    # iterate over the rectangles and rotate them around the center
    for i in range(num_rectangles):
        # calculate the coordinates of the current rectangle
        left = i * rect_width
        top = 0
        right = left + rect_width
        bottom = rect_height

        # crop the rectangle from the input image
        rect_image = image.crop((left, top, right, bottom))

        # calculate the rotation angle for the current rectangle
        angle = i * (360 / num_rectangles)

        # rotate the rectangle
        rotated_rect = rect_image.rotate(angle, expand=True)

        # calculate the position to paste the rotated rectangle
        offset_x = center_x - rotated_rect.width // 2
        offset_y = center_y - rotated_rect.height // 2

        # paste the rotated rectangle onto the output image
        output_image.paste(rotated_rect, (offset_x, offset_y), rotated_rect)

    return output_image

# ... (previous code remains the same)

def triangular_symmetry(upload, num_triangles):
    # initiate image variable
    image = upload.convert("RGBA")

    # calculate the size of each triangle
    triangle_width = image.width // num_triangles
    triangle_height = image.height

    # create the output image
    output_size = max(image.width, image.height)
    output_image = Image.new("RGBA", (output_size, output_size))

    # calculate the center of the output image
    center_x = output_size // 2
    center_y = output_size // 2

    # create a mask for the triangle
    triangle_mask = Image.new("L", (triangle_width, triangle_height), 0)
    draw = ImageDraw.Draw(triangle_mask)
    draw.polygon([(0, triangle_height), (triangle_width // 2, 0), (triangle_width, triangle_height)], fill=255)

    # calculate the rotation angle for each triangle
    angle_step = 360 / num_triangles

    # iterate over the triangles and rotate them to form a larger triangle
    for i in range(num_triangles):
        # calculate the coordinates of the current triangle
        left = i * triangle_width
        top = 0
        right = left + triangle_width
        bottom = triangle_height

        # crop the triangle from the input image
        triangle_image = image.crop((left, top, right, bottom))

        # apply the triangle mask to the cropped image
        triangle_image.putalpha(triangle_mask)

        # calculate the rotation angle for the current triangle
        angle = i * angle_step

        # rotate the triangle
        rotated_triangle = triangle_image.rotate(angle, expand=True)

        # calculate the position to paste the rotated triangle
        offset_x = center_x - rotated_triangle.width // 2
        offset_y = center_y - rotated_triangle.height // 2

        # paste the rotated triangle onto the output image
        output_image.paste(rotated_triangle, (offset_x, offset_y), rotated_triangle)

    return output_image

# ... (previous code remains the same)

if file is not None:
    image = Image.open(file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

    # symmetry type selection
    symmetry_type = st.selectbox('Select Symmetry Type', ('Reflective', 'Radial', 'Distort', 'Circular', 'Triangular'))

    if symmetry_type == 'Reflective':
        result_image = square(image)
    elif symmetry_type == 'Radial':
        num_segments = st.slider('Number of Segments', min_value=2, max_value=12, value=6)
        result_image = radial(image, num_segments)
    elif symmetry_type == 'Distort':
        distortion_level = st.slider('Distortion Level', min_value=1, max_value=10, value=1, step=1)
        result_image = distort_symmetry(image, distortion_level)
    elif symmetry_type == 'Circular':
        gcd_value = math.gcd(image.width, image.height)
        max_factor = 10
        num_rectangles = st.slider('Number of Rectangles', min_value=2, max_value=1000, value=min(10, gcd_value), step=gcd_value)
        result_image = circular_symmetry(image, num_rectangles)
    else:
        num_triangles = st.slider('Number of Triangles', min_value=2, max_value=1000, value=3, step=1)
        result_image = triangular_symmetry(image, num_triangles)

    st.image(result_image, caption='Symmetry Result', use_column_width=True)
