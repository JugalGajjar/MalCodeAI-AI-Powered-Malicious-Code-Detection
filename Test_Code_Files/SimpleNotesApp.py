from flask import Flask, request, session, redirect, url_for, render_template_string, send_from_directory
import os
import uuid

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.debug = True

# In-memory storage
users = {"admin": "password123"}
notes = {}

# Ensuring upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Templates
login_template = '''
    <h2>Login</h2>
    <form method="POST">
        Username: <input name="username" required><br>
        Password: <input name="password" type="password" required><br>
        <button type="submit">Login</button>
    </form>
'''

notes_template = '''
    <h2>Welcome {{ username }}</h2>
    <a href="{{ url_for('logout') }}">Logout</a> | 
    <a href="{{ url_for('upload') }}">Upload Profile Picture</a>
    <h3>Create Note</h3>
    <form method="POST" action="{{ url_for('add_note') }}">
        Title: <input name="title" required><br>
        Content: <textarea name="content" required></textarea><br>
        <button type="submit">Add Note</button>
    </form>

    <h3>All Notes</h3>
    {% for note in notes %}
        <div style="border:1px solid black; margin:10px; padding:10px">
            <h4>{{ note['title'] }}</h4>
            <p>{{ note['content'] }}</p>
        </div>
    {% endfor %}
'''

upload_template = '''
    <h2>Upload Profile Picture</h2>
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="profile_pic" required><br>
        <button type="submit">Upload</button>
    </form>
    <a href="{{ url_for('notes_page') }}">Back to Notes</a>
'''

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            session['token'] = str(uuid.uuid4())
            return redirect(url_for('notes_page'))
        else:
            return "<p>Invalid credentials!</p>" + login_template
    return login_template

@app.route('/notes')
def notes_page():
    if 'username' not in session:
        return redirect(url_for('login'))
    user_notes = notes.get(session['username'], [])
    return render_template_string(notes_template, username=session['username'], notes=user_notes)

@app.route('/add_note', methods=['POST'])
def add_note():
    if 'username' not in session:
        return redirect(url_for('login'))
    title = request.form['title']
    content = request.form['content']
    note = {"title": title, "content": content}
    notes.setdefault(session['username'], []).append(note)
    return redirect(url_for('notes_page'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        file = request.files['profile_pic']
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return f"<p>Uploaded successfully: {filename}</p><a href='{url_for('notes_page')}'>Back</a>"
    return render_template_string(upload_template)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    app.run()
