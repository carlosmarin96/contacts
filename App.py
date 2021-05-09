from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/contacts.db'
db = SQLAlchemy(app)

app.secret_key = 'mysecretkey'

class Contacts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100),nullable=False)
    company = db.Column(db.String(100),nullable=True)
    phone = db.Column(db.String(10),nullable=True)
    email = db.Column(db.String(100),nullable=False)

@app.route('/')
def index():
    data = Contacts.query.all()
    return render_template('index.html', contacts=data)
    

@app.route('/add_contact', methods=['POST'])
def add_contact():
    name = request.form['name']
    lastname = request.form['lastname']
    company = request.form['company']
    phone = request.form['phone']
    email = request.form['email']

    new_contact = Contacts(name=name, lastname=lastname, company=company, phone=phone, email=email)
    db.session.add(new_contact)
    db.session.commit()
    flash ("Added success")
    return redirect(url_for('index'))

@app.route('/edit/<id>')
def get_contact(id):
    data = Contacts.query.get(id)
    return render_template('update-contact.html', contact=data)

@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    contact_to_update = Contacts.query.get(id)

    contact_to_update.name = request.form['name']
    contact_to_update.lastname = request.form['lastname']
    contact_to_update.company = request.form['company']
    contact_to_update.phone = request.form['phone']
    contact_to_update.email = request.form['email']

    db.session.commit()

    flash ("Updated success")
    return redirect(url_for('index'))

@app.route('/delete/<id>')
def delete_contact(id):
    data = Contacts.query.filter_by(id=int(id)).delete()
    db.session.commit()
    flash ("Deleted success")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug = True)
