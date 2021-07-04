# Gomichan REST Backend 
1. Serves translated subtitle lines for youtube videos with highlighted grammar and pronunciation guides.
2. Generates Text-To-Speech files with Google TTS for pronunciation aids (files will appear but don't upload so, sound links do not work.)

- for use with [Gomichan-API-Tool](https://github.com/Fonzki/Gomichan-API-Tool)
- built with flask-RESTful and flask-SQLAlchemy (Python 3.8)
- developed with the aid of Postman 

## How to Run
1. install Python 3.8+
2. activate virtual environment
3. clone repo
4. cd into folder and run 'pip install -r requirements.txt'
5. run 'flask run'
6. to demo ensure server is running at 'http://127.0.0.1:5000/'
7. [ON FIRST RUN] send a POST request to the 'http://127.0.0.1:5000/phonemes' endpoint to load phonemes.json
