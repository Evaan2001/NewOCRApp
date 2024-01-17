import streamlit as st
from functions import *
import requests
import json


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

print_headings(demo_limit)

# Create or get the session state

my_api_key = "K86635264288957"

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

        payload = {
            "isOverlayRequired": False,
            "apikey": my_api_key,
            "detectOrientation": True,
            "scale": True,
            "OCREngine": 2,
        }

        final_image = "test.jpg"

        with open(final_image, "rb") as f:
            r = requests.post(
                "https://api.ocr.space/parse/image",
                files={final_image: f},
                data=payload,
            )
        output = r.content.decode()
        output_dictionary = json.loads(output)

        if output_dictionary["OCRExitCode"] != 1:
            with col2:
                st.write(
                    "OCR Failed due to - " + str(output_dictionary["ErrorMessage"])
                )
        else:
            mrz = my_extract_mrz(output_dictionary["ParsedResults"][0]["ParsedText"])
            data = {}
            if (
                mrz[1][0].isalnum() and len(mrz[0]) > 10
            ):  # if len(mrz[0] + mrz[1]) == 88:
                first_line = mrz[0]
                data["country"] = first_line[2:5].strip().strip("<")
                last_name_ending_index = first_line.find("<<", 5)
                data["lastname"] = preliminary_correction(
                    first_line[5:last_name_ending_index].replace("<", " ").strip("<")
                )
                data["first_names"] = preliminary_correction(
                    first_line[last_name_ending_index:].replace("<", " ").strip()
                )

                second_line = mrz[1]
                if second_line.find(data["country"]) == -1:
                    offset = 0  # nationality(11,12,13) -> dob (14th char onwards so index=13)
                else:
                    offset = second_line.find(data["country"]) - 10

                index = 0 + offset
                data["document_number"] = (
                    second_line[index : index + 9].strip("<").strip()
                )
                index = index + 9 + 1 + 3
                data["dob"] = format_date(second_line[index : index + 6].strip("<"))
                index = index + 6
                data["sex"] = ""
                for char in second_line[index:]:
                    if char == "F" or char == "M":
                        data["sex"] = char
                        break
            else:
                pass  # Call run_mrz

            with col2:
                for key, value in data.items():
                    st.write(key + " - " + value)

else:
    st.write(
        "Free Demo is now over! Contact ahmedeva@grinnell.edu for more details or to request an extended demo"
    )
