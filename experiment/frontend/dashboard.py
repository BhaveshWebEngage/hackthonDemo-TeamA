from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def dashboard():
    # Mock data for the dashboard
    churn_predictions = [
        {'user_id': 'user1', 'churn_risk': 'Low'},
        {'user_id': 'user2', 'churn_risk': 'High'},
    ]
    return render_template('dashboard.html', churn_predictions=churn_predictions)

if __name__ == '__main__':
    app.run(debug=True)
