# TeachWell

Project for ICHACK 2020 (Imperial College 24 hour hackathon)
Created by Alex Cummins, Adele Wang, Terence Hernandez, Kazuya Kai-Olowu and John Yao

# What it does

Uses facial recognition to analyze and track student response to class material.

* Uses Microsoft Azure Face technology to analyze facial expressions of students (anger, contempt, disgust, fear, happiness, sadness, surprise) and calculate dominant emotion
* Generates realtime dynamic graphing of the overall emotion in class.
* Generates downloadable report that displays how different emotions varied with time
* Also allows user to examine how each individual student responded to different materials
* Eliminates random personnel processing. Does not recognize faces that have not been inputted

# How does it work?


* Use postman to collect images detected by the cisco Mareki camera
* Send images to Microsoft Azure Face AI endpoint
* Using the Python client SDK provided by Microsoft, process image data - includes identification of dominant emotion, face recognition and tagging, looping snapshot processing every 15 seconds, generate moving average
* Send to frontend developed using React for real time updates.

# What's next?


* Add additional functionality such as allowing the teacher to add in time-stamps corresponding to different sections of the lecture integrate lesson plan uploading * smart processing of lesson plan to automatically generate time-stamp
* Integration into online classroom platform - e.g. udemy. Analyzes images passed through webcam
* Eliminating the influence of personal factors in student response using negative feedback loop, compares student response to overall class response to see if there is complete disassociation with class engagement
