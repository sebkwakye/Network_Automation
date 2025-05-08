'''
Flask Web Application Development
Objective: The objective of this assignment is to create a basic web application using Flask.
You will learn to develop multiple pages with hyperlinks to navigate between them.
You will also gain additional experience in rendering HTML templates using Flask.
'''

from flask import Flask, render_template   # necessary modules from the Flask package

app = Flask(__name__)   # instance of the Flask class, representing the web application

# Route for the home page
@app.route('/')
def splash():
    # Render and return the "splash.html" template when the home page is accessed
    return render_template('splash.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/course_goals')
def course_goals():
    return render_template('course_goals.html')

@app.route('/honor_code')
def honor_code():
    return render_template('honor_code.html')


if __name__ == '__main__':
    app.run(debug=True)

