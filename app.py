from flask import Flask, request, render_template
from flask_cors import cross_origin
import sklearn
import pickle
import time
import pandas as pd

# [$] For Sending Mail =>
import smtplib,ssl

port = 587
smtp_server = "smtp.gmail.com"
sender = "adcetcse1@gmail.com"
reciever = "suryawanshisanket69@gmail.com"
password = "ADCETcse1@"

context = ssl.create_default_context()



app = Flask(__name__)
model = pickle.load(open("flight_rf.pkl", "rb"))

model2 = pickle.load(open("hotel_price_pred.pkl", "rb"))

@app.route("/")
@cross_origin()
def home():
    return render_template("home.html")

@app.route("/hotel")
@cross_origin()
def hotel():
    return render_template("hotel.html")

@app.route("/about")
@cross_origin()
def about():
    return render_template("about.html")

@app.route("/developerinfo")
@cross_origin()
def developerinfo():
    return render_template("developerinfo.html")

@app.route("/SearchFlights")
@cross_origin()
def SearchFlights():
    return render_template("SearchFlights.html")

@app.route("/contact",methods=["GET", "POST"])
@cross_origin()
def contact():
    if request.method == "POST":
        FullName = request.form["FullName"]
        EmailID = request.form["EmailID"]
        Message = EmailID+' : '+request.form["Message"]

        print(FullName, EmailID, Message)

        
        with smtplib.SMTP(smtp_server,port) as server:
            server.starttls(context=context)
            server.login(sender, password)
            server.sendmail(sender,reciever, Message)

        time.sleep(3)
        return render_template('home.html')
    
    return render_template("contact.html")


@app.route("/predict", methods=["GET", "POST"])
@cross_origin()
def predict():
    if request.method == "POST":

        # Date_of_Journey
        date_dep = request.form["Dep_Time"]
        Journey_day = int(pd.to_datetime(
            date_dep, format="%Y-%m-%dT%H:%M").day)
        Journey_month = int(pd.to_datetime(
            date_dep, format="%Y-%m-%dT%H:%M").month)
        # print("Journey Date : ",Journey_day, Journey_month)

        # Departure
        Dep_hour = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").hour)
        Dep_min = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").minute)
        # print("Departure : ",Dep_hour, Dep_min)

        # Arrival
        date_arr = request.form["Arrival_Time"]
        Arrival_hour = int(pd.to_datetime(
            date_arr, format="%Y-%m-%dT%H:%M").hour)
        Arrival_min = int(pd.to_datetime(
            date_arr, format="%Y-%m-%dT%H:%M").minute)
        # print("Arrival : ", Arrival_hour, Arrival_min)

        # Duration
        dur_hour = abs(Arrival_hour - Dep_hour)
        dur_min = abs(Arrival_min - Dep_min)
        # print("Duration : ", dur_hour, dur_min)

        # Total Stops
        Total_stops = int(request.form["stops"])
        # print(Total_stops)

        # Airline
        # AIR ASIA = 0 (not in column)
        airline = request.form['airline']
        if(airline == 'Jet Airways'):
            Jet_Airways = 1
            IndiGo = 0
            Air_India = 0
            Multiple_carriers = 0
            SpiceJet = 0
            Vistara = 0
            GoAir = 0
            Multiple_carriers_Premium_economy = 0
            Jet_Airways_Business = 0
            Vistara_Premium_economy = 0
            Trujet = 0

        elif (airline == 'IndiGo'):
            Jet_Airways = 0
            IndiGo = 1
            Air_India = 0
            Multiple_carriers = 0
            SpiceJet = 0
            Vistara = 0
            GoAir = 0
            Multiple_carriers_Premium_economy = 0
            Jet_Airways_Business = 0
            Vistara_Premium_economy = 0
            Trujet = 0

        elif (airline == 'Air India'):
            Jet_Airways = 0
            IndiGo = 0
            Air_India = 1
            Multiple_carriers = 0
            SpiceJet = 0
            Vistara = 0
            GoAir = 0
            Multiple_carriers_Premium_economy = 0
            Jet_Airways_Business = 0
            Vistara_Premium_economy = 0
            Trujet = 0

        elif (airline == 'Multiple carriers'):
            Jet_Airways = 0
            IndiGo = 0
            Air_India = 0
            Multiple_carriers = 1
            SpiceJet = 0
            Vistara = 0
            GoAir = 0
            Multiple_carriers_Premium_economy = 0
            Jet_Airways_Business = 0
            Vistara_Premium_economy = 0
            Trujet = 0

        elif (airline == 'SpiceJet'):
            Jet_Airways = 0
            IndiGo = 0
            Air_India = 0
            Multiple_carriers = 0
            SpiceJet = 1
            Vistara = 0
            GoAir = 0
            Multiple_carriers_Premium_economy = 0
            Jet_Airways_Business = 0
            Vistara_Premium_economy = 0
            Trujet = 0

        elif (airline == 'Vistara'):
            Jet_Airways = 0
            IndiGo = 0
            Air_India = 0
            Multiple_carriers = 0
            SpiceJet = 0
            Vistara = 1
            GoAir = 0
            Multiple_carriers_Premium_economy = 0
            Jet_Airways_Business = 0
            Vistara_Premium_economy = 0
            Trujet = 0

        elif (airline == 'GoAir'):
            Jet_Airways = 0
            IndiGo = 0
            Air_India = 0
            Multiple_carriers = 0
            SpiceJet = 0
            Vistara = 0
            GoAir = 1
            Multiple_carriers_Premium_economy = 0
            Jet_Airways_Business = 0
            Vistara_Premium_economy = 0
            Trujet = 0

        elif (airline == 'Multiple carriers Premium economy'):
            Jet_Airways = 0
            IndiGo = 0
            Air_India = 0
            Multiple_carriers = 0
            SpiceJet = 0
            Vistara = 0
            GoAir = 0
            Multiple_carriers_Premium_economy = 1
            Jet_Airways_Business = 0
            Vistara_Premium_economy = 0
            Trujet = 0

        elif (airline == 'Jet Airways Business'):
            Jet_Airways = 0
            IndiGo = 0
            Air_India = 0
            Multiple_carriers = 0
            SpiceJet = 0
            Vistara = 0
            GoAir = 0
            Multiple_carriers_Premium_economy = 0
            Jet_Airways_Business = 1
            Vistara_Premium_economy = 0
            Trujet = 0

        elif (airline == 'Vistara Premium economy'):
            Jet_Airways = 0
            IndiGo = 0
            Air_India = 0
            Multiple_carriers = 0
            SpiceJet = 0
            Vistara = 0
            GoAir = 0
            Multiple_carriers_Premium_economy = 0
            Jet_Airways_Business = 0
            Vistara_Premium_economy = 1
            Trujet = 0

        elif (airline == 'Trujet'):
            Jet_Airways = 0
            IndiGo = 0
            Air_India = 0
            Multiple_carriers = 0
            SpiceJet = 0
            Vistara = 0
            GoAir = 0
            Multiple_carriers_Premium_economy = 0
            Jet_Airways_Business = 0
            Vistara_Premium_economy = 0
            Trujet = 1

        else:
            Jet_Airways = 0
            IndiGo = 0
            Air_India = 0
            Multiple_carriers = 0
            SpiceJet = 0
            Vistara = 0
            GoAir = 0
            Multiple_carriers_Premium_economy = 0
            Jet_Airways_Business = 0
            Vistara_Premium_economy = 0
            Trujet = 0

        # print(Jet_Airways,
        #     IndiGo,
        #     Air_India,
        #     Multiple_carriers,
        #     SpiceJet,
        #     Vistara,
        #     GoAir,
        #     Multiple_carriers_Premium_economy,
        #     Jet_Airways_Business,
        #     Vistara_Premium_economy,
        #     Trujet)

        # Source
        # Banglore = 0 (not in column)
        Source = request.form["Source"]
        if (Source == 'Delhi'):
            s_Delhi = 1
            s_Kolkata = 0
            s_Mumbai = 0
            s_Chennai = 0

        elif (Source == 'Kolkata'):
            s_Delhi = 0
            s_Kolkata = 1
            s_Mumbai = 0
            s_Chennai = 0

        elif (Source == 'Mumbai'):
            s_Delhi = 0
            s_Kolkata = 0
            s_Mumbai = 1
            s_Chennai = 0

        elif (Source == 'Chennai'):
            s_Delhi = 0
            s_Kolkata = 0
            s_Mumbai = 0
            s_Chennai = 1

        else:
            s_Delhi = 0
            s_Kolkata = 0
            s_Mumbai = 0
            s_Chennai = 0

        # print(s_Delhi,
        #     s_Kolkata,
        #     s_Mumbai,
        #     s_Chennai)

        # Destination
        # Banglore = 0 (not in column)
        Source = request.form["Destination"]
        if (Source == 'Cochin'):
            d_Cochin = 1
            d_Delhi = 0
            d_New_Delhi = 0
            d_Hyderabad = 0
            d_Kolkata = 0

        elif (Source == 'Delhi'):
            d_Cochin = 0
            d_Delhi = 1
            d_New_Delhi = 0
            d_Hyderabad = 0
            d_Kolkata = 0

        elif (Source == 'New_Delhi'):
            d_Cochin = 0
            d_Delhi = 0
            d_New_Delhi = 1
            d_Hyderabad = 0
            d_Kolkata = 0

        elif (Source == 'Hyderabad'):
            d_Cochin = 0
            d_Delhi = 0
            d_New_Delhi = 0
            d_Hyderabad = 1
            d_Kolkata = 0

        elif (Source == 'Kolkata'):
            d_Cochin = 0
            d_Delhi = 0
            d_New_Delhi = 0
            d_Hyderabad = 0
            d_Kolkata = 1

        else:
            d_Cochin = 0
            d_Delhi = 0
            d_New_Delhi = 0
            d_Hyderabad = 0
            d_Kolkata = 0

        # print(
        #     d_Cochin,
        #     d_Delhi,
        #     d_New_Delhi,
        #     d_Hyderabad,
        #     d_Kolkata
        # )

    #     ['Total_Stops', 'Journey_day', 'Journey_month', 'Dep_hour',
    #    'Dep_min', 'Arrival_hour', 'Arrival_min', 'Duration_hours',
    #    'Duration_mins', 'Airline_Air India', 'Airline_GoAir', 'Airline_IndiGo',
    #    'Airline_Jet Airways', 'Airline_Jet Airways Business',
    #    'Airline_Multiple carriers',
    #    'Airline_Multiple carriers Premium economy', 'Airline_SpiceJet',
    #    'Airline_Trujet', 'Airline_Vistara', 'Airline_Vistara Premium economy',
    #    'Source_Chennai', 'Source_Delhi', 'Source_Kolkata', 'Source_Mumbai',
    #    'Destination_Cochin', 'Destination_Delhi', 'Destination_Hyderabad',
    #    'Destination_Kolkata', 'Destination_New Delhi']

        if(request.form["Source"]==request.form["Destination"]):
            output = 0
            return render_template('home.html', prediction_text="Your Flight price is Rs. {}".format(output))

        prediction = model.predict([[
            Total_stops,
            Journey_day,
            Journey_month,
            Dep_hour,
            Dep_min,
            Arrival_hour,
            Arrival_min,
            dur_hour,
            dur_min,
            Air_India,
            GoAir,
            IndiGo,
            Jet_Airways,
            Jet_Airways_Business,
            Multiple_carriers,
            Multiple_carriers_Premium_economy,
            SpiceJet,
            Trujet,
            Vistara,
            Vistara_Premium_economy,
            s_Chennai,
            s_Delhi,
            s_Kolkata,
            s_Mumbai,
            d_Cochin,
            d_Delhi,
            d_Hyderabad,
            d_Kolkata,
            d_New_Delhi
        ]])

        output = round(prediction[0], 2)

        return render_template('home.html', prediction_text="Your Flight price is Rs. {}".format(output))

    return render_template("home.html")


@app.route("/predict2", methods=["GET", "POST"])
@cross_origin()
def predict2():
    if request.method == "POST":

        # [$] Taking Parameters =>

        # [1] Hotel Capacity =>
        Hotel_Capacity = int(request.form["capacity"])
        print(Hotel_Capacity)

        # [2] Star Ratings =>
        Ratings = int(request.form["ratings"])
        print(Ratings)

        # [3] Is Tourist Destination =>
        IsTouristDestination = request.form["touristDestination"]

        if(IsTouristDestination=="YES"):
            IsTouristDestination = 1
        else:
            IsTouristDestination = 0
        print(IsTouristDestination)


        # [4] Is Hotel Luxury =>
        IsHotelLuxury = request.form["luxury"]

        if(IsHotelLuxury=="YES"):
            IsHotelLuxury = 1
        else:
            IsHotelLuxury = 0
        print(IsHotelLuxury)

        # [5] Is Free Wifi =>
        IsFreeWifi = request.form["freeWifi"]

        if(IsFreeWifi=="YES"):
            IsFreeWifi = 1
        else:
            IsFreeWifi = 0
        print(IsFreeWifi)

        # [6] Is Free Breakfast =>
        IsFreeBreakfast = request.form["freebreakfast"]

        if(IsFreeBreakfast=="YES"):
            IsFreeBreakfast = 1
        else:
            IsFreeBreakfast = 0
        print(IsFreeBreakfast)
        
        
        # [7] Is Free Breakfast =>
        HasSwimmingPool = request.form["Swimmingpool"]

        if(HasSwimmingPool=="YES"):
            HasSwimmingPool = 1
        else:
            HasSwimmingPool = 0
        print(HasSwimmingPool)

        # [8] Is Metro City =>
        IsMetroCity = request.form["metrocity"]

        if(IsMetroCity=="YES"):
            IsMetroCity = 1
        else:
            IsMetroCity = 0
        print(IsMetroCity)

        # [9] CheckIn & Checkout Date =>
        CheckInDate = request.form["Check_In"]
        CheckINDay = int(pd.to_datetime(CheckInDate, format="%Y-%m-%dT%H:%M").day)
        CheckInMonth = int(pd.to_datetime(CheckInDate, format="%Y-%m-%dT%H:%M").month)

        # [10] CheckIn & Checkout Date =>
        CheckoutDate = request.form["Check_Out"]
        CheckoutDay = int(pd.to_datetime(CheckoutDate, format="%Y-%m-%dT%H:%M").day)
        CheckoutMonth = int(pd.to_datetime(CheckoutDate, format="%Y-%m-%dT%H:%M").month)

        # [11] Taking City Name =>

        CityName = request.form["city"]

        if(CityName=="CityName_Ahmedabad"):
            CityName_Ahmedabad = 1
            CityName_Bangalore = 0
            CityName_Chennai = 0	
            CityName_Delhi = 0
            CityName_Goa = 0
            CityName_Hyderabad= 0	
            CityName_Jaipur	= 0
            CityName_Kochi	= 0
            CityName_Kolkata = 0
            CityName_Mumbai	= 0
            CityName_Pune = 0
            CityName_Udaipur = 0
        elif(CityName=="CityName_Bangalore"):
            CityName_Ahmedabad = 0
            CityName_Bangalore = 1
            CityName_Chennai = 0	
            CityName_Delhi = 0
            CityName_Goa = 0
            CityName_Hyderabad= 0	
            CityName_Jaipur	= 0
            CityName_Kochi	= 0
            CityName_Kolkata = 0
            CityName_Mumbai	= 0
            CityName_Pune = 0
            CityName_Udaipur = 0
        elif(CityName=="CityName_Chennai"):
            CityName_Ahmedabad = 0
            CityName_Bangalore = 0
            CityName_Chennai = 1	
            CityName_Delhi = 0
            CityName_Goa = 0
            CityName_Hyderabad= 0	
            CityName_Jaipur	= 0
            CityName_Kochi	= 0
            CityName_Kolkata = 0
            CityName_Mumbai	= 0
            CityName_Pune = 0
            CityName_Udaipur = 0
        elif(CityName=="CityName_Delhi"):
            CityName_Ahmedabad = 0
            CityName_Bangalore = 0
            CityName_Chennai = 0	
            CityName_Delhi = 1
            CityName_Goa = 0
            CityName_Hyderabad= 0	
            CityName_Jaipur	= 0
            CityName_Kochi	= 0
            CityName_Kolkata = 0
            CityName_Mumbai	= 0
            CityName_Pune = 0
            CityName_Udaipur = 0
        elif(CityName=="CityName_Goa"):
            CityName_Ahmedabad = 0
            CityName_Bangalore = 0
            CityName_Chennai = 0	
            CityName_Delhi = 0
            CityName_Goa = 1
            CityName_Hyderabad= 0	
            CityName_Jaipur	= 0
            CityName_Kochi	= 0
            CityName_Kolkata = 0
            CityName_Mumbai	= 0
            CityName_Pune = 0
            CityName_Udaipur = 0
        elif(CityName=="c"):
            CityName_Ahmedabad = 0
            CityName_Bangalore = 0
            CityName_Chennai = 0	
            CityName_Delhi = 0
            CityName_Goa = 0
            CityName_Hyderabad= 1
            CityName_Jaipur	= 0
            CityName_Kochi	= 0
            CityName_Kolkata = 0
            CityName_Mumbai	= 0
            CityName_Pune = 0
            CityName_Udaipur = 0
        elif(CityName=="CityName_Jaipur"):
            CityName_Ahmedabad = 0
            CityName_Bangalore = 0
            CityName_Chennai = 0	
            CityName_Delhi = 0
            CityName_Goa = 0
            CityName_Hyderabad= 0
            CityName_Jaipur	= 1
            CityName_Kochi	= 0
            CityName_Kolkata = 0
            CityName_Mumbai	= 0
            CityName_Pune = 0
            CityName_Udaipur = 0
        elif(CityName=="CityName_Kochi"):
            CityName_Ahmedabad = 0
            CityName_Bangalore = 0
            CityName_Chennai = 0	
            CityName_Delhi = 0
            CityName_Goa = 0
            CityName_Hyderabad= 0
            CityName_Jaipur	= 0
            CityName_Kochi	= 1
            CityName_Kolkata = 0
            CityName_Mumbai	= 0
            CityName_Pune = 0
            CityName_Udaipur = 0
        elif(CityName=="CityName_Kolkata"):
            CityName_Ahmedabad = 0
            CityName_Bangalore = 0
            CityName_Chennai = 0	
            CityName_Delhi = 0
            CityName_Goa = 0
            CityName_Hyderabad= 0
            CityName_Jaipur	= 0
            CityName_Kochi	= 0
            CityName_Kolkata = 1
            CityName_Mumbai	= 0
            CityName_Pune = 0
            CityName_Udaipur = 0
        elif(CityName=="CityName_Mumbai"):
            CityName_Ahmedabad = 0
            CityName_Bangalore = 0
            CityName_Chennai = 0	
            CityName_Delhi = 0
            CityName_Goa = 0
            CityName_Hyderabad= 0
            CityName_Jaipur	= 0
            CityName_Kochi	= 0
            CityName_Kolkata = 0
            CityName_Mumbai	= 1
            CityName_Pune = 0
            CityName_Udaipur = 0
        elif(CityName=="CityName_Pune"):
            CityName_Ahmedabad = 0
            CityName_Bangalore = 0
            CityName_Chennai = 0	
            CityName_Delhi = 0
            CityName_Goa = 0
            CityName_Hyderabad= 0
            CityName_Jaipur	= 0
            CityName_Kochi	= 0
            CityName_Kolkata = 0
            CityName_Mumbai	= 0
            CityName_Pune = 1
            CityName_Udaipur = 0
        else:
            CityName_Ahmedabad = 0
            CityName_Bangalore = 0
            CityName_Chennai = 0	
            CityName_Delhi = 0
            CityName_Goa = 0
            CityName_Hyderabad= 0
            CityName_Jaipur	= 0
            CityName_Kochi	= 0
            CityName_Kolkata = 0
            CityName_Mumbai	= 0
            CityName_Pune = 0
            CityName_Udaipur = 1

        # [12] Taking Hotel Type =>
        Hotel_Type = request.form["hotel_type"]

        if(Hotel_Type=="OYO"):
            Luxury = 0
            OYO = 1
            Taj	= 0
            Garden_Hotel = 0	
            Other = 0
        elif(Hotel_Type=="Luxury"):
            Luxury = 1
            OYO = 0
            Taj	= 0
            Garden_Hotel = 0	
            Other = 0
        elif(Hotel_Type=="Taj"):
            Luxury = 0
            OYO = 0
            Taj	= 1
            Garden_Hotel = 0	
            Other = 0
        elif(Hotel_Type=="Garden_Hotel"):
            Luxury = 0
            OYO = 0
            Taj	= 0
            Garden_Hotel = 1
            Other = 0
        else:
            Luxury = 0
            OYO = 0
            Taj	= 0
            Garden_Hotel = 0
            Other = 1
        
        CityRank = 0
        IsWeekend = 0
        IsNewYear = 0
        Airport = 25

        prediction = model2.predict([[
            CityRank,
            IsMetroCity,
            IsTouristDestination,
            IsWeekend,
            IsNewYear,
            Ratings,
            Airport,
            IsFreeWifi,
            IsFreeBreakfast,
            Hotel_Capacity,
            HasSwimmingPool,
            CheckINDay,
            CheckInMonth,
            Luxury,
            OYO,
            Taj,
            Garden_Hotel,
            Other,
            CityName_Ahmedabad,
            CityName_Bangalore,
            CityName_Chennai,
            CityName_Delhi,
            CityName_Goa,
            CityName_Hyderabad,
            CityName_Jaipur,
            CityName_Kochi,
            CityName_Kolkata,
            CityName_Mumbai,
            CityName_Pune,
            CityName_Udaipur
        ]])

        output = round(prediction[0], 2)
        
        return render_template('hotel.html',prediction_text="Your Hotel price is Rs. {}".format(output))
    
    return render_template('hotel.html')

if __name__ == "__main__":
    app.run(debug=True)
