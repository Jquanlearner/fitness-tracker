from flask import Flask, render_template, request, redirect, url_for
import json
from datetime import datetime

app = Flask(__name__)
DATA_FILE = 'data.json'

def load_data():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/', methods=['GET', 'POST'])
def index():
    data = load_data()
    if request.method == 'POST':
        date = request.form['date']
        workout_name = request.form['workout_name']
        exercises = []
        count = int(request.form['exercise-count'])

        for i in range(count):
            name = request.form.get(f'exercise-{i}-name', '')
            sets = request.form.get(f'exercise-{i}-sets', '')
            reps = request.form.get(f'exercise-{i}-reps', '')
            weight = request.form.get(f'exercise-{i}-weight', '')
            notes = request.form.get(f'exercise-{i}-notes', '')
            if name:
                exercises.append({
                    'name': name,
                    'sets': sets,
                    'reps': reps,
                    'weight': weight,
                    'notes': notes
                })

        data.append({
            'date': date,
            'workout_name': workout_name,
            'exercises': exercises
        })
        save_data(data)
        return redirect(url_for('index'))

    return render_template('index.html', past_workouts=data)

@app.route('/edit/<int:index>', methods=['GET', 'POST'])
def edit(index):
    data = load_data()
    if index >= len(data):
        return redirect(url_for('history'))

    if request.method == 'POST':
        data[index]['date'] = request.form['date']
        data[index]['workout_name'] = request.form['workout_name']
        exercises = []
        count = int(request.form['exercise-count'])

        for i in range(count):
            name = request.form.get(f'exercise-{i}-name', '')
            sets = request.form.get(f'exercise-{i}-sets', '')
            reps = request.form.get(f'exercise-{i}-reps', '')
            weight = request.form.get(f'exercise-{i}-weight', '')
            notes = request.form.get(f'exercise-{i}-notes', '')
            if name:
                exercises.append({
                    'name': name,
                    'sets': sets,
                    'reps': reps,
                    'weight': weight,
                    'notes': notes
                })
        data[index]['exercises'] = exercises
        save_data(data)
        return redirect(url_for('history'))

    return render_template('edit.html', workout=data[index], index=index)

@app.route('/history')
def history():
    data = load_data()
    return render_template('history.html', workouts=data)

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
