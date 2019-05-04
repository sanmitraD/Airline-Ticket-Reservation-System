#Importing the necessary dependencies
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import datetime
#configuring the app
app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'mydatabase'
app.config['MONGO_URI'] = '<<MONGO_URI fill it with your credentials>>'
app.config['SECRET_KEY'] = '<<SECRET_KEY>>'

#User class for user login system
class User():
	def __init__(self, username):
		self.username = username
		self.email = username

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return self.username

	def validate_login(password_hash, password):
		return check_password_hash(password_hash, password)

#starting the mongoDB database
mongo = PyMongo(app)

#staring the login manager
login_manager = LoginManager()
login_manager.init_app(app)

#required data for using in various pages
citycodemapping = {'Agartala': 'IXA',
 'Agatti Island': 'AGX',
 'Agra': 'AGR',
 'Ahmedabad': 'AMD',
 'Aizawl': 'AJL',
 'Allahabad ': 'IXD',
 'Amritsar ': 'ATQ',
 'Andhra Pradesh ': 'TIR',
 'Assam': 'TEZ',
 'Assam ': 'DIB',
 'Auranagabad': 'IXU',
 'Bangalore ': 'BLR',
 'Bathinda': 'BUP',
 'Bhavnagar ': 'BHU',
 'Bhopal ': 'BHO',
 'Bhuj': 'BHJ',
 'Bhuntar': 'KUU',
 'Bihar ': 'GAY',
 'Bikaner ': 'BKB',
 'Chandigarh ': 'IXC',
 'Chennai ': 'MAA',
 'Chhattisgarh': 'RPR',
 'Coimbatore ': 'CJB',
 'Dehradun ': 'DED',
 'Delhi ': 'DEL',
 'Dimapur ': 'DMU',
 'Diu ': 'DIU',
 'Goa': 'GOI',
 'Gorakhpur': 'GOP',
 'Gujarat ': 'IXY',
 'Guwahati ': 'GAU',
 'Hyderabad ': 'HYD',
 'Indore': 'IDR',
 'Jaipur ': 'JAI',
 'Jaisalmer ': 'JSA',
 'Jammu': 'IXJ',
 'Jamnagar ': 'JGA',
 'Jodhpur ': 'JDH',
 'Jorhat': 'JRH',
 'Jubbarhatti': 'SLV',
 'Kadapa': 'CDP',
 'Kangra ': 'DHM',
 'Kanpur': 'KNU',
 'Karipur': 'CCJ',
 'Karnataka ': 'MYQ',
 'Kattalangulam': 'TCR',
 'Khajuraho ': 'HJR',
 'Kochi': 'COK',
 'Kolkata ': 'CCU',
 'Leh': 'IXL',
 'Lucknow': 'LKO',
 'Madhurapundi': 'RJA',
 'Madhya Pradesh ': 'JLR',
 'Maharashtra': 'SAG',
 'Maharashtra ': 'NDC',
 'Manipur ': 'IMF',
 'Mexico ': 'TCN',
 'Mumbai ': 'BOM',
 'Nagpur': 'NAG',
 'Odisha ': 'BBI',
 'Paro': 'PBD',
 'Patna': 'PAT',
 'Pondicherry ': 'PNY',
 'Port Blair ': 'IXZ',
 'Pune': 'PNQ',
 'Punjab': 'IXP',
 'Punjab ': 'LUH',
 'Rajkot': 'RAJ',
 'Ranchi': 'IXR',
 'Sambra ': 'IXG',
 'Srinagar ': 'SXR',
 'Surat': 'STV',
 'Tamil naidu': 'IXM',
 'Temail naidu ': 'TRZ',
 'Toranagallu': 'VDY',
 'Triruvanthapuram': 'TRV',
 'Udaipur': 'UDR',
 'Ujjalpur': 'IXI',
 'Umroi': 'SHL',
 'Uttarakhand': 'PGH',
 'Vadodara': 'BDQ',
 'Varanasi': 'VNS',
 'Vijayawada': 'VGA',
 'Visakhapatnam': 'VTZ',
 'West Bengal ': 'IXB'}
cities = list(citycodemapping.keys())

airlinecodemapping = {'2T':'Trujet',
                 '6E':'IndiGo',
                 '9I':'Alliance Air',
                 '9W':'Jet Airways',
                 'AI':'Air India',
                 'G8':'GoAir',
                 'I5':'AirAsia India',
                 'LB':'AirCosta',
                 'S2':'JetLite',
                 'SG':'Spicejet',
                 'UK':'Vistara'}
airlines = list(airlinecodemapping.values())
codeairlinemapping = {v:k for k,v in airlinecodemapping.items()}
codecitymapping = {v:k for k,v in citycodemapping.items()}

#LoginForm class for Login system created using wtforms
class LoginForm(FlaskForm):
	username = StringField('User Name',  validators=[InputRequired()])
	password = PasswordField('Password', validators = [InputRequired()])
	remember = BooleanField('remember me')

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

#handling login request at "/login"
@app.route('/login', methods=['GET','POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		UserLogin = mongo.db.UserLogin
		email = form.username.data
		hash = UserLogin.find_one(email)
		if hash == None:
			return render_template('login.html', form=form, failed=True)
		hash = hash['PasswordHash']
		if check_password_hash(hash, form.password.data):
			user_obj = User(email)
			login_user(user_obj, remember=form.remember.data)
		else:
			return render_template('login.html', form=form, failed=True)
		return redirect('/')
	return render_template('login.html', form=form)

#handling logout request at "/logout"
@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect('/')

#registration form
@app.route('/register', methods=['GET','POST'])
def registerNow():
	if request.method == 'POST':
		FullName = request.form.get('FullName')
		DOB =  request.form.get('DateOfBirth')
		Email =  request.form.get('Email')
		PhoneNumber = request.form.get('PhoneNumber')
		Gender = request.form.get('Gender')
		Address = request.form.get('Address')
		Password = request.form.get('Password')
		Person = {
		'_id': Email,
		'FullName': FullName,
		'DateOfBirth': DOB,
		'PhoneNumber': PhoneNumber,
		'Gender' : Gender,
		'Address' : Address
		}
		UserData = mongo.db.UserData
		UserLogin = mongo.db.UserLogin
		UserPerson = {
		"_id":Email,
		"PasswordHash": generate_password_hash(Password)
		}
		try:
			UserData.insert_one(Person)
			UserLogin.insert_one(UserPerson)
		except DuplicateKeyError:
			print('User already exist')
		return redirect('/')
	return render_template('register.html')

#homepage request handling
@app.route('/', methods=['GET','POST'])
def print_list():
    date = datetime.datetime.now()
    end_date = date+ datetime.timedelta(days = 60)
    min_d = str(date.year)+'-'+str(date.month).rjust(2,'0')+'-'+str(date.day).rjust(2,'0')
    max_d = str(end_date.year)+'-'+str(end_date.month).rjust(2,'0')+'-'+str(end_date.day).rjust(2,'0')
    form = LoginForm()
    if request.method == 'POST':
        name = current_user.username
    return render_template('index.html',mindate=min_d,maxdate=max_d, cities = cities, form=form, failed=False)

#handling list of files available
@app.route('/flights_res', methods=['GET','POST'])
def flight_res():
    if request.method == 'POST':
        SOURCE = request.form.get('source')
        DEST = request.form.get('dest')
        DATE = request.form.get('DateOfJourney')
        Seats = request.form.get('NoOfPassengers')
        Y = int(DATE[:4])
        M = int(DATE[5:7])
        D = int(DATE[8:11])
        day = int(datetime.date(Y,M,D).weekday()+1)
        source_code = citycodemapping[SOURCE]
        destination_code = citycodemapping[DEST]
        airlineDB = mongo.db.airlineDB
        flighttrans = mongo.db.flighttrans
        res = airlineDB.find({'SOURCE':source_code, "DESTINATION":destination_code, 'DAYS': day})
        available_flights = []
        for i in res:
            flightNow = {}
            flightNow['AIRLINE_CODE'] = airlinecodemapping[i['AIRLINE_CODE']]
            #CONVERTING NUMBER TO TIME
            dtime = str(i['DEPARTURE_TIME']).rjust(4,'0')
            min = dtime[-2:]
            hrs = dtime[:-2]
            dtime = hrs+':'+min
            flightNow['DEPARTURE_TIME'] = dtime
            atime = str(i['ARRIVAL_TIME']).rjust(4,'0')
            min = atime[-2:]
            hrs = atime[:-2]
            atime = hrs+':'+min
            flightNow['ARRIVAL_TIME'] = atime
            flightNow['FARE'] = i['FARE']
            flightNow['COMPLETE_FLIGHT_NUMBER'] = i['COMPLETE_FLIGHT_NUMBER']
            flighttrans_id = DATE+i['COMPLETE_FLIGHT_NUMBER']
            fli = flighttrans.find_one({'_id':flighttrans_id})
            if fli:
                flightNow['NoOfSeats'] = fli['NoOfSeats']
            else:
                flightNow['NoOfSeats'] = 60
            available_flights.append(flightNow)
    return render_template('flights_res.html',n=Seats, cities=cities, flights = available_flights, date = DATE)

#hadling the request on selecting the flight
@app.route('/confirm', methods=['GET', 'POST'])
#@login_required
def confirmNow():

    if request.method == 'POST' and current_user.is_authenticated:
        Number = request.form.get('FlightNumber')
        Date = request.form.get('Date')
        seats = request.form.get('Seats')
        flighttrans = mongo.db.flighttrans
        strn  = Date+Number
        fli = flighttrans.find_one({'_id':strn})
        if not fli:
            flighttrans.insert_one({'_id':strn,'NoOfSeats': 60, 'Passengers':[]})
        airlineDB = mongo.db.airlineDB
        UserData = mongo.db.UserData

        user = UserData.find_one({'_id':current_user.username})
        data = airlineDB.find_one({'COMPLETE_FLIGHT_NUMBER': Number})
        AirlineCode = airlinecodemapping[data['AIRLINE_CODE']]
        dtime = str(data['DEPARTURE_TIME']).rjust(4,'0')
        mins = dtime[-2:]
        hrs = dtime[:-2]
        dtime = hrs+':'+mins
        atime = str(data['ARRIVAL_TIME']).rjust(4,'0')
        mins = atime[-2:]
        hrs = atime[:-2]
        atime = hrs+':'+mins
        ArrivalTime = atime
        DepartureTime = dtime
        Destination = codecitymapping[data['DESTINATION']]
        Source = codecitymapping[data['SOURCE']]
        Fare = data['FARE']
        FlightNumber = data['FLIGHT_NUMBER']
        FullName = user['FullName']
        PhoneNumber = user['PhoneNumber']
        toUserDb = {}
        toUserDb['SOURCE'] = data['SOURCE']
        toUserDb['DESTINATION'] = data['DESTINATION']

        passenger={'FullName':FullName,
                    'PhoneNumber':PhoneNumber}
        flight = {'COMPLETE_FLIGHT_NUMBER':Number,
                    'SOURCE_CODE':data['SOURCE'],
                    'DESTINATION_CODE':data['DESTINATION'],
                    'FLIGHT_NUMBER':FlightNumber,
                    'AIRLINE_CODE':AirlineCode,
                    'ARRIVAL_TIME': ArrivalTime,
                    'DEPARTURE_TIME': DepartureTime,
                    'SOURCE':Source,
                    'DESTINATION':Destination,
                    'FARE':Fare
                    }
        print(flight)

        return render_template('Confirm.html',n=int(seats),date = Date,fare = Fare,flight=flight,passenger=passenger)
        return "<h1>"+Number + "</h1>"
    return redirect('/login')

@app.route('/ConfirmBooking', methods=['GET','POST'])
def ConfirmBooking():
    if request.method == 'POST' :
        passengers = []
        n = int(request.form.get('Seats'))
        for i in range(1,n+1):
            FullName = request.form.get("FullName"+str(i))
            Age = request.form.get('Age'+str(i))
            Gender = request.form.get('Gender'+str(i))
            passengers.append({'FullName':FullName,'Age':Age,'Gender':Gender})
        print(passengers)
        PhoneNumber = request.form.get('PhoneNumber')
        completeNumber = request.form.get('completeNumber')
        BookingDate = request.form.get('BookingDate')
        flighttrans_id = BookingDate+completeNumber
        airlineDB = mongo.db.airlineDB
        UserData = mongo.db.UserData
        userTrans = mongo.db.UserTransactions
        flighttrans = mongo.db.flighttrans
        PNR = mongo.db.PNR
        TICKETS = mongo.db.TICKETS
        UserTransaction = userTrans.find_one({'_id':current_user.username})
        if not UserTransaction:
            userTrans.insert_one({'_id':current_user.username,'TICKETS':[]})
            UserTransaction = userTrans.find_one({'_id':current_user.username})
        pnr = PNR.update_one({ "_id" : "PNR" },{ '$inc': { "PNR" : 1 } });

        data = airlineDB.find_one({'COMPLETE_FLIGHT_NUMBER': completeNumber})
        AirlineCode = airlinecodemapping[data['AIRLINE_CODE']]
        dtime = str(data['DEPARTURE_TIME']).rjust(4,'0')
        mins = dtime[-2:]
        hrs = dtime[:-2]
        dtime = hrs+':'+mins
        atime = str(data['ARRIVAL_TIME']).rjust(4,'0')
        mins = atime[-2:]
        hrs = atime[:-2]
        atime = hrs+':'+mins
        ArrivalTime = atime
        DepartureTime = dtime
        Destination = codecitymapping[data['DESTINATION']]
        Source = codecitymapping[data['SOURCE']]
        Fare = data['FARE']
        FlightNumber = data['FLIGHT_NUMBER']
        toUserDb = {}
        toUserDb['SOURCE'] = data['SOURCE']
        toUserDb['DESTINATION'] = data['DESTINATION']
        pnr = PNR.find_one({'_id':'PNR'})['PNR']

        toTransDB = []

        #to the TICKETS mydatabase
        ticket = {
            '_id':pnr,
            'FROM': Source,
            'TO': Destination,
            'AIRLINE_CODE': AirlineCode,
            'FLIGHT_NUMBER': FlightNumber,
            'DATE':BookingDate,
            'DEPARTURE_TIME':DepartureTime,
            'ARRIVAL_TIME':ArrivalTime,
            'NUMBER_OF_PASSENGERS':n,
            'FARE_PER_HEAD': Fare,
            'TOTAL_FARE': Fare * n,
            'USER': current_user.username
        }
        for i in passengers:
            flight_transaction = flighttrans.find_one({'_id':flighttrans_id})
            flight_transaction['NoOfSeats']-=1
            passenger = {'SEAT_NUMBER':60-flight_transaction['NoOfSeats'], 'NAME':i['FullName'], 'AGE':i['Age'],'GENDER':i['Gender']}
            flight_transaction['Passengers'].append(passenger)
            flighttrans.save(flight_transaction)
            toTransDB.append(passenger)
        ticket['PASSENGERS'] = toTransDB
        TICKETS.insert_one(ticket)
        UserTransaction['PNR'].append(pnr)
        userTrans.save(UserTransaction)

        print('toTransDB',toTransDB)
        print(ticket)

        return render_template('ticket.html',ticket = ticket)

@app.route('/my_journeys')
def my_journeys():
    userTrans = mongo.db.UserTransactions
    pnrs = userTrans.find_one({'_id':current_user.username})['PNR']
    TICKETS = mongo.db.TICKETS
    tickets = []
    for i in pnrs:
        tickets.insert(0,TICKETS.find_one({"_id":i}))
    return render_template('my_journeys.html',TICKETS = tickets)

@app.route('/PrintTicket',methods=['POST','GET'])
def PrintTicket():
    if  request.method == 'POST':
        PNR = request.form.get('PNR')
        print(PNR)
        TICKETS = mongo.db.TICKETS
        ticket = TICKETS.find_one({"_id":int(PNR)})
        print(ticket)
        return render_template('ticket.html',ticket = ticket)

#admin system
@app.route('/admin')
@login_required
def admin():
	if current_user.username == 'admin@airline.com':
		return render_template('admin.html')
	return '<h1>log in as Admin</h1>'

@app.route('/AddFlight', methods=['GET','POST'])
@login_required
def AddFlight():
	if current_user.username == 'admin@airline.com':
		if request.method == 'POST':
			try:
				FlightNumber = request.form.get('Flight Number')
				AirlineCode = request.form.get('Airline Code')
				AirlineCode = codeairlinemapping[AirlineCode]
				Source = request.form.get('Source')
				Scode = citycodemapping[Source]
				Destination = request.form.get('Destination')
				Dcode = citycodemapping[Destination]
				NoOfSeats = int(request.form.get('Number of seats'))
				DepartureTime = request.form.get('Departure Time')
				ArrivalTime = request.form.get('Arrival Time')
				Sunday = request.form.get('sunday')
				Monday = request.form.get('monday')
				Tuesday = request.form.get('tuesday')
				Wednesday = request.form.get('wednesday')
				Thursday = request.form.get('thursday')
				Friday = request.form.get('friday')
				Saturday = request.form.get('saturday')
				Fare = int(request.form.get('Fare'))
				l = []
				if Sunday:
					l.append(1)
				if Monday:
					l.append(2)
				if Tuesday:
					l.append(3)
				if Wednesday:
					l.append(4)
				if Thursday:
					l.append(5)
				if Friday:
					l.append(6)
				if Saturday:
					l.append(7)
				Frequency = ''
				Frequency = Frequency.join(list(map(str,l)))

				flight = {
					"AIRLINE_CODE": AirlineCode,
					"ARRIVAL_TIME": int(ArrivalTime.replace(':','')),
					"COMPLETE_FLIGHT_NUMBER":AirlineCode+FlightNumber+Scode+Dcode,
					"DAYS":l,
					"DEPARTURE_TIME": int(DepartureTime.replace(':','')),
					"DESTINATION": Dcode,
					"FLIGHT_NUMBER": FlightNumber,
					"FREQUENCY": Frequency,
					"SOURCE": Scode,
					"FARE": Fare
				}
				airlineDB = mongo.db.airlineDB
				airlineDB.insert_one(flight)
				return render_template('admin.html', flight = True)

			except:
				return render_template('Add Flight.html',cities = cities, airlines = airlines)

		return render_template('Add Flight.html',cities = cities, airlines = airlines)

	return '<h1>log in as Admin</h1>'

@app.route('/RemoveFlight', methods=['GET','POST'])
@login_required
def DeleteFlight():
	if current_user.username == 'admin@airline.com':
		if request.method == 'POST':
			try:
				FlightNumber = request.form.get('Flight Number')
				AirlineCode = request.form.get('Airline Code')
				AirlineCode = codeairlinemapping[AirlineCode]
				Source = request.form.get('Source')
				Scode = citycodemapping[Source]
				Destination = request.form.get('Destination')
				Dcode = citycodemapping[Destination]
				airlineDB = mongo.db.airlineDB
				airlineDB.delete_one({"COMPLETE_FLIGHT_NUMBER":AirlineCode+FlightNumber+Scode+Dcode})
				return render_template('admin.html', delete = True)

			except:
				return render_template('RemoveFlight.html',cities = cities, airlines = airlines)

		return render_template('RemoveFlight.html',cities = cities, airlines = airlines)

	return '<h1>log in as Admin</h1>'

@app.route('/UpdateFlight', methods=['GET','POST'])
@login_required
def UpdateFlight():
	if current_user.username == 'admin@airline.com':
		if request.method == 'POST':
			try:
				FlightNumber = request.form.get('Flight Number')
				AirlineCode = request.form.get('Airline Code')
				AirlineCode = codeairlinemapping[AirlineCode]
				Source = request.form.get('Source')
				Scode = citycodemapping[Source]
				Destination = request.form.get('Destination')
				Dcode = citycodemapping[Destination]
				NoOfSeats = int(request.form.get('Number of seats'))
				DepartureTime = request.form.get('Departure Time')
				ArrivalTime = request.form.get('Arrival Time')
				Sunday = request.form.get('sunday')
				Monday = request.form.get('monday')
				Tuesday = request.form.get('tuesday')
				Wednesday = request.form.get('wednesday')
				Thursday = request.form.get('thursday')
				Friday = request.form.get('friday')
				Saturday = request.form.get('saturday')
				Fare = int(request.form.get('Fare'))
				l = []
				if Sunday:
					l.append(1)
				if Monday:
					l.append(2)
				if Tuesday:
					l.append(3)
				if Wednesday:
					l.append(4)
				if Thursday:
					l.append(5)
				if Friday:
					l.append(6)
				if Saturday:
					l.append(7)
				Frequency = ''
				Frequency = Frequency.join(list(map(str,l)))

				flight = {
				}
				airlineDB = mongo.db.airlineDB
				flight = airlineDB.find_one({"COMPLETE_FLIGHT_NUMBER":AirlineCode+FlightNumber+Scode+Dcode})
				flight['ARRIVAL_TIME'] = int(ArrivalTime.replace(':',''))
				flight['DAYS'] = l
				flight["DEPARTURE_TIME"] = int(DepartureTime.replace(':',''))
				flight["FREQUENCY"]=Frequency
				flight["FARE"]= Fare
				airlineDB.save(flight)
				return render_template('admin.html', update = True)

			except:
				return render_template('Update Flight.html',cities = cities, airlines = airlines)

		return render_template('Update Flight.html',cities = cities, airlines = airlines)

	return '<h1>log in as Admin</h1>'

@app.route('/PrintList', methods=['GET','POST'])
@login_required
def PrintList():
	if current_user.username == 'admin@airline.com':
		if request.method == 'POST':
			try:
				FlightNumber = request.form.get('Flight Number')
				FlightDetails = {}
				FlightDetails['FLIGHT_NUMBER'] = FlightNumber
				AirlineCode = request.form.get('Airline Code')
				FlightDetails['AIRLINE_CODE'] = AirlineCode
				AirlineCode = codeairlinemapping[AirlineCode]
				Source = request.form.get('Source')
				Scode = citycodemapping[Source]
				Destination = request.form.get('Destination')
				Dcode = citycodemapping[Destination]
				DATE = request.form.get('DateOfJourney')
				flighttrans_id = DATE+AirlineCode+FlightNumber+Scode+Dcode
				flighttrans = mongo.db.flighttrans
				passengers = flighttrans.find_one({'_id':flighttrans_id})
				print(passengers)
				passengers = passengers['Passengers']
				airlineDB = mongo.db.airlineDB
				flight = airlineDB.find_one({"COMPLETE_FLIGHT_NUMBER":AirlineCode+FlightNumber+Scode+Dcode})
				FlightDetails['FROM'] = Source
				FlightDetails['TO'] = Destination
				FlightDetails['DATE'] = DATE
				dtime = str(flight['DEPARTURE_TIME']).rjust(4,'0')
				min = dtime[-2:]
				hrs = dtime[:-2]
				dtime = hrs+':'+min
				FlightDetails['DEPARTURE_TIME'] = dtime
				atime = str(flight['ARRIVAL_TIME']).rjust(4,'0')
				min = atime[-2:]
				hrs = atime[:-2]
				atime = hrs+':'+min
				FlightDetails['ARRIVAL_TIME'] = atime
				return render_template('PassengersList.html', flight = FlightDetails, passengers = passengers)

			except:
				return render_template('PrintList.html',cities = cities, airlines = airlines)

		return render_template('PrintList.html',cities = cities, airlines = airlines)

	return '<h1>log in as Admin</h1>'



if __name__ == '__main__':
    app.run(debug=True)
