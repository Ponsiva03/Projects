from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd

app = Flask(__name__)
app.secret_key = '123456' 
users = [
    {'username': 'user1', 'password': '1234'},
    {'username': 'user2', 'password': '1234'}
]


data= pd.read_csv('datas.csv')

def save_data():
    data.to_csv('datas.csv',index= False)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/insert_data',methods=['post'])
def input_details():
    global data
    name = request.form['name']
    details = request.form['details'] 

    data= data.append({'Name': name,'Details':details}, ignore_index=True)
    return f"deatils for {name} saved  successfully !"

@app.route('/display_data', methods=['GET'])
def display_details():
    name = request.args.get('name')  # Use parentheses, not square brackets
    person_details = data[data['Name'] == name]
    if not person_details.empty:
        details = person_details.iloc[0]['Details']  # Corrected variable name
    else:
        details = "Details not found for this name."
    return f"Details for {name}: {details}"

@app.route('/savedata')
def savedata():
    return render_template('Savedata.html',data=data) 

@app.route('/login',methods=['post'])
def login_user():
    username= request.form['username']
    password= request.form['password']

    for user in users:
        if user ['username']== username and user ['password']== password:
            session['username']= username
            return redirect(url_for('dashboard'))
        return" Login failed . invalied username or passwprd"
@app.route('/singup',methods=['post'])
def signup_user():
    Newusername= request.form['New username']
    Newpassword= request.form['New password']

    for user in users:
        if user['username']== Newusername:
            return"Signup failed .Username already taken.."
        user.append({'username':Newusername,'passsword':Newpassword})
        return "Signup successfully" 
    



@app.route('/delete', methods=['post'])
def delete_data():
    global data
    items_to_delete = request.form.getlist('delete_item')
    data = data[~data['Name'].isin(items_to_delete)]
    save_data()
    return redirect(url_for('savedata'))



if __name__  == '__main__':
    app.run(debug=True)
