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

<p  align="center">
Every passport has a *Machine Readable Zone*, or ***MRZ*** for short. The MRZ is a standardized format for encoding essential passport holder information in a format that can be easily read by machine. It consists of two or three lines of text at the bottom of the personal information page of a passport. Here's a good article on [how we can decode an MRZ](https://www.linkedin.com/pulse/machine-readable-zone-mrz-decoding-globalpassag/). 
</p>

https://pyimagesearch.com/

<p  align="center">
<img  src="https://github.com/Evaan2001/Images_For_ReadMe/blob/main/passport_mrz.png"
width = "400"/>

