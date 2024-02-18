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
What's The Logic?
</h2>

<div align="center">
 
Every passport has a *Machine Readable Zone*, or ***MRZ*** for short. The MRZ is a standardized format for encoding essential passport holder information in a format that can be easily read by machine. It consists of two or three lines of text at the bottom of the personal information page of a passport. Here's a good article on [how we can decode an MRZ](https://www.linkedin.com/pulse/machine-readable-zone-mrz-decoding-globalpassag/). 
</div>


<p  align="center">
<img  src="https://github.com/Evaan2001/Images_For_ReadMe/blob/main/passport_mrz.png"
width = "400"/>

<div align="center">
 
[PyImageSearch](https://pyimagesearch.com/) has a good article on how we can [isolate the MRZ using traditional Computer Vision methods](https://pyimagesearch.com/2021/12/01/ocr-passports-with-opencv-and-tesseract/), so no fancy ML models. The author then suggests using HP/Google's Tesseract OCR engine to OCR the identified MRZ area (OCR simply means getting all the words/characters in an image). However, PyImageSearch's MRZ-identifying code proved unreliable from my tests. Additionally, Tesseract often made errors while OCRing characters in the Passport-Font.
</div>

<div align="center">
 
I then ran into [PassportEye](https://github.com/konstantint/PassportEye), a Python library and a command-line tool that claims to be able to extract the relevant details from a photo of a passport. It is also rotation-invariant, so it works for images rotated by 90°, 180°, or 270°. However, I found that the author's algorithm works well only if we hava a close-up photo of a passport. Anything in the background triggers a lot of errors. Plus, it uses the Tesseract OCR engine which, as discussed above, is not the best for the passport font.
</div>

<div align="center">
 
I then discovered the [Free OCR API by ocr.space](https://ocr.space/OCRAPI). It's *OCR Engine 2* works really well for the Passport Font. However, my testing revealed that the OCR loses accuracy when working on a close-up shot of a passport. So, I decided to combine this with the PassportEye library to get the following algorithm:
</div>
