# Gomichan REST Backend 
Serves translated subtitle lines for youtube videos with highlighted grammar and pronunciation guides.

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
7. [ON FIRST RUN] send a POST request to the 'http://127.0.0.1:5000/phonemes' to load phonemes.json
