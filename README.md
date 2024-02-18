<p  align="center">
<img  src="https://github.com/Evaan2001/Images_For_ReadMe/blob/main/Passport_OCR_App.png"
width = "900"/>

</p>
<h3 align="center">
We'll create a web-app where users can upload a photo of a passport and extract the essential details! 
</h3>

<div align="center">

I was freelancing for a security company in Austin, TX, and was tasked to write code for an embedded device to extract someone's information from a photo of their passport. I took that software and created a web-app using [Streamlit](https://streamlit.io) so that others can also use my work. Click here to [use my app](https://revisedocr.streamlit.app/)!
</div>

<h2 align="center"> 
What Information Can We Get?
</h2>
 
<p  align="center">
Given a photo of a passport, my software can retrieve the following:
</p>

1. Passport Issuing Country (It's almost always the country of citizenship of the passport holder)
2. Full Name
3. Passport Number
4. Date of Birth
5. Sex

<h2 align="center"> 
What's The Process?
</h2>

<div align="center">
 
Every passport has a *Machine Readable Zone*, or ***MRZ*** for short. The MRZ is a standardized format for encoding essential passport holder information in a format that can be easily read by machine. It consists of two or three lines of text at the bottom of the personal information page of a passport. Here's a good article on [how we can decode an MRZ](https://www.linkedin.com/pulse/machine-readable-zone-mrz-decoding-globalpassag/). 
</div>


<p  align="center">
<img  src="https://github.com/Evaan2001/Images_For_ReadMe/blob/main/passport_mrz.png"
width = "400"/>

<div align="left">
 
[PyImageSearch](https://pyimagesearch.com/) has a good article on how we can [isolate the MRZ using traditional Computer Vision methods](https://pyimagesearch.com/2021/12/01/ocr-passports-with-opencv-and-tesseract/), so no fancy ML models. The author then suggests using HP/Google's Tesseract OCR engine to OCR the identified MRZ area (OCR simply means getting all the words/characters in an image). However, PyImageSearch's MRZ-identifying code proved unreliable from my tests. Additionally, Tesseract often made errors while OCRing characters in the Passport-Font.
</div>

<div align="left">
 
I then ran into [PassportEye](https://github.com/konstantint/PassportEye), a Python library and a command-line tool that claims to be able to extract the relevant details from a photo of a passport. It is also rotation-invariant, so it works for images rotated by 90°, 180°, or 270°. However, I found that the author's algorithm works well only if we hava a close-up photo of a passport. Anything in the background triggers a lot of errors. Plus, it uses the Tesseract OCR engine which, as discussed above, is not the best for the passport font.
</div>

<div align="left">
 
I then discovered the [Free OCR API by ocr.space](https://ocr.space/OCRAPI). It's *OCR Engine 2* works really well for the Passport Font. However, my testing revealed that the OCR loses accuracy when working on a close-up shot of a passport. So, I decided to combine this with the PassportEye library to get the following algorithm:
</div>

1. Make the API call to ocr.space with the uploaded passport photo
2. Decode the OCR'ed text
3. If decoding is proving troublesome or the OCR seems inaccurate, use the PassportEye Library
4. Show output

<h2 align="center"> 
What's Streamlit?
</h2>

<div align="center">
 

Streamlit is an open-source Python library that allows you to create web applications for machine learning and data science projects quickly and easily. It is designed to make the process of building interactive web applications as simple as writing Python scripts. There are 2 parts to using Streamlit –
</div>

1. The super simple Front-End Support which makes designing the UI of the web-app a breeze
2. Hosting the web-app on the free Streamlit Cloud so that people can use your app at no cost

<h2 align="center"> 
Limitations
</h2>

<div align="center">
 
1. The free version of the ocr.space API is restricted to 500 calls per month. As such, I'm currently limiting usage of my app to 75 uploads in a week to provide equal access to everybody.
2. Because I don't have any control over the traffic present on ocr.space's servers or on the Streamlit Cloud, the process can sometimes take longer than 30 seconds, though the average processing time is about 15 seconds.
3. Based on the picture quality and the correctness of the OCR'ed text, my software is not 100% accurate. The current accuracy is 95%.
</div>

<h2 align="center"> 
Files
</h2>

<p  align="center">
Here's what you'll find –
</p>

1. *Demo_Images* – A list of images I used to test my algorithm 
2. *app-venv* – The virtual environment I used to develop this app
3. *functions.py* – A file that has a bunch of helper functions I used frequently (including my string processing functions for OCR'ed text)
4. *images_processed.txt* – A text file that records how many images my web-app has processed in the last week
5. *packages.txt* – list of Linux dependencies (installed with apt-get) outside the Python environment to be installed by Streamlit for app deployment
6. *requirements.txt* – list of python packages to be installed by Streamlit for app deployment
7. *streamlit_app.py* – python script that manages the front-end of the app and calls the relevant algorithm/function contained in *functions.py*
