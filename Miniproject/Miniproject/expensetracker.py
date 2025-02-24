from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Expense categories
categories = ["Food", "Transport", "Entertainment", "Others"]

# Dictionary to store expenses
expenses = {category: 0 for category in categories}

def calculate_total():
    return sum(expenses.values())

def calculate_percentages():
    total = calculate_total()
    if total == 0:
        return {category: 0 for category in categories}
    return {category: (amount / total) * 100 for category, amount in expenses.items()}

@app.route('/')
def index():
    total_expenses = calculate_total()
    percentages = calculate_percentages()
    return render_template('index.html', categories=categories, expenses=expenses, total=total_expenses, percentages=percentages)

@app.route('/add', methods=['POST'])
def add_expense():
    category = request.form['category']
    amount = float(request.form['amount'])
    if category in expenses:
        expenses[category] += amount
    return redirect(url_for('index'))

@app.route('/summary')
def summary():
    total_expenses = calculate_total()
    percentages = calculate_percentages()
    return render_template('summary.html', expenses=expenses, total=total_expenses, percentages=percentages)

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

if __name__ == '__main__':
    app.run(debug=True)
