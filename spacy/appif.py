from flask import Flask, jsonify, request
import csv

app = Flask(__name__)

@app.route('/resolution', methods=['POST'])
def get_resolution():
    data = request.get_json()
    model = data['Model']
    serial_prefix = data['serial prefix']
    smcs = data['SMCS']
    problem = data['Problem']
    
    with open(r'C:\Users\ponsi\Downloads\Table.csv','r') as file:
        reader = csv.DictReader(file)  
        for row in reader:
            if (row['Model'] == model and 
                row['serial prefix'] == serial_prefix and 
                row['SMCS'] == smcs and 
                row['Problem'] == problem):
                
                return jsonify({'Resolution path': row['Resolution path'], 'Resolution': row['Resolution']})
                
    return jsonify({'Error': 'Resolution not found'})

if __name__ == '__main__':
    app.run(debug=True)
