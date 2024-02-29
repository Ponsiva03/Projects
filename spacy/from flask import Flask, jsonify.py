from flask import Flask, jsonify, request

app = Flask(__name__)

table = []

@app.route('/table', methods=['POST'])
def add_row():
    # get the JSON data from the request body
    json_data = request.get_json()

    # add the row to the table
    table.append(json_data)

    # return a success message
    return jsonify({'message': 'Row added successfully'})

if __name__ == '__main__':
    app.run()
