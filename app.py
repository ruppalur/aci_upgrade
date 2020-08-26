from flask import Flask, render_template, request, redirect, jsonify
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, SelectMultipleField
from apic_info import APIC_INFORMATION, give_credentials
from apic_data import fabricChoices, leaf_choices, locationChoices


app = Flask(__name__)
app.config['SECRET_KEY'] = 'akdsfjq340jf9q34ifk43fq439f'


class ACI_inputForm(FlaskForm):
    location = SelectField('Select the Location', choices=locationChoices)
    fabric = SelectField('Select the Fabric', choices=fabricChoices)
    leafs = SelectMultipleField(choices=leaf_choices, default=['1011', '1021'])
    submit = SubmitField("Fetch")


@ app.route('/', methods=['GET', 'POST'])
def index():
    form = ACI_inputForm()
    if request.method == 'POST' and form.validate():
        location = form.location.data
        fabric = form.fabric.data
        leafs = form.leafs.data
        cred = give_credentials(location, fabric, leafs)
        return render_template('dataout.html', **cred)
    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
