from flask import Flask, request, jsonify, render_template
import os
import json

app = Flask(__name__)

# Paths to the data files
OLD_DATA_FILE = 'static/old_data.json'
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
    try:
        # Read the new data file and append the new marker
        with open(NEW_DATA_FILE, 'r') as file:
            data = json.load(file)

        # Append the new marker
        data.append(new_marker)

        # Write the updated data back to the new_data.json file
        with open(NEW_DATA_FILE, 'w') as file:
            json.dump(data, file, indent=4)

        return jsonify({"status": "success"}), 200
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
        # Save the image file to static folder
        filepath = os.path.join('static', image.filename)
        image.save(filepath)
        return jsonify({'url': f"/static/{image.filename}"}), 200
    except Exception as e:
        print(f"Error uploading image: {e}")
        return jsonify({"error": str(e)}), 500
    
# Serve the homepage
@app.route("/")
def homepage():
    return render_template("homepage.html")

if __name__ == '__main__':
    app.run(debug=True)
