from flask import Flask, request, redirect, url_for, render_template, session
import requests

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for session management

@app.route('/')
def index():
    # Default: No results to display
    results = session.pop('results', '')
    return render_template('index.html', results=results)

@app.route('/connect')
def connect():
    return render_template('connect.html')  # This will render connect.html

@app.route('/search', methods=['POST'])
def search():
    food = request.form['food']
    
    try:
        # Make the API request
        response = requests.get(
            f"https://api.edamam.com/api/nutrition-data?app_id=f05eab4e&app_key=4fcb4cd27d20ffbfdc991e3654322327&nutrition-type=logging&ingr={food}"
        )
        data = response.json()
        
        if 'totalNutrients' not in data or not data['totalNutrients']:
            results = "No data found for this food item."
        else:
            results = ""

            # Format results
            results += f"Calories: {data.get('calories', 'No data')}\n"

            # Extracting nutrient information with error handling
            nutrients = ['CHOCDF', 'FIBTG', 'SUGAR', 'PROCNT', 'FAT', 'NA', 'CA', 'FE']
            for nutrient in nutrients:
                try:
                    quantity = data['totalNutrients'][nutrient]['quantity']
                    unit = data['totalNutrients'][nutrient]['unit']
                    results += f"{nutrient}: {quantity} {unit}\n"
                except KeyError:
                    results += f"{nutrient}: No data\n"
            
            # Diet and health labels
            diet_labels = data.get('dietLabels', [])
            results += "Diet Labels:\n" + "\n".join(f"- {label}" for label in diet_labels) if diet_labels else "None\n"
            health_labels = data.get('healthLabels', [])
            results += "Health Labels:\n" + "\n".join(f"- {label}" for label in health_labels[:4]) if health_labels else "None\n"
    
    except Exception as e:
        results = f"Error: {str(e)}"
    
    # Store results in the session and redirect to home
    session['results'] = results
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
