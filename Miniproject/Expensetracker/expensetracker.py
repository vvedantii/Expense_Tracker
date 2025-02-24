from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management

# Simulated database (Replace with actual database later)
users = {}
categories = ["Food", "Transport", "Entertainment", "Others"]
expenses = {category: 0 for category in categories}

def calculate_total():
    return sum(expenses.values())

def calculate_percentages():
    total = calculate_total()
    return {category: (amount / total) * 100 if total else 0 for category, amount in expenses.items()}

@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', categories=categories, expenses=expenses, total=calculate_total(), percentages=calculate_percentages())

@app.route('/add', methods=['POST'])
def add_expense():
    if 'username' not in session:
        return redirect(url_for('login'))
    category = request.form['category']
    amount = float(request.form['amount'])
    if category in expenses:
        expenses[category] += amount
    return redirect(url_for('index'))

@app.route('/update', methods=['POST'])
def update_expense():
    if 'username' not in session:
        return redirect(url_for('login'))
    category = request.form['category']
    new_amount = float(request.form['new_amount'])
    if category in expenses:
        expenses[category] = new_amount  # Update the expense with new amount
    return redirect(url_for('index'))

@app.route('/summary')
def summary():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('summary.html', expenses=expenses, total=calculate_total(), percentages=calculate_percentages())

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/reset', methods=['POST'])
def reset_expenses():
    global expenses
    expenses = {category: 0 for category in categories}
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('index'))
        return "Invalid credentials. Try again."
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            return "User already exists!"
        users[username] = password
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
