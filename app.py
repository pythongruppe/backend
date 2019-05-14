from flask import Flask, request
from Memory import input_to_database

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        #assumed request.data is json with proper formatting / attributes NO checking atm.
        return input_to_database(request.data)
    return 'Hello World!'


#@app.route('/getAllIds', methods=['GET'])
#def show_ids():
    #return house_ids()


if __name__ == '__main__':
    app.run()


#check i can get data
#check i can read to file
#check i will not read to file if already exists
#create unit tests for this
#refactor methods in memory.py into smaller methods