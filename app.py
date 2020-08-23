from flask import Flask, render_template, request, redirect, jsonify
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from apic_info import APIC_INFORMATION, give_credentials


app = Flask(__name__)
app.config['SECRET_KEY'] = 'akdsfjq340jf9q34ifk43fq439f'


class ACI_inputForm(FlaskForm):
    location = SelectField('Select the Location', choices=[
                           ('SVL', 'SVL-Fabric'), ('RTP', 'RTP-Fabric')])
    fabric = SelectField('Select the Fabric', choices=[('SVL-FAB7', 'SVL Fabric 7'),
                                                       ('RTP1-FAB1', 'RTP Fabric 1'),
                                                       ('RTP1-FAB3', 'RTP Fabric 3')])
    submit = SubmitField("Fetch")


@ app.route('/', methods=['GET', 'POST'])
def index():
    form = ACI_inputForm()
    if request.method == 'POST' and form.validate():
        location = form.location.data
        fabric = form.fabric.data
        cred = give_credentials(location, fabric)
        return render_template('dataout.html', cred=cred)
    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
