from flask import *
from flask_mysqldb import MySQL
import json
import MySQLdb.cursors
import re
import random
import string
from flask_cors import cross_origin
import os

app = Flask(__name__)



app.secret_key = 'your secret key'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Mydorito048187686332'
app.config['MYSQL_DB'] = 'WeatherAPIMusaib'


mysql = MySQL(app)


def checklogin():
    uID = session.get('uID')
    uEmail = session.get('uEmail')
    if not uID:
        return False, None, None  #user not loggedin
    if not uEmail:
        return False, None, None  #user not loggedin

    return True, uID, uEmail


@app.route('/portal/home', methods=['GET', 'POST'])
def portal_home():
    l, uID, uEmail = checklogin()
    if l == False:
        return redirect(url_for('login', message='Login first'))
    applications = get_applications(uID)
    #print(applications)
    return render_template('portal_home.html', applications = applications)




@app.route('/portal/createapplication', methods=['GET', 'POST'])
def portal_createapplication():
    l, userID, uEmail = checklogin()
    if l == False:
        return redirect(url_for('login', message='Login first'))

    if request.method == 'POST':
        applicationID = request.form['applicationID']
        applicationName = request.form['applicationName']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Apps WHERE appID = % s', (applicationID,))

        application = cursor.fetchone()
        if application:
            message = 'Application ID exists. This needs to be a unique identifier!'
            return render_template('portal_createapplication.html', message=message)

        #userID is got from session
        #userEmail is got from session
        cursor.execute('SELECT * FROM Apps WHERE appName = % s AND uID = % s', (applicationName, userID))
        application = cursor.fetchone()
        if application:
            message = 'Application with this name exists. Application name needs to be unique to your dashboard.'
            return render_template('portal_createapplication.html', message=message)

        elif not re.match(r'^[a-zA-Z0-9]+$', applicationID):
            message = "Invalid Application ID! It can only contain letters and digits and must not contain any symbols/spaces"
            return render_template('portal_createapplication.html', message=message)
        else:
            #create random numbers as auth tokens
            characters = string.ascii_letters + string.digits
            auth_token = ''.join(random.choice(characters) for _ in range(20))
            cursor.execute('INSERT INTO Apps VALUES (%s, %s, %s, %s, 0)', (applicationID, applicationName, auth_token, userID))
            mysql.connection.commit()
            return redirect(url_for('portal_createapplication', message='Application created successfully. Go to Dashboard to see the application details'))
    message = request.args.get('message')
    return render_template('portal_createapplication.html', message=message)




@app.route('/portal/updateprofile', methods=['GET', 'POST'])
def portal_updateprofile():
    l, uID, uEmail = checklogin()
    if l == False:
        return redirect(url_for('login', message='Login first'))
    if request.method == 'POST':
        password = request.form['password']
        newpassword = request.form['newpassword']
        confirmpassword = request.form['confirmpassword']
        print(password,newpassword,confirmpassword)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Users WHERE uID = % s AND uEmail = % s AND uPass = % s', (uID,uEmail,password))
        #print("DONE1")
        user = cursor.fetchone()
        #print(user)
        if not newpassword == confirmpassword:
            return render_template('portal_updateprofile.html', uEmail=uEmail, message="New Password and Confirm Password are not same.")
        if user:
            cursor.execute('UPDATE Users SET uPass = % s WHERE uID = % s AND uEmail = % s AND uPass = % s', (newpassword, uID, uEmail, password,))
            mysql.connection.commit()
            #print("done2")
            return render_template('portal_updateprofile.html', uEmail=uEmail,message="Password changed successfully")

        else:
            return render_template('portal_updateprofile.html', uEmail=uEmail, message="An error occurred")

    message = request.args.get('message')
    return render_template('portal_updateprofile.html', uEmail=uEmail, message=message)




@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if not re.match(r'^\w+@\w+(\.\w+)+$', email):
            message = "Invalid Email Address!"
            return render_template('login.html', message=message)


        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Users WHERE uEmail = % s', (email,))
        user = cursor.fetchone()

        #print(user.keys())
        #print(user.values())
        if user:
            #print(user['uID'])
            session['uID'] = user['uID']
            session['uEmail'] = user['uEmail']
            return redirect(url_for('portal_home'))
        else:
            return render_template('login.html', message='Email and/or password mismatch!')

    message = request.args.get('message')
    return render_template('login.html', message=message)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Users WHERE uEmail = % s', (email,))
        account = cursor.fetchone()
        if account:
            message = 'Account already exists !'
            return render_template('signup.html', message=message)
        elif not re.match(r'^\w+@\w+(\.\w+)+$', email):
            message = "Invalid Email Address!"
            return render_template('signup.html', message=message)
        else:
            cursor.execute('INSERT INTO Users VALUES (NULL, %s, %s)',(email, password))
            mysql.connection.commit()
            return redirect(url_for('login', message='Account created successfully. Please login now'))
        
        
        # Check if the username or email already exists in the database
        #if User.query.filter_by(email=email).first() is not None:
        #    return render_template('signup.html', message='Email already exists')

        # Create a new user
        #new_user = User(email=email, password=password)
        #db.session.add(new_user)
        #db.session.commit()


    return render_template('signup.html')


@app.route('/static/<path:path>')
def serve_static(path):
    return app.send_static_file(path)


@app.route('/logout', methods=['GET','POST'])
def logout():
    session.clear()
    return redirect(url_for('login', message="Logged out successfully") )

def get_applications(uID):
    l, uID, uEmail = checklogin()
    if l == False:
        return redirect(url_for('login', message='Login first'))

    if request.method == 'GET':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Apps WHERE uID = % s', (uID,))

        applications = cursor.fetchall()
        return applications



@app.route('/applications/<appID>', methods=['DELETE'])
def delete_application(appID):
        l, uID, uEmail = checklogin()
        if l == False:
            return redirect(url_for('login', message='Login first'))

        if request.method == 'DELETE':
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM Apps WHERE uID = % s AND appID = % s', (uID,appID,))
            applications = cursor.fetchone()
            #print(applications)
            jsonreturn = dict()
            if applications:
                cursor.execute('DELETE FROM Apps WHERE uID = % s AND appID = % s', (uID, appID,))
                jsonreturn['success'] = 'true'
                mysql.connection.commit()
                cursor.close()
                return app.response_class(response=json.dumps(jsonreturn), status=200, mimetype='application/json')
            else:
                jsonreturn['success'] = 'false'
                return app.response_class(response=json.dumps(jsonreturn), status=404, mimetype='application/json')

            # Close cursor


# @app.route('/applications2', methods=['GET'])
# def get_applications2():
#     if request.method == 'GET':
#         applications = [{'id': 1, 'name': 'App 1', 'accesstoken': '1-12121212'}, {'id': 2, 'name': 'App 2', 'accesstoken': '2-12121212'}, {'id': 2,'name': 'App 2','accesstoken': '3-12121212'}]
#         return app.response_class(response=json.dumps(applications), status=200, mimetype='application/json')


### API CALLS FROM HERE
from datetime import datetime, date, timedelta
import pandas as pd


CSV_PATH="C:/Users/musai/OneDrive/Desktop/New folder/weather data"  #CHANGE PATH IF YOU HAVE NEW DATA AN DCONVERT BACK SLAHES TO FORWARD SLASHES
#OWN DATA
csvs = os.listdir(CSV_PATH)
csvdata = dict()

for csv in csvs:
    print(csv)
    csvdata[csv.split(".csv")[0]] = pd.read_csv(CSV_PATH+"/"+csv)


basic_cols = ['YEAR', 'DOY'] 
columns_temperature = ['T2M', 'TS', 'T2M_MAX', 'T2M_MIN']
columns_rainfall = ['QV2M', 'RH2M', 'PRECTOTCORR']
columns_wind =  ['WS2M_MAX', 'WS2M_MIN']

def get_day_of_year(date_str):  #because in CSV, the date is not in DD-MM-YYYY format so we need to convert the input date given by user to its number of day of the year ranging from 1-365
    # Convert the date string to a datetime object
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    # Get the year
    year = date_obj.year
    # Get the day of the year (1-based index)
    day_of_year = date_obj.timetuple().tm_yday 
    return year, day_of_year

def getdistrictdata(str):
    if str in csvdata.keys():
        return csvdata[str]
    else:
        return None


NUM_ALLOWED_REQUESTS = 100
@app.route('/api/v1', methods=['POST'])
@cross_origin()
def fetchWeather():
    flag = "" #kept for keeping track of errors
    data_from_user = request.json
    if True:
        try:
            inputDate = data_from_user['date']
            inputdistrict = data_from_user['district']
            appId = data_from_user['appID']
            authToken = data_from_user['authToken']
            prediction = data_from_user['prediction']
            temperature = data_from_user['temperature']
            #print(temperature)
            wind = data_from_user['wind']
            #print(wind)
            rainfall = data_from_user['rainfall']
            #print(rainfall)
            #print(data_from_user)
            #print(appId)

            #check begin
            #first we check the appID, authToken
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM Apps WHERE appID = % s AND appAccessToken = % s', (appId,authToken,))
            application = cursor.fetchone()
            if not application:
                flag = " App-ID and/or Access-Token details are incorrect."
            if application:
                #print("yes")
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('SELECT SUM(requests) AS totalrequests FROM Apps WHERE uID = (SELECT uID FROM Apps WHERE appID = % s) ', (appId,))
                totalreq = cursor.fetchone()
                #print(requests['totalrequests'])
                print(int(totalreq['totalrequests']) )
                if int(totalreq['totalrequests']) >= NUM_ALLOWED_REQUESTS:
                    #print("stop the user from making more requests")
                    flag += " User has exhausted quota of Maximum allowed API Requests."
                  
            #then check the date
            if inputDate == "":
                flag += " Input date is not valid."
            
            #then we check the district
            if inputdistrict not in csvdata.keys():
                flag += " District name is not valid."
            
            params_to_send = dict()
            
            #then we filter what columns the user wants like temperature, wind, or rinfall or two or all of them
            columns = basic_cols.copy()
            if temperature == True:
                params_to_send['temperature'] = True
                columns += columns_temperature
            if wind==True:
                params_to_send['wind'] = True
                columns += columns_wind
            if rainfall==True:
                params_to_send['rainfall'] = True
                columns += columns_rainfall
            #print(columns)
            if not temperature and not wind and not rainfall:
                flag += " You need to select either temperature, or wind or rainfall data."
            

            inputyear, day_of_the_year = get_day_of_year(inputDate)
            #print(day_of_the_year)
            data_of_district = csvdata[inputdistrict]
            fetched_data = data_of_district[(data_of_district.YEAR==int(inputyear)) & (data_of_district.DOY==int(day_of_the_year))]
            data_to_return = fetched_data[columns]
            data_to_return['DOY'] =inputDate
            #print(inputyear, fetched_data)
            
            if fetched_data.shape[0] ==0:
                flag = " Data is not present for the selected date."
                data_to_return = fetched_data[columns]

            if flag == "": 
                #means no errors were found in the input data
                #add to users requesiting quota
                cursor.execute('UPDATE Apps SET requests = requests + 1 WHERE appID = % s AND appAccessToken = % s', (appId, authToken,))
                mysql.connection.commit()
                cursor.close()


                response_data = {"status": "success","message": json.dumps(params_to_send),"data": data_to_return.to_json(orient='records')}
                response = app.response_class(response=json.dumps(response_data),status=200,mimetype='application/json')
                response.headers.add('Content-type','application/json')
                return response
            else:
                response_data = {"status": "fail","message": flag, "data_received": request.json }
                response = app.response_class(response=json.dumps(response_data),status=400,mimetype='application/json')
                response.headers.add('Content-type','application/json')
                return response


        except Exception as e:
            print(e)
            response_data = {"status": "fail","message": str(e),"received_data": request.json }
            response = app.response_class(response=json.dumps(response_data),status=400,mimetype='application/json')
            response.headers.add('Content-type','application/json')
            return response





# @app.route('/api/v1', methods=['POST'])
# @cross_origin()
# def process_data():
#     # Get the JSON data from the request
#     json_data = request.json
#     data_from_user = json.loads(request.json)
#     return "1"



    

# #     # Print the received data to the console
# #     print('Received JSON data:', json_data)

# #     # Do something with the JSON data
# #     # ...

# #     return 'Data received successfully'

if __name__ == '__main__':
    app.run(debug=True)
