from flask import Flask, render_template, request, redirect, url_for, flash, session
import requests
import secrets  
import os  

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

MAILGUN_API_KEY = os.getenv('MAILGUN_API_KEY')
MAILGUN_DOMAIN = os.getenv('MAILGUN_DOMAIN')
FIXED_RECIPIENTS = os.getenv('FIXED_RECIPIENTS')

def send_simple_message(name, message):
    response = requests.post(
        f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
        auth=("api", MAILGUN_API_KEY),
        data={
            "from": f"Excited User <mailgun@{MAILGUN_DOMAIN}>",
            "to": FIXED_RECIPIENTS,
            "subject": f"Hello {name}!",
            "text": f"Hi {name},\n\n{message}"
        }
    )
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")
    return response

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
       
        response = send_simple_message(name, "Obrigado pelo submit na aula 70!")
        if response.status_code == 200:
            flash('Email enviado!', 'Sucesso')
        else:
            flash('Falha ao enviar e-mail. Por favor, tente mais tarde.', 'Perigo')
        session['name'] = name
        return redirect(url_for('index'))

    name = session.get('name', None)
    return render_template('index.html', name=name)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
