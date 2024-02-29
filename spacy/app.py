from flask import Flask, jsonify

app = Flask(__name__)

table = [
    {
        'Model': '120k 2',
        'serial prefix': 'SZS',
        'SMCS': '1251',
        'Problem': '19',
        'Resolution path': 'A',
        'Resolution': ['Test', 'Test1', 'Test 2']
    },
    {
        'Model': '120k 2',
        'serial prefix': 'SZS',
        'SMCS': '1251',
        'Problem': '19',
        'Resolution path': 'B',
        'Resolution': ['Test3', 'Test4', 'Test5']
    },
    {
        'Model': '120k 2',
        'serial prefix': 'SZS',
        'SMCS': '1251',
        'Problem': '19',
        'Resolution path': 'C',
        'Resolution': ['Test6', 'Test7']
    },
    {
        'Model': '950L',
        'serial prefix': 'LXX',
        'SMCS': '1011',
        'Problem': '17',
        'Resolution path': 'A',
        'Resolution': ['Test', 'Test1']
    },
    {
        'Model': '120K',
        'serial prefix': 'JAP',
        'SMCS': '1231',
        'Problem': '20',
        'Resolution path': 'A',
        'Resolution': ['Test', 'Test1', 'Test2']
    },
    {
        'Model': '120K',
        'serial prefix': 'JAP',
        'SMCS': '1231',
        'Problem': '20',
        'Resolution path': 'B',
        'Resolution': ['Test3', 'Test4', 'Test5']
    }
]

@app.route('/table')
def get_table():
    return jsonify(table)

if __name__ == '__main__':
    app.run()
