# ud-blog
Multi-User Blog.

What is it?
--------------
This is a multi user blog built for the google app engine using the python SDK. It utilizes a login/authentication system, new/edit/delete posts comments and a voting system. 

Where do i get this?
--------------
This is available on github.

What do i need to run it?
--------------
You will need the latest version of python 2.7 available at www.python.org.
You will need to install the google app engine SDK from https://cloud.google.com/appengine/downloads#Google_App_Engine_SDK_for_Python.
You will either need to use google app engines native console or i recommend using bash unix shell locally (you will have to find out how to do this by which operating system you are using).


How do i run this?
--------------
you can run locally using python by going to the directory and typing dev_appserver.py . (dont forget the extra period)
The website will launch in you local host (it will list the address on the command-line)


Version:
--------------
This is an initial 1.0

What is included?
--------------
(note: these files are dependent on having the google app sdk installed..)
- app.yaml is for setting the app's name, libraries, and handlers which link local files. this will have to be modified once you start using the google app engine to launch the site.

-main.py is the main file of the app for the WSGI application.

-the index.yaml is generated by the app engine and is explained within the file.

-css folder is for local css

-sec folder contains the data, and password authentication related files.

-Templates is where all of the individual templates for the app are. 

-Handlers file is where all of the other handlers for each feature is located.

Note: .pyc file extensions will also be created documentation can be found here https://docs.python.org/2/glossary.html


Copyright and license
-------------
The MIT License (MIT)

Copyright (c) 2016 Thomas L.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.