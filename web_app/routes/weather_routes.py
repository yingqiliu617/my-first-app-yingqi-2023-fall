
# this is the "web_app/routes/weather_routes.py" file ...

from flask import Blueprint, request, render_template, redirect, flash

from app.weather_dashboard import display_forecast

weather_routes = Blueprint("weather_routes", __name__)

@weather_routes.route("/weather/form")
def weather_form():
    print("WEATHER FORM...")
    return render_template("weather_form.html")

@weather_routes.route("/weather/dashboard", methods=["GET", "POST"])
def weather_dashboard():
    print("WEATHER DASHBOARD...")

    if request.method == "POST":
        # for data sent via POST request, form inputs are in request.form:
        request_data = dict(request.form)
        print("FORM DATA:", request_data)
    else:
        # for data sent via GET request, url params are in request.args
        request_data = dict(request.args)
        print("URL PARAMS:", request_data)

    symbol = request_data.get("symbol") or "20057"

    try:
        df = display_forecast(zip_code=symbol)
        # latest_close_usd = format_usd(df.iloc[0]["adjusted_close"])
        latest_date = df.iloc[0]["date"]
        data = df.to_dict("records")

        return render_template("weather_dashboard.html",
            symbol=symbol,
            # latest_close_usd=latest_close_usd,
            latest_date=latest_date,
            data=data
        )
    except Exception as err:
        print('OOPS', err)

        #flash("Market Data Error. Please check your symbol and try again!", "danger")
        return redirect("/weather/form")

#
# API ROUTES
#

@weather_routes.route("/api/weather.json")
def weather_api():
    print("WEATHER DATA (API)...")

    # for data supplied via GET request, url params are in request.args:
    url_params = dict(request.args)
    print("URL PARAMS:", url_params)
    symbol = url_params.get("symbol") or "20057"

    try:
        df = display_forecast(zip_code=symbol)
        data = df.to_dict("records")
        return {"symbol": symbol, "data": data }
    except Exception as err:
        print('OOPS', err)
        return {"message":"Weather Data Error. Please try again."}, 404