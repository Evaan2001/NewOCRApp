def format_date(input_date, is_expiration_date=False):
    from datetime import date

    current_year = date.today().year

    year = input_date[0:2]
    month = input_date[2:4]
    day = input_date[4:]

    reference_date = current_year % 100
    if is_expiration_date is True:
        reference_date = reference_date + 10

    if int(year) > reference_date:
        year = "19" + year
    else:
        year = "20" + year

    formatted_date = month + "/" + day + "/" + year
    return formatted_date


def new_preliminary_correction(name):
    name = name.strip()
    new_name = name + "  "
    for i in range(len(name)):
        if name[i].isspace() and name[i + 1].isspace():
            new_name = name[0:i]
            break
        if name[i].isalpha() == False and name[i].isspace() == False:
            new_name = name[0:i]
            break
        # if (
        #     name[i].isspace()
        #     and name[i + 1] == "K"
        #     and (name[i + 2] == "K" or name[i + 2].isspace())
        # ):
        #     new_name = name[0:i]
        #     break

    return new_name.strip()


""" Helper Function"""


def k_proportion(name):
    k_count = 0
    for char in name:
        if char == "K":
            k_count = k_count + 1
    return k_count / len(name)


def advanced_correction(name):
    new_name = name.strip()
    list_of_names = new_name.split()
    output = ""

    for name_part in list_of_names:
        if k_proportion(name_part) > 0.25:
            name_part = name_part.strip("K")
        output = output + " " + name_part

    output = output.strip()
    return output


def reduce_image_size(input_path, output_path, target_size_kb=1024, quality=95):
    import cv2

    """
    Reduce the file size of an image by adjusting JPEG compression.

    Args:
    - input_path (str): Path to the input image.
    - output_path (str): Path to save the reduced-size image.
    - target_size_kb (int): Target size in kilobytes.
    - quality (int): JPEG compression quality (0-100).

    Returns:
    - None
    """
    try:
        # Read the input image
        img = cv2.imread(input_path)

        # Encode the image with JPEG compression
        _, encoded_img = cv2.imencode(
            ".jpg", img, [int(cv2.IMWRITE_JPEG_QUALITY), quality]
        )

        # Calculate the current size
        current_size_kb = len(encoded_img.tobytes()) / 1024

        # Adjust quality until the target size is reached or exceeded
        while current_size_kb > target_size_kb and quality > 0:
            quality -= 5
            _, encoded_img = cv2.imencode(
                ".jpg", img, [int(cv2.IMWRITE_JPEG_QUALITY), quality]
            )
            current_size_kb = len(encoded_img.tobytes()) / 1024

        # Write the reduced-size image
        with open(output_path, "wb") as output_file:
            output_file.write(encoded_img.tobytes())

    except Exception as e:
        print(f"Error: {e}")


def num_of_letters(my_string):
    count = 0
    for char in my_string:
        if char.isalpha():
            count = count + 1

    return count


def get_first_n_alphabets(input_string, n):
    result = ""
    count = 0
    index = 0

    for char in input_string:
        index = index + 1
        if char.isalpha():
            result += char
            count += 1

            if count == n:
                break

    return (result, index)


def strip_non_alphanumeric_from_ends(input_string):
    # return input_string
    import re

    # Use a regular expression to match non-alphanumeric characters
    pattern = re.compile(r"^[^a-zA-Z0-9]+|[^a-zA-Z0-9]+$")

    # Strip non-alphanumeric characters from the beginning and end
    stripped_string = pattern.sub("", input_string)

    return stripped_string


def my_extract_mrz(text):
    # Split the text into lines
    lines = text.split("\n")
    i = -1
    j = -1
    index = 0
    for line in lines:
        if "<" in line:
            if i == -1:
                i = index
            else:
                j = index
        index = index + 1

    mrz_lines = lines[i : j + 1]

    # Concatenate matching lines to form the MRZ string
    mrz_string = "".join(mrz_lines)
    line1_endpoint = 0
    if len(mrz_string) == 88:
        line1_endpoint = 43
    else:
        for index in range(len(mrz_string) // 2):
            char = mrz_string[index]
            if not (char.isalpha() or char.isdigit()):
                line1_endpoint = index
    return [
        strip_non_alphanumeric_from_ends(mrz_string[0 : line1_endpoint + 1]),
        strip_non_alphanumeric_from_ends(mrz_string[line1_endpoint + 1 :].strip("<")),
    ]


def preliminary_correction(name):
    name = name.strip()
    new_name = name + "  "
    for i in range(len(name)):
        if name[i].isspace() and name[i + 1].isspace():
            new_name = name[0:i]
            break
        if (
            name[i].isspace()
            and name[i + 1] == "K"
            and (name[i + 2] == "K" or name[i + 2].isspace())
        ):
            new_name = name[0:i]
            break

    return new_name.strip()


""" Helper Function"""


def k_proportion(name):
    k_count = 0
    for char in name:
        if char == "K":
            k_count = k_count + 1
    return k_count / len(name)


def advanced_correction(name):
    new_name = name.strip()
    list_of_names = new_name.split()
    output = ""

    for name_part in list_of_names:
        if k_proportion(name_part) > 0.25:
            name_part = name_part.strip("K")
        output = output + " " + name_part

    output = output.strip()
    return output


def run_mrz(image):
    from passporteye import read_mrz

    output = {}
    try:
        mrz = read_mrz(image)
        if mrz is None:
            output["Couldn't Process"] = "Not A Passport"
            return output
        data = mrz.to_dict()
        # Now select relevant fields
        country = data["country"].strip("<")
        output["country"] = country
        first_name = data["names"].strip("<")
        surname = data["surname"].strip("<")
        first_name = advanced_correction(preliminary_correction(first_name))
        surname = advanced_correction(preliminary_correction(surname))
        output["name"] = first_name + " " + surname
        passport_number = data["number"].strip("<")
        output["document_number"] = passport_number
        dob = format_date(data["date_of_birth"].strip("<"), False)
        output["dob"] = dob
        output["sex"] = data["sex"].strip("<")
    except Exception as e:
        output[
            "warning"
        ] = "An error occurred while processing the uploaded passport image. This is what was extracted and is probably incorrect: "
    finally:
        return output


def get_data(my_api_key):
    import requests
    import json

    try:
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
            return {}
        else:
            mrz = my_extract_mrz(output_dictionary["ParsedResults"][0]["ParsedText"])
            data = {}
            if type(mrz) is not list:
                return data  # print("MRZ Extraction Failed")
            elif len(mrz[0]) <= 10 or len(mrz[1]) <= 10:
                return data  # print("Extracted MRZ is too short")
            elif mrz[1][0].isalnum() == False:
                return data  # print("Second MRZ line doesn't begin with an alphabet or number")
            else:  # if mrz[1][0].isalnum() and len(mrz[0]) > 10: # if len(mrz[0] + mrz[1]) == 88:
                first_line = mrz[0]

                data["country"] = first_line[2:5].strip().strip("<")
                num_letters = num_of_letters(data["country"])
                if num_letters < 3:
                    adjustments = get_first_n_alphabets(first_line[5:], 3 - num_letters)
                    data["country"] = data["country"].replace(" ", "") + adjustments[0]
                    first_line = (
                        first_line[:5].strip() + first_line[4 + adjustments[1] :]
                    )

                last_name_ending_index = first_line.find("<<", 5)
                data["lastname"] = new_preliminary_correction(
                    first_line[5:last_name_ending_index].replace("<", " ").strip("<")
                )
                data["first_names"] = new_preliminary_correction(
                    first_line[last_name_ending_index:].replace("<", " ").strip()
                )

                data["name"] = data["first_names"] + " " + data["lastname"]

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

                return data
    except Exception as generic_error:
        return {}
