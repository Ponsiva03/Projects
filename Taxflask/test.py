from flask import Flask,request, render_template, current_app, send_file, jsonify
from fileinput import filename
import pandas as pd
import numpy as np
import os
pd.options.mode.chained_assignment = None
import requests
import json
from urllib.request import urlopen , Request
from bs4 import BeautifulSoup
import openai 

app = Flask(__name__)

# @app.route('/')
# def index_new():
#     return render_template('index.html')


@app.route('/')
def index_new():
    #df = pd.read_excel('Schema with data types.xlsx')
    df = pd.read_excel('set2_sample_data.xlsx')
    end_node = df[['End Node']].value_counts().reset_index(name='counts')
    return render_template('index_2.html',cl_name=end_node['End Node'])


@app.route('/select_column', methods = ['POST'])  
def select_column(): 
    if request.method == 'POST': 
        #df = pd.read_excel('Schema with data types.xlsx')
        df = pd.read_excel('set2_sample_data.xlsx')
        end_node = df[['End Node']].value_counts().reset_index(name='counts')
        endnode = request.form.get("c_name")
        entity_dictionary = {"var_name":'' ,"type":'',"description":'' }
        entity_list = []
        attr = []
        match_tax = ''
        for i in range(0,len(df)):
            if df['End Node'][i] == endnode:
                match_tax = df['Taxonomy'][i]
                entity_dictionary['var_name'] = df['Variable_Type'][i]
                entity_dictionary['type'] = df['Data Type'][i]
                entity_dictionary['description'] = df['Attribute'][i]
                entity_list.append(entity_dictionary)
                attr.append(df['Attribute'][i])
                entity_dictionary = {"var_name":'' ,"type":'',"description":'' }
        
        #print(match_tax)
        return render_template('index_2.html',cl_name=end_node['End Node'],col_name=endnode,entity_list=entity_list,attr_list=attr,match_tax=match_tax)

@app.route('/fetch_from_url', methods = ['POST'])
def fetch_from_url():
    urlValue = request.get_json()
    url = urlValue["fetchUrl"]
    #print(url)
    #url = input('Please enter the URL :')
    req = Request(
        url=url, 
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    html = urlopen(req).read()
    soup = BeautifulSoup(html, features="html.parser")
    # kill all script and style elements
    # for script in soup(["script", "style",]):
    #     script.extract()    # rip it out
    header = soup.find('header')
    # Remove header element
    if header:
        header.decompose()
    # Find footer element
    footer = soup.find('footer')
    # Remove footer element
    if footer:
        footer.decompose()
    #text = soup.get_text()
    text = soup.prettify()
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)


    #print(text)
    #print('completed')

    fetch_result = {'fetchValue': text}
    return jsonify(fetch_result)


@app.route('/fetched_info', methods = ['POST'])
def fetched_info():
    fetchValue = request.get_json()
    endnode = fetchValue["endNode"]
    url = fetchValue["fetchUrl"]
    selected_val = fetchValue["selText"]
    selected_schema = fetchValue["selSchema"]
    df1 = pd.read_csv('fetched_data.csv')
    df2 = [[endnode,url,selected_schema,selected_val]]
    df3 = pd.DataFrame(df2,columns=['end node','URL','attribute_name','attribute_val'])
    df4 = pd.concat([df1,df3],ignore_index=True)
    print(df4)
    df4.to_csv('fetched_data.csv',index= False)
    

    map_result = {'result': "Success"}
    return map_result


@app.route('/gpt_sugg', methods = ['POST','GET'])
def gpt_sugg():
    if request.method == 'POST': 
        fetchValue = request.get_json()
        selected_val = fetchValue["selText"]
        openai.api_key =  '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'
    
        response_grantor = openai.Completion.create(
                engine="text-davinci-003",
                prompt = f'Suggest one suitable attribute name for {selected_val}. Return only attribute name',            
                temperature=1.0,
                max_tokens=300,
                n=1,
                stop=None
            )

        output_data = response_grantor.choices[0].text

    if request.method == 'GET': 
        # resArg = request.args.get(0)
        # print('result argument : ' + resArg)
        #fetchValue = json.loads(resArg)
        fetchValue = request.get_json()
        selected_val = fetchValue["selText"]
        openai.api_key =  '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'

        response_grantor = openai.Completion.create(
                engine="text-davinci-003",
                prompt = f'Suggest one suitable attribute name for {selected_val}. Return only attribute name',            
                temperature=1.0,
                max_tokens=300,
                n=1,
                stop=None
            )

        output_data = response_grantor.choices[0].text

    #output_data = 'test output'
    gpt_res = {'result': output_data}
    return gpt_res

if __name__ == "__main__":
    app.run(debug=True)