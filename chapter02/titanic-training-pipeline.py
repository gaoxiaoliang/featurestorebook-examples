import hopsworks
from hopsworks.hsfs.builtin_transformations import label_encoder
import pdb

project = hopsworks.login()
fs = project.get_feature_store()
titanic_fg = fs.get_feature_group(name="titanic", version=1)
#pdb.set_trace()
selected_features = titanic_fg.select_features()

feature_view = fs.get_or_create_feature_view(
    name="titanic",
    version=1,
    description="Read from Titanic Passengers Dataset",
    labels=["survived"],
    transformation_functions=[label_encoder("sex"), label_encoder("embarked")],
    query=selected_features,
)

X_train, X_test, y_train, y_test = feature_view.train_test_split(0.2)

import xgboost as xgb
model = xgb.XGBClassifier()
model.fit(X_train, y_train.values.ravel())
y_pred = model.predict(X_test)

from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
metrics = classification_report(y_test, y_pred, output_dict=True)
results = confusion_matrix(y_test, y_pred)

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
df_cm = pd.DataFrame(results, ['True Deceased', 'True Survivor'], ['Pred Deceased', 'Pred Survivor'])
cm = sns.heatmap(df_cm, annot=True)
fig = cm.get_figure()
plt.show()



mr = project.get_model_registry()
model_dir = 'titanic_model'
import os
if os.path.isdir(model_dir) == False:
    os.mkdir(model_dir)
images_dir = model_dir + '/images'
if os.path.isdir(images_dir) == False:
    os.mkdir(images_dir)
    
model.get_booster().save_model(model_dir + '/titanic_model.json')
fig.savefig(images_dir + '/confusion_matrix.png')

titanic_model = mr.python.create_model(
        name='titanic',
        metrics={'accuracy': metrics['accuracy'],
                 'f1 score': metrics['weighted avg']['f1-score']},
        feature_view=feature_view,
        description='Titanic Survivor Predictor'
        )

titanic_model.save(model_dir)
