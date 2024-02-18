"""
Passport OCR App

This script implements a Streamlit web application for Passport OCR (Optical Character Recognition). 
Users can upload passport images to extract the names, nationality, date of birth, sex, and passport number.
The script keeps track of the number of images processed and limits the demo to 75 free uploads in a week.

Usage:
1. Run the script.
2. Upload passport images using the file uploader.
3. Extracted passport information will be displayed on the interface.
4. The demo is limited to 75 free uploads in a week.

"""


import streamlit as st
from functions import *
import concurrent.futures
import time


def read_file():
    """
    Retrieve the number of images processed this week
    """
    with open("images_processed.txt", "r") as file:
        num_images = file.read()
    return int(num_images.strip())


def overwrite_file(num_images):
    """
    Update the number of images processed this week
    """
    with open("images_processed.txt", "w") as file:
        file.write(num_images)


def print_headings(demo_limit):
    """
    Display headings on the user's screen
    """
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


image_count = read_file() # Get how many images have already been processed in this week
demo_limit = 75
my_api_key = "K86635264288957" # My personal API key for the ocr.space API

print_headings(demo_limit)


if image_count < demo_limit:
    # If the demo limit hasn't been reached 
    uploaded_image = st.file_uploader( # Receive the uploaded image
        label="Upload Passport Image", type=["png", "jpg", "jpeg"]
    )
    if uploaded_image: # If the uploaded file is of a valid format ("png", "jpg", or "jpeg")
        # Increment the image counter
        image_count = image_count + 1
        # Update the session state
        overwrite_file(str(image_count))

        st.write("Number of images processed - ", image_count, "/", demo_limit)

        # To read file as bytes:
        # First get the uploaded image as an array of bytes
        bytes_data = uploaded_image.getvalue() 
        # Then we will create a local copy of the image (which we will later re-read as a numpy array)
        # So first let's create a file name
        file_path = "image.jpg"
        # Write the bytes to the file
        with open(file_path, "wb") as file:
            file.write(bytes_data)

        # Divide the user display into 2 columns
        col1, col2 = st.columns(2)
        # Display the uploaded image in the 1st column 
        with col1:
            st.image(
                uploaded_image,
                caption="Uploaded Image",
                channels="RGB",
                output_format="auto",
            )
        # Reducde the image size to below 1024 kb as that's a constraint enforced by the ocr.space API
        image = "image.jpg"
        reduce_image_size(image, "test.jpg")

        # Sometimes, the ocr.space API takes too long to run if there's too much server traffic or if the image is of bad quality
        # To not freeze when the web-app is running, we will create 2 threads In the 
        # In the 1st thread, we will call the ocr.space API and wait for the thread to terminate (which will terminate as soon as the API is done running)
        # If the thread does not finish running within 35 seconds, we will use our back-up PassportEye library algorithm
        
        # So let's now create 2 threads
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Run the get_data function (which calls the api) on the 1st thread
            future_get_data = executor.submit(get_data, my_api_key)
            try:
                # Wait for the get_data function to finish or timeout after 35 seconds
                user_data = future_get_data.result(timeout=35)
                # If the function does not return anything, it implies the thread was forcibly terminated via the timeout and we need to use our backup PassportEye algorithm
                if not bool(user_data): # So check if the get_data function returned anything
                    output = run_mrz(image) # If not, call the run_mrz function, which invokes the PassportEye algorithm
                    # Display the output in the 2nd column
                    with col2:
                        for key, value in output.items():
                            st.write(key + " - " + value)
                # Else if the get_date function did return something, it implies the API call finished executing without any errors
                elif ( # However, if either of the returned First Name or Last Name is an empty string, it's probably because the OCR results have errors
                    user_data["first_names"].strip() == ""
                    or user_data["lastname"].strip() == ""
                ):
                    # So call the run_mrz function, which invokes the backup PassportEye algorithm
                    output = run_mrz(image)
                    # Display the output in the 2nd column
                    with col2:
                        for key, value in output.items():
                            st.write(key + " - " + value)
                else: # If the API call terminated successfully
                    # Display the output in the 2nd column
                    with col2:
                        for key, value in user_data.items():
                            if key == "lastname" or key == "first_names":
                                continue
                            st.write(key + " - " + value)
            # If the API call was terminated after 35 seconds
            except concurrent.futures.TimeoutError:
                future_get_data.cancel()  # Cancel the get_data task
                # Submit (run) the run_mrz function, which invokes the backup PassportEye algorithm
                future_run_mrz = executor.submit(run_mrz, image)
                # Store the results
                run_mrz_result = future_run_mrz.result()
                # Display the output in the 2nd column
                with col2:
                    for key, value in run_mrz_result.items():
                        st.write(key + " - " + value)

# If the demo limit has already been reached, don't let the user upload an image and print a message instead 
else:
    st.write(
        "Free Demo is now over! Contact ahmedeva@grinnell.edu for more details or to request an extended demo"
    )
