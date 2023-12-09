from PIL import Image, ImageChops
import streamlit as st

# configue the page
st.set_page_config(page_title='Four times')
st.title('Four times')



def sqaure(upload):
    image1 = upload
    image2 = image1.transpose(Image.FLIP_LEFT_RIGHT)
    base_height = min(image1.height, image2.height)
    image1 = image1.resize((int((base_height / image1.height) * image1.width), base_height))
    image2 = image2.resize((int((base_height / image2.height) * image2.width), base_height))
    combined = Image.new("RGB", (image1.width + image2.width, base_height))
    combined.paste(image1, (0, 0))
    combined.paste(image2, (image1.width, 0))

    # flip combined and paste it below
    flipped_combined = combined.transpose(Image.FLIP_TOP_BOTTOM)
    new_combined = Image.new("RGB", (combined.width, combined.height * 2))

    # Paste the original combined image at the top
    new_combined.paste(combined, (0, 0))

    # Paste the flipped image at the bottom
    new_combined.paste(flipped_combined, (0, combined.height))

    # Save the final image
    return new_combined
        

    # combined.save("combined.jpg")
    # combined.save("combined.jpg")


# file input
file = st.file_uploader('Enter Image', type=['jpg', 'png'])


if file is not None:
    # Open the image file
    image = Image.open(file)
    
    # Display image
    # st.image(image, caption='Uploaded Image', use_column_width=True)
    four_times = sqaure(image)


    st.image(four_times, caption='Uploaded Image', use_column_width=True)