import streamlit as st
from functions import *
import concurrent.futures
import time


def read_file():
    with open("images_processed.txt", "r") as file:
        num_images = file.read()
    return int(num_images.strip())


def overwrite_file(num_images):
    with open("images_processed.txt", "w") as file:
        file.write(num_images)


def print_headings(demo_limit):
    st.markdown(
        "<h1 style='text-align: center; color: rgb(133, 196, 230);'>Passport OCR App</h1>",
        unsafe_allow_html=True,
    )
    st.divider()
    subheader_text = str(demo_limit) + " Total Free Uploads"
    st.markdown(
        f"<h2 style='text-align: center; color: lightblue;'>{subheader_text}</h2>",
        unsafe_allow_html=True,
    )


image_count = read_file()
demo_limit = 75
my_api_key = "K86635264288957"

print_headings(demo_limit)


if image_count < demo_limit:
    uploaded_image = st.file_uploader(
        label="Upload Passport Image", type=["png", "jpg", "jpeg"]
    )
    if uploaded_image:
        # Increment the image counter
        image_count = image_count + 1
        # Update the session state
        overwrite_file(str(image_count))

        st.write("Number of images processed - ", image_count, "/", demo_limit)

        # To read file as bytes:
        bytes_data = uploaded_image.getvalue()
        file_path = "image.jpg"
        # Write the bytes to the file
        with open(file_path, "wb") as file:
            file.write(bytes_data)

        col1, col2 = st.columns(2)
        with col1:
            st.image(
                uploaded_image,
                caption="Uploaded Image",
                channels="RGB",
                output_format="auto",
            )

        image = "image.jpg"
        reduce_image_size(image, "test.jpg")

        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Submit the get_data function
            future_get_data = executor.submit(get_data, my_api_key)
            try:
                # Wait for the get_data function to finish or timeout after 20 seconds
                user_data = future_get_data.result(timeout=35)
                if not bool(user_data):
                    output = run_mrz(image)
                    with col2:
                        for key, value in output.items():
                            st.write(key + " - " + value)
                elif (
                    user_data["first_names"].strip() == ""
                    or user_data["lastname"].strip() == ""
                ):
                    output = run_mrz(image)
                    with col2:
                        for key, value in output.items():
                            st.write(key + " - " + value)
                else:
                    with col2:
                        for key, value in user_data.items():
                            if key == "lastname" or key == "first_names":
                                continue
                            st.write(key + " - " + value)
            except concurrent.futures.TimeoutError:
                future_get_data.cancel()  # Cancel the get_data task
                # Submit the run_mrz function
                future_run_mrz = executor.submit(run_mrz, image)
                run_mrz_result = future_run_mrz.result()
                with col2:
                    for key, value in run_mrz_result.items():
                        st.write(key + " - " + value)


else:
    st.write(
        "Free Demo is now over! Contact ahmedeva@grinnell.edu for more details or to request an extended demo"
    )
