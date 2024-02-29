from fileinput import filename
from multiprocessing import current_process
from tabnanny import filename_only
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin
import json
import pandas as pd
from collections import Counter
import os
import pdfkit  
from jinja2 import Template
import datetime

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
api = Api(app)


def get_values(lst, key):
    result = []
    for dictionary in lst:
        if key in dictionary:
            result.append(dictionary[key])
    return result


def Average(lst):
    sum_of_list = 0
    for i in range(len(lst)):
        if str(lst[i]).isdigit():
            sum_of_list += int(lst[i])
        else:
            sum_of_list += 0
    average = sum_of_list / len(lst)
    return round(average, 2)


@app.route('/', methods=['GET', 'POST'])
class Json_to_pdf(Resource):
    @cross_origin()
    def post(self):
        # Extract JSON data from the POST request
        data = request.get_json()

        #
        # data_file = pd.read_json(file_name + '.json')
        # with the provided JSON data
        data_file = pd.DataFrame(data)

        data_file = data_file.fillna('')
        col_name = []
        for cols in data_file.columns:
            col_name.append(cols)

           
 
            data_file = data_file.fillna('')
            col_name = []
            for cols in data_file.columns:
                col_name.append(cols)

            df1 = pd.DataFrame(columns=['Index info', 'alarm info', 'other data'])
            
            df1['Index info'] = data_file[0]
            df1['alarm info'] = data_file[1]
            df1 = df1.join(df1['Index info'].apply(pd.Series))
            df1 = df1.drop(0, axis=1)
            df1 = df1.join(df1['alarm info'].apply(pd.Series))
            df1 = df1.drop(0, axis=1)
            df1 = df1.drop('Index info', axis=1)
            df1 = df1.drop('alarm info', axis=1)

            for i in range(0, len(data_file)):
                final_res_data = []
                dict_list = []
                for j in range(2, len(col_name)):
                    if data_file[j][i] != '':
                        dict_list.append(data_file[j][i])

                new_list = []
                for l in dict_list:
                    for j in l:
                        new_list.append(j)
                uniq = Counter(new_list)
                uniq_key = list(uniq.keys())

                res_data = []
                final_res_data = []
                for k in range(0, len(uniq_key)):
                    res_all = get_values(dict_list, uniq_key[k])
                    res = [s for s in res_all if str(s).isdigit()]
                    res_str = list(set(res_all) - set(res))
                    if res:
                        min_res = min(res, key=float)
                        max_res = max(res, key=float)
                        avg_res = Average(res)
                    else:
                        min_res = ''
                        max_res = res_str
                        avg_res = ''
                    res_data.append(uniq_key[k] + '|' + str(min_res) + '|' + str(max_res) + '|' + str(avg_res))
                df1.at[i, 'other data'] = res_data
            df1 = df1.iloc[:-1, :]
            df1.to_csv('process_1.csv', index=False)
            print(df1)
            df1 = df1.explode('other data')
            df1.to_csv('process.csv', index=False)
            df2 = pd.read_csv('process.csv')
            df2 = df2.explode('other data')
            df2[['Parameter', 'MIN', 'MAX', 'AVG']] = df2['other data'].astype(str).str.split('|', n=3, expand=True)
            df2 = df2.drop('other data', axis=1)
            df2 = df2.fillna(0)
            df2['component_id'] = df2['component_id'].astype(str)
            df2['current_machine_id'] = df2['current_machine_id'].astype(int)
            df2['current_process_id'] = df2['current_process_id'].astype(int)
            df2['alarm_no'] = df2['alarm_no'].astype(int)
            df2['alarm_type'] = df2['alarm_type'].astype(int)
            for i in range(0, len(df2)):
                if df2['Parameter'][i] == 'time':
                    df2.at[i, 'MIN'] = datetime.datetime.fromtimestamp(int(df2['MIN'][i])).strftime('%Y-%m-%d %H:%M:%S')
                    df2.at[i, 'MAX'] = datetime.datetime.fromtimestamp(int(df2['MAX'][i])).strftime('%Y-%m-%d %H:%M:%S')

            for i in range(0, len(df2)):
                if df2['MIN'][i] == df2['MAX'][i]:
                    df2.at[i, 'MIN'] = ''
                    df2.at[i, 'AVG'] = ''

            df2['merged'] = df2.apply(lambda x: list([x['Parameter'], x['MIN'], x['MAX'], x['AVG']]), axis=1)
            df2 = df2.groupby(['component_id', 'current_machine_id', 'current_process_id', 'alarm_no',
                               'alarm_type', 'alarm_message', 'component_status'])['merged'].apply(list).reset_index()
            df2['list_len'] = df2['merged'].str.len()
            df2.to_csv('final.csv', index=False)

            otherlen = []
            df3 = pd.read_csv('process_1.csv', converters={'component_id': str})
            df3 = df3.sort_values('current_machine_id')
            print(df3)
            col_name = df1.columns
            df1_len = len(df3)
            df2_len = len(df2)
            component = str(df3['component_id'][0])
            status = df3['component_status'][0]
            machine = df3['current_machine_id'].tolist()
            process = df3['current_process_id'].tolist()
            alarmno = df3['alarm_no'].tolist()
            alarmtype = df3['alarm_type'].tolist()
            alarmmsg = df3['alarm_message'].tolist()
            compstatus = df3['component_status'].tolist()
            other = df3['other data'].tolist()
            mergedata = df2['merged']
            mergelen = df2['list_len'].tolist()

            HTML = '''
            <style>
            table, th, td {
              border: 2px solid black;
              border-collapse: collapse;
            }
            </style>

            <table border="1" width="100%">
                <tr>
                   <th style="width:25%">Component ID</th>
                   <td style="width:25%">{{component}}</td>
                   <th style="width:25%">Overall Status</th>
                   <td style="width:25%">{{status}}</td>
                </tr>
                {% for j in range(0, mergelen[0]) %}
                <tr>
                    {% if mergedata[0][j][0] == 'time' %}
                        <th style="width:25%">Overall Start Time</th>
                        <td style="width:25%">{{mergedata[0][j][1].format('MMMM Do YYYY, h:mm:ss a')}}</td>
                        <th style="width:25%">Overall End Time</th>
                        <td style="width:25%">{{mergedata[0][j][2].format('MMMM Do YYYY, h:mm:ss a')}}</td>
                    {% endif %}
                </tr>
                {% endfor %}
            </table>
            <br><br>
            {% for i in range(0, df1_len) %}
            <table border="1" width="100%">
                <tr>
                   <th style="width:25%">Current Process ID</th>
                   <td style="width:25%">{{process[i]}}</td>
                   <th style="width:25%">Current Machine ID</th>
                   <td style="width:25%">{{machine[i]}}</td>
                </tr>
                {% for j in range(0, mergelen[i]) %}
                <tr>
                    {% if mergedata[i][j][0] == 'time' %}
                        <th style="width:25%">Start Time</th>
                        <td style="width:25%">{{mergedata[i][j][1].format('MMMM Do YYYY, h:mm:ss a')}}</td>
                        <th style="width:25%">End Time</th>
                        <td style="width:25%">{{mergedata[i][j][2].format('MMMM Do YYYY, h:mm:ss a')}}</td>
                    {% endif %}
                </tr>
                {% endfor %}
            </table>
            <br><br>
            <table border="1" width="50%">
                <tr>
                   <th style="width:25%">Parameter</th>
                   <th style="width:25%">Value</th>
                </tr>
                <tr>
                   <th style="width:25%">Alarm NO</th>
                   <td style="width:25%">{{alarmno[i]}}</td>
                </tr>
                <tr>
                   <th style="width:25%">Alarm Type</th>
                   <td style="width:25%">{{alarmtype[i]}}</td>
                </tr>
                <tr>
                   <th style="width:25%">Alarm Message</th>
                   <td v>{{alarmmsg[i]}}</td>
                </tr>
                <tr>
                   <th style="width:25%">Component Status</th>
                   <td style="width:25%">{{compstatus[i]}}</td>
                </tr>
                {% for j in range(0, mergelen[i]) %}
                <tr>
                    {% if mergedata[i][j][1] == '' %}
                        <th style="width:25% ; text-align: center">{{mergedata[i][j][0]}}</th>
                        <td style="width:25%">{{mergedata[i][j][2]|replace("['","") | replace("']","")}}</td>
                    {% endif %}
                </tr>
                {% endfor %}
            </table>
            <br><br>
            <table border="1" width="100%">
                <tr>
                   <th style="width:25%">Parameter</th>
                   <th style="width:25%">MIN</th>
                   <th style="width:25%">MAX</th>
                   <th style="width:25%">AVG</th>
                </tr>
                {% for j in range(0, mergelen[i]) %}
                <tr>
                    {% if mergedata[i][j][1] != '' and mergedata[i][j][0] != 'time' %}
                        <th style="width:25%">{{mergedata[i][j][0]}}</th>
                        <td style="width:25%">{{mergedata[i][j][1]}}</td>
                        <td style="width:25%">{{mergedata[i][j][2]}}</td>
                        <td style="width:25%">{{mergedata[i][j][3]}}</td>
                    {% endif %}
                </tr>
                {% endfor %}
            </table>
            <br><br><br><br>

            {% endfor %}
            '''

            template = Template(HTML)
            res = template.render(col_name=col_name, df1_len=df1_len, df2_len=df2_len, component=component,
                                  status=status, machine=machine, process=process, alarmno=alarmno, alarmtype=alarmtype,
                                  alarmmsg=alarmmsg, compstatus=compstatus, other=other, mergedata=mergedata,
                                  mergelen=mergelen)

            text_file = open("index.html", "w")
            text_file.write(res)
            text_file.close()
            path = os.path.abspath('index.html')
            # specific_process_id = process[0]
            pdf_filename = f"{component}_.pdf"
            pdfkit.from_file(path, pdf_filename)

            resultJson = {}
            resultJson['result'] = 'pdf generated successfully'
            strResJson = json.dumps(resultJson)
            return json.loads(strResJson)


      

   


api.add_resource(Json_to_pdf, '/json_to_pdf')








if __name__ == '__main__':
    app.run(host= '192.168.1.146',port=5000)
