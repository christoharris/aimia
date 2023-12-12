from PIL import Image, ImageChops
import streamlit as st

# configue the page
st.set_page_config(page_title='Four times')
st.title('Four times')

def sqaure(upload):

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
        

# file input
file = st.file_uploader('Enter Image', type=['jpg', 'png'])


if file is not None:

    image = Image.open(file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

    four_times = sqaure(image)
    st.image(four_times, caption='Uploaded Image', use_column_width=True)

