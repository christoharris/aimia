from PIL import Image, ImageChops, ImageOps, ImageDraw
import streamlit as st
import math

# configure the page
st.set_page_config(page_title='Symmetry')
st.title('Symmetry')
st.write('Upload an image and choose the type of symmetry')
file = st.file_uploader('Enter Image', type=['jpg', 'png'])

def reflective_symmetry(upload, num_reflections, reflect_mode):
    # initiate image variable
    image = upload

    if reflect_mode == 'Square':
        # create the output image for square reflection
        output_width = image.width * 2
        output_height = image.height * 2
        output_image = Image.new("RGB", (output_width, output_height))

        # paste the original image in the top-left quadrant
        output_image.paste(image, (0, 0))

        # reflect the image horizontally and paste in the top-right quadrant
        reflection_h = image.transpose(Image.FLIP_LEFT_RIGHT)
        output_image.paste(reflection_h, (image.width, 0))

        # reflect the image vertically and paste in the bottom-left quadrant
        reflection_v = image.transpose(Image.FLIP_TOP_BOTTOM)
        output_image.paste(reflection_v, (0, image.height))

        # reflect the image both horizontally and vertically and paste in the bottom-right quadrant
        reflection_hv = reflection_h.transpose(Image.FLIP_TOP_BOTTOM)
        output_image.paste(reflection_hv, (image.width, image.height))

        # apply the reflections multiple times based on the num_reflections slider
        for _ in range(num_reflections - 1):
            output_image = reflective_symmetry(output_image, 1, 'Square')

    else:
        # create the output image for row reflection
        output_width = image.width * 2
        output_height = image.height
        output_image = Image.new("RGB", (output_width, output_height))

        # paste the original image on the left side
        output_image.paste(image, (0, 0))

        # reflect the image horizontally and paste on the right side
        reflection = image.transpose(Image.FLIP_LEFT_RIGHT)
        output_image.paste(reflection, (image.width, 0))

        # apply the reflections multiple times based on the num_reflections slider
        for _ in range(num_reflections - 1):
            output_image = reflective_symmetry(output_image, 1, 'Row')

    return output_image

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


def dilation_symmetry(upload, num_rectangles, dilation_factor):
    # initiate image variable
    image = upload.convert("RGBA")

    # calculate the size of each rectangle
    rect_width = image.width // num_rectangles
    rect_height = image.height

    # create the output image
    output_size = int(max(image.width, image.height) * dilation_factor)
    output_image = Image.new("RGBA", (output_size, output_size))

    # calculate the center of the output image
    center_x = output_size // 2
    center_y = output_size // 2

    # iterate over the rectangles and apply dilation
    for i in range(num_rectangles):
        # calculate the coordinates of the current rectangle
        left = i * rect_width
        top = 0
        right = left + rect_width
        bottom = rect_height

        # crop the rectangle from the input image
        rect_image = image.crop((left, top, right, bottom))

        # calculate the dilation size for the current rectangle
        dilation_size = int(rect_width * dilation_factor)

        # resize the rectangle based on the dilation size
        dilated_rect = rect_image.resize((dilation_size, rect_height), Image.ANTIALIAS)

        # calculate the position to paste the dilated rectangle
        offset_x = center_x - (i + 0.5) * dilation_size
        offset_y = center_y - rect_height // 2

        # paste the dilated rectangle onto the output image
        output_image.paste(dilated_rect, (int(offset_x), offset_y), dilated_rect)

    return output_image

def mesh_symmetry(upload, num_rectangles):
    # initiate image variable
    image = upload.convert("RGBA")

    # calculate the size of each rectangle based on the image dimensions
    rect_width = image.width // num_rectangles
    rect_height = image.height // num_rectangles

    # create the output image with the same size as the input image
    output_image = Image.new("RGBA", (image.width, image.height))

    # iterate over the rectangles and rotate them
    for i in range(num_rectangles):
        for j in range(num_rectangles):
            # calculate the coordinates of the current rectangle
            left = i * rect_width
            top = j * rect_height
            right = left + rect_width
            bottom = top + rect_height

            # crop the rectangle from the input image
            rect_image = image.crop((left, top, right, bottom))

            # calculate the rotation angle for the current rectangle
            angle = (i * num_rectangles + j) * (360 / (num_rectangles ** 2))

            # rotate the rectangle
            rotated_rect = rect_image.rotate(angle, expand=True)

            # calculate the position to paste the rotated rectangle
            paste_left = left + (rect_width - rotated_rect.width) // 2
            paste_top = top + (rect_height - rotated_rect.height) // 2

            # paste the rotated rectangle onto the output image
            output_image.paste(rotated_rect, (paste_left, paste_top), rotated_rect)

    return output_image

def spiral_symmetry(upload, num_rotations, scale_factor):
    # initiate image variable
    image = upload.convert("RGBA")

    # create the output image
    output_size = max(image.width, image.height)
    output_image = Image.new("RGBA", (output_size, output_size))

    # calculate the center of the output image
    center_x = output_size // 2
    center_y = output_size // 2

    # calculate the angle increment for each rotation
    angle_increment = 360 / num_rotations

    # iterate over the rotations
    for i in range(num_rotations):
        # calculate the current angle
        angle = i * angle_increment

        # calculate the scale factor for the current rotation
        scale = 1 - (i / num_rotations) * (1 - scale_factor)

        # rotate and scale the image
        rotated_image = image.rotate(angle, expand=True)
        scaled_image = rotated_image.resize((int(rotated_image.width * scale), int(rotated_image.height * scale)))

        # calculate the position to paste the scaled image
        paste_x = center_x - scaled_image.width // 2
        paste_y = center_y - scaled_image.height // 2

        # paste the scaled image onto the output image
        output_image.paste(scaled_image, (paste_x, paste_y), scaled_image)

    return output_image
# ... (previous code remains the same)
def kaleidoscope_symmetry(upload, num_segments):
    # initiate image variable
    image = upload.convert("RGBA")

    # create the output image
    output_size = max(image.width, image.height)
    output_image = Image.new("RGBA", (output_size, output_size))

    # calculate the angle increment for each segment
    angle_increment = 360 / num_segments

    # iterate over the segments
    for i in range(num_segments):
        # calculate the rotation angle for the current segment
        angle = i * angle_increment

        # rotate the image
        rotated_image = image.rotate(angle, expand=True)

        # create a mirrored version of the rotated image
        mirrored_image = ImageOps.mirror(rotated_image)

        # calculate the position to paste the mirrored image
        paste_x = (output_size - mirrored_image.width) // 2
        paste_y = (output_size - mirrored_image.height) // 2

        # paste the mirrored image onto the output image
        output_image.paste(mirrored_image, (paste_x, paste_y), mirrored_image)

    return output_image

if file is not None:
    image = Image.open(file)
    st.image(image, caption='Uploaded Image', use_column_width=True)
    
    # store the uploaded image in the session state
    st.session_state.uploaded_image = image

# check if there is a transformed image in the session state
if 'transformed_image' in st.session_state:
    # display the transformed image
    st.image(st.session_state.transformed_image, caption='Transformed Image', use_column_width=True)
    
    # provide a button to re-enter the transformed image
    if st.button('Re-enter Transformed Image'):
        st.session_state.uploaded_image = st.session_state.transformed_image

# check if there is an uploaded image in the session state

if 'uploaded_image' in st.session_state:
    # symmetry type selection
    symmetry_type = st.selectbox('Select Symmetry Type', ('Reflective', 'Circular', 'Triangular', 'Dilation', 'Mesh', 'Spiral', 'Kaleidoscope'))

    if symmetry_type == 'Reflective':
        num_reflections = st.slider('Number of Reflections', min_value=1, max_value=10, value=2, step=1)
        reflect_mode = st.radio('Reflection Mode', ('Square', 'Row'))
        result_image = reflective_symmetry(st.session_state.uploaded_image, num_reflections, reflect_mode)
    elif symmetry_type == 'Circular':
        num_rectangles = st.slider('Number of Rectangles', min_value=2, max_value=500, value=10, step=1)
        result_image = circular_symmetry(st.session_state.uploaded_image, num_rectangles)
    elif symmetry_type == 'Triangular':
        num_triangles = st.slider('Number of Triangles', min_value=2, max_value=500, value=3, step=1)
        result_image = triangular_symmetry(st.session_state.uploaded_image, num_triangles)
    elif symmetry_type == 'Dilation':
        num_rectangles = st.slider('Number of Rectangles', min_value=2, max_value=500, value=4, step=1)
        dilation_factor = st.slider('Dilation Factor', min_value=1.0, max_value=5.0, value=2.0, step=0.1)
        result_image = dilation_symmetry(st.session_state.uploaded_image, num_rectangles, dilation_factor)
    elif symmetry_type == 'Mesh':
        num_rectangles = st.slider('Number of Rectangles', min_value=2, max_value=500, value=10, step=1)
        result_image = mesh_symmetry(st.session_state.uploaded_image, num_rectangles)
    elif symmetry_type == 'Spiral':
        num_rotations = st.slider('Number of Rotations', min_value=1, max_value=100, value=50, step=1)
        scale_factor = st.slider('Scale Factor', min_value=0.001, max_value=1.0, value=0.01, step=0.01)
        result_image = spiral_symmetry(st.session_state.uploaded_image, num_rotations, scale_factor)
    else:
        num_segments = st.slider('Number of Segments', min_value=2, max_value=36, value=8, step=1)
        result_image = kaleidoscope_symmetry(st.session_state.uploaded_image, num_segments)
    
    st.image(result_image, caption='Symmetry Result', use_column_width=True)
    
    # add a button to output half of the symmetry result
    if st.button('Output Half'):
        half_width = result_image.width // 2
        half_height = result_image.height
        half_image = result_image.crop((0, 0, half_width, half_height))
        st.image(half_image, caption='Half Symmetry Result', use_column_width=True)
    
    # store the transformed image in the session state
    st.session_state.transformed_image = result_image
