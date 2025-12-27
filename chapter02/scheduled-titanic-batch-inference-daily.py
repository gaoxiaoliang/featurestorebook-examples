import hopsworks

project = hopsworks.login()
fs = project.get_feature_store()
mr = project.get_model_registry()
model_reg = mr.get_model('titanic', version=1)
feature_view = model_reg.get_feature_view()
feature_view.init_batch_scoring(training_dataset_version=1)
batch_data = feature_view.get_batch_data()
model_dir = model_reg.download()

import xgboost as xgb
booster = xgb.Booster()
booster.load_model(model_dir + '/titanic_model.json')
model = xgb.XGBClassifier()
model._Booster = booster
model._le = None

y_pred = model.predict(batch_data)
passenger_survived = y_pred[y_pred.size-1]
passenger_details = batch_data.iloc[-1]
def remove_last_line_from_string(s):
    return s[:s.rfind('\n')]
passenger_details = remove_last_line_from_string(str(passenger_details))

with open(f'titanic.html', 'a', newline='\n') as file:
    file.write('<h2>Predicted passenger</h2>')
    file.write('<pre>')
    file.write(passenger_details)
    file.write('</pre>')
    img = 'titanic_' + str(passenger_survived) + '.jpg'
    file.write(f'<img src="{img}" style="max-width:80%; height:auto;"/>')

