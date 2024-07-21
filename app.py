from flask import Flask, render_template, request, jsonify
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import DataRequired
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

# Load dataset
main_df = pd.read_csv('final_merged_data.csv')

# Exclude air fryers with NaN values in 'Price' and 'Suitable for number of people' columns
main_df = main_df.dropna(subset=['Price', 'Suitable for number of people'])

# Updated energy provider tariffs (in EUR per kWh)
energy_providers = {
    'Vattenfall': 0.33,
    'Budget Energie': 0.331,
    'Eneco': 0.304,
    'Engie': 0.294,
    'Essent': 0.38,
    'Greenchoice': 0.35,
    'Innova Energie': 0.29,
    'Oxxio': 0.34,
    'UnitedConsumers': 0.32,
    'Pure Energie': 0.31,
    'Vandebron': 0.33,
    'Coolblue Energie': 0.246,
    'Mega': 0.28,
    'Frank Energie': 0.29,
    'Clean Energy': 0.32,
    'Tibber': 0.30,
    'NextEnergy': 0.29,
    '365energie': 0.31,
    'NoordEnergie': 0.28,
    'Powerpeers': 0.33,
    'Vrijopnaam': 0.31
}

# Helper function to classify energy label
def energy_label(power):
    if 0.5 <= power < 1:
        return "A++"
    elif 1 <= power < 1.3:
        return "A+"
    elif 1.3 <= power <= 1.5:
        return "A"
    elif 1.5 < power < 2:
        return "B+"
    elif 2 <= power < 2.5:
        return "B"
    else:
        return "C"

# Helper function to calculate payback period and monthly savings after payback period
def calculate_payback_period_and_savings(price_recommendation, power_difference, tariff, usage_per_week):
    if power_difference == 0:
        return None, None, None
    weekly_savings = power_difference * usage_per_week
    monthly_savings = weekly_savings * 4  # 4 weeks in a month
    monthly_cost_savings = monthly_savings * tariff
    payback_period_months = price_recommendation / monthly_cost_savings
    years = int(payback_period_months // 12)
    months = int(payback_period_months % 12)
    return years, months, monthly_cost_savings

# Helper function to generate tags
def generate_tags(search_row, rec_row):
    tags = []
    if rec_row['Number of programs'] > search_row['Number of programs']:
        tags.append("Number of programs")
    if rec_row['Cord length'] > search_row['Cord length']:
        tags.append("Cord length")
    if rec_row['Product weight'] < search_row['Product weight']:
        tags.append("Product weight")
    if rec_row['Contents'] > search_row['Contents']:
        tags.append("Contents")
    if rec_row['Factory warranty term'] > search_row['Factory warranty term']:
        tags.append("Factory warranty term")
    if rec_row['Introduction'] > search_row['Introduction']:
        tags.append("Introduction")
    if rec_row['Price'] < search_row['Price']:
        tags.append("Price")
    if rec_row['Power'] < search_row['Power']:
        tags.append("Power")

    return tags

class ApplianceForm(FlaskForm):
    energy_provider = SelectField('Select your energy provider', choices=list(energy_providers.keys()), validators=[DataRequired()])
    usage_frequency = SelectField('How much do you use your airfryer?', choices=['1-7 times a week', 'A few times a month', 'Rarely'], validators=[DataRequired()])
    usage_per_week = SelectField('Select usage per week', choices=[str(i) for i in range(1, 8)], default='3')
    search_model = StringField('Search for a model', validators=[DataRequired()])
    selected_model = StringField('Selected model')
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = ApplianceForm()
    selected_model = None
    search_model = None
    recommendations = None
    suitable_for = None
    matched_airfryer = pd.DataFrame()
    matched_airfryer_data = {}
    recommendations_data = []

    if form.validate_on_submit():
        energy_provider = form.energy_provider.data
        usage_frequency = form.usage_frequency.data
        usage_per_week = int(form.usage_per_week.data)
        search_model = form.search_model.data
        selected_model = form.selected_model.data

        if selected_model:
            matched_airfryer = main_df[main_df['Model'] == selected_model]
            if not matched_airfryer.empty:
                row = matched_airfryer.iloc[0]
                energy_label_value = energy_label(row['Power'])

                yearly_cost = row['Power'] * usage_per_week * 52 * energy_providers[energy_provider]
                matched_airfryer_data = {
                    'model': ' '.join(row['Model'].split()[:3]),
                    'price': row['Price'],
                    'total_score': row['Total Score'],
                    'power': row['Power'],
                    'energy_label': energy_label_value,
                    'yearly_cost': f"{yearly_cost:.2f}",
                    'link': row['Link']
                }

                if energy_label_value not in ["A++", "A+", "A"]:
                    suitable_for = row['Suitable for number of people']
                    recommendations = main_df[(main_df['Suitable for number of people'] == suitable_for) &
                                              (main_df['Model'] != row['Model']) &
                                              (main_df['Total Score'] > row['Total Score']) &
                                              (main_df['Power'] < row['Power']) &
                                              (main_df['Price'] < row['Price']) &
                                              (main_df['Power'] != 0) & (main_df['Price'] != 0)]

                    recommendations = recommendations.drop_duplicates(subset=['Model']).sort_values(by=['Total Score', 'Power', 'Price'], ascending=[False, True, True]).head(3)

                    if recommendations.empty:
                        recommendations = main_df[(main_df['Suitable for number of people'] == suitable_for) &
                                                  (main_df['Model'] != row['Model']) &
                                                  (main_df['Power'] < row['Power']) &
                                                  (main_df['Price'] < row['Price']) &
                                                  (main_df['Power'] != 0) & (main_df['Price'] != 0)]

                        recommendations = recommendations.drop_duplicates(subset=['Model']).sort_values(by=['Total Score', 'Power', 'Price'], ascending=[False, True, True]).head(3)

                    for _, rec_row in recommendations.iterrows():
                        power_difference = row['Power'] - rec_row['Power']
                        years, months, monthly_savings = calculate_payback_period_and_savings(rec_row['Price'], power_difference, energy_providers[energy_provider], usage_per_week)
                        yearly_cost_rec = rec_row['Power'] * usage_per_week * 52 * energy_providers[energy_provider]
                        recommendations_data.append({
                            'model': ' '.join(rec_row['Model'].split()[:3]),
                            'price': rec_row['Price'],
                            'total_score': rec_row['Total Score'],
                            'power': rec_row['Power'],
                            'energy_label': energy_label(rec_row['Power']),
                            'yearly_cost': f"{yearly_cost_rec:.2f}",
                            'payback_period': f"{years} years, {months} months",
                            'monthly_savings': f"{monthly_savings:.2f}",
                            'link': rec_row['Link'],
                            'tags': generate_tags(row, rec_row)
                        })

    return render_template('index.html', form=form, energy_providers=energy_providers, matched_airfryer_data=matched_airfryer_data, recommendations_data=recommendations_data, suitable_for=suitable_for)

@app.route('/search_model', methods=['POST'])
def search_model():
    search_model = request.form.get('search_model')
    filtered_df = main_df[main_df['Model'].str.contains(search_model, case=False, na=False) & (main_df['Power'] != 0)]
    matching_models = filtered_df[['Model', 'Image']].drop_duplicates().head(3).to_dict(orient='records')
    return jsonify(matching_models)

if __name__ == '__main__':
    app.run(debug=True)
