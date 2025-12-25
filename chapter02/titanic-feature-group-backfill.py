import pandas as pd

# Load the Titanic dataset and keep only the relevant columns
titanic_df = pd.read_csv('titanic.csv')
titanic_df = titanic_df[['PassengerId', 'Sex','Age','Pclass','Fare','Parch','SibSp','Embarked', 'Survived']]
# Handle missing values: fill missing Age with the mean and missing Embarked with the most frequent value
def_values = {'Age': titanic_df['Age'].mean(), 'Embarked': titanic_df['Embarked'].value_counts().idxmax()}
titanic_df = titanic_df.fillna(value=def_values)



import hopsworks

project = hopsworks.login(engine='Python')
fs = project.get_feature_store()
titanic_fg = fs.get_or_create_feature_group(
        name='titanic',
        version=1,
        primary_key=['PassengerId'],
        description="Titanic passengers dataset"
)
titanic_fg.insert(titanic_df, wait=True)
