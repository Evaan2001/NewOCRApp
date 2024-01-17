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


def preliminary_correction(name):
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
    # print(str(len(mrz_string)) + " - " + mrz_string)
    line1_endpoint = 0
    if len(mrz_string) == 88:
        line1_endpoint = 43
    else:
        for index in range(len(mrz_string) // 2):
            char = mrz_string[index]
            if not (char.isalpha() or char.isdigit()):
                line1_endpoint = index

    return [
        mrz_string[0 : line1_endpoint + 1],
        mrz_string[line1_endpoint + 1 :].strip("<"),
    ]
