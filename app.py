from flask import Flask, request, jsonify, render_template
import os
import json
from datetime import datetime
from functions import get_current_weather, get_air_pollution  # Import functions from weather_utils.py

app = Flask(__name__)

# Paths to the data files
OLD_DATA_FILE = 'static/data.json'
NEW_DATA_FILE = 'static/new_data.json'

# Ensure the static directory exists
if not os.path.exists('static'):
    os.makedirs('static')

# Serve the old markers
@app.route('/old-markers', methods=['GET'])
def get_old_markers():
    try:
        with open(OLD_DATA_FILE, 'r') as old_file:
            old_data = json.load(old_file)
        return jsonify(old_data)
    except Exception as e:
        print(f"Error loading old data: {e}")
        return jsonify({"error": str(e)}), 500

# Serve the new markers
@app.route('/new-markers', methods=['GET'])
def get_new_markers():
    try:
        with open(NEW_DATA_FILE, 'r') as new_file:
            new_data = json.load(new_file)
        return jsonify(new_data)
    except Exception as e:
        print(f"Error loading new data: {e}")
        return jsonify({"error": str(e)}), 500

# Handle the addition of new marker data (POST to new data)
@app.route('/markers', methods=['POST'])
def add_marker():
    new_marker = request.json
    print(f"Received marker data: {new_marker}")  # Log the received data

    try:
        # Ensure new_marker is a dictionary
        if not isinstance(new_marker, dict):
            raise ValueError("Expected a dictionary, but received something else.")

        lat = new_marker.get("lat")
        lon = new_marker.get("lon")

        if lat is None or lon is None:
            raise ValueError("Latitude and longitude are required.")

        # Fetch weather and air pollution data
        weather_data = get_current_weather(lat, lon)
        air_pollution_data = get_air_pollution(lat, lon)

        if weather_data:
            new_marker["weather"] = weather_data["weather"][0].get("main", "")  # Main weather condition (e.g., Rain)
            temp_kelvin = weather_data["main"].get("temp", 0)
            temp_celsius = temp_kelvin - 273.15
            new_marker["temp"] = round(temp_celsius, 2)  # Rounded to 2 decimal places

        if air_pollution_data:
            new_marker["aqi"] = air_pollution_data.get("aqi", "")
            new_marker["co"] = air_pollution_data.get("co", "")

        # Read the new data file
        with open(NEW_DATA_FILE, 'r') as file:
            data = json.load(file)

        # Append new marker data
        data.append(new_marker)

        # Write the updated data back to the file
        with open(NEW_DATA_FILE, 'w') as file:
            json.dump(data, file, indent=4)

        return jsonify(new_marker), 200  # Send the updated marker data back with added details
    except Exception as e:
        print(f"Error saving marker: {e}")
        return jsonify({"error": str(e)}), 500


# Handle image upload (if applicable)
@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image part'}), 400
    image = request.files['image']
    if image.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    try:
        # Save the image file
        image.save(os.path.join('static', image.filename))
        return jsonify({'url': f"/static/{image.filename}"}), 200
    except Exception as e:
        print(f"Error uploading image: {e}")
        return jsonify({"error": str(e)}), 500

# Serve the homepage
@app.route("/")
def homepage():
    return render_template("SEA.html")

@app.route("/homepage")
def show_homepage():
    return render_template("homepage.html")

@app.route("/findings")
def show_findings():
    return render_template("findings.html")

@app.route("/us")
def show_us():
    return render_template("about-us.html")


#@app.route('/filter', methods=['GET'])
def filter_markers():
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')
    weather = request.args.get('weather', '')
    temperature = request.args.get('temperature', '')
    air = request.args.get('air', '')
    co = request.args.get('co', '')

    # Debugging: print the filters to check if they're being received correctly
    print(f"Filters received: start_date={start_date}, end_date={end_date}, weather={weather}, "
          f"temperature={temperature}, air={air}, co={co}")

    filtered = []
    
    try:
        # Load the old markers
        with open(OLD_DATA_FILE, 'r') as old_file:
            old_data = json.load(old_file)

        for marker in old_data:
            # Date filter
            if start_date and datetime.strptime(marker['date'], '%Y-%m-%d') < datetime.strptime(start_date, '%Y-%m-%d'):
                continue
            if end_date and datetime.strptime(marker['date'], '%Y-%m-%d') > datetime.strptime(end_date, '%Y-%m-%d'):
                continue
            
            # Weather filter
            if weather and weather.lower() not in marker['Weather'].lower():
                continue

            # Temperature filter (assuming the filter format is like '>=10' or '<=30')
            if temperature:
                try:
                    temp_value = marker['Temperature C']
                    if not eval(f"{temp_value} {temperature}"):  # You could improve this with a safe evaluation
                        continue
                except Exception as e:
                    print(f"Error evaluating temperature filter: {e}")
                    continue
            
            # Air Quality Index filter (similar to temperature filter)
            if air:
                try:
                    aqi_value = marker['Air Quality Index (AQI)']
                    if not eval(f"{aqi_value} {air}"):
                        continue
                except Exception as e:
                    print(f"Error evaluating AQI filter: {e}")
                    continue
            
            # CO Concentration filter (similar to temperature filter)
            if co:
                try:
                    co_value = marker['CO Concentration μg/m3']
                    if not eval(f"{co_value} {co}"):
                        continue
                except Exception as e:
                    print(f"Error evaluating CO filter: {e}")
                    continue
            
            filtered.append(marker)

        return jsonify(filtered)

    except Exception as e:
        print(f"Error applying filters: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
