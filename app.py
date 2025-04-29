from flask import Flask, render_template, request, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename

git add static/ templates/

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Für Flash-Nachrichten

# Route für die Startseite
@app.route('/')
def index():
    return render_template('index.html')

# Route zum Hochladen der Audioaufnahme
@app.route('/upload', methods=['POST'])
def upload():
    try:
        if 'audio' not in request.files:
            flash('Keine Audiodatei hochgeladen.')
            return redirect(url_for('index'))
        
        audio_file = request.files['audio']
        if audio_file.filename == '':
            flash('Keine Datei ausgewählt.')
            return redirect(url_for('index'))
        
        # Sicherstellen, dass der Dateiname sicher ist
        filename = secure_filename(audio_file.filename)
        
        # Speichern der Datei im lokalen Verzeichnis
        audio_file.save(os.path.join('uploads', filename))
        flash('Audio erfolgreich hochgeladen!')
    except Exception as e:
        flash(f'Fehler beim Hochladen: {str(e)}')
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Sicherstellen, dass der Upload-Ordner existiert
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)
