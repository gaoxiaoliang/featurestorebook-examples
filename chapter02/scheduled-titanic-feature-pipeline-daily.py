import random
import time
import pandas as pd

random.seed(time.time())

def generate_random_passenger(id):
    """
    Returns a single Titanic passenger as a single row in a DataFrame
    """

    survived = False
    pick_random = random.uniform(0,2)
    if pick_random >= 1:
        print("Survivor added")
        survived = True
    else:
        print("Non-Survivor added")

    if survived:
        unif = random.uniform(0, 1)
        if unif < 109/342:
            sex = 'male'
        else:
            sex = 'female'
        if unif < 136/342:
            pclass = 1
        elif unif < 223/342:
            pclass = 2
        else:
            pclass = 3
        age = random.uniform(0.42, 80.0)
        if unif < 25/100:
            fare = random.uniform(0.0, 12.47)
        elif unif < 50/100:
            fare = random.uniform(12.47, 26.0)
        elif unif < 75/100:
            fare = random.uniform(26.0, 57.0)
        else:
            fare = random.uniform(57.0, 512.0)
        if unif < 233/342:
            parch = 0.0
        elif unif < (65+233)/342:
            parch = 1.0
        elif unif < (40+65+233)/342:
            parch = 2.0
        else:
            parch = round(random.uniform(3.0, 5.0))
        if unif < 210/342:
            sibsp = 0.0
        elif unif < (112+210)/342:
            sibsp = 1.0
        else:
            sibsp = round(random.uniform(2.0, 4.0))
        if unif < 219/342:
            embarked = 'S'
        elif unif < (93+210)/342:
            embarked = 'C'
        else:
            embarked = 'Q'
    else:
        unif = random.uniform(0, 1)
        if unif < 468/549:
            sex = 'male'
        else:
            sex = 'female'
        if unif < 80/549:
            pclass = 1
        elif unif < 177/549:
            pclass = 2
        else:
            pclass = 3
        age = random.uniform(1.0, 74.0)
        if unif < 25/100:
            fare = random.uniform(0.0, 7.85)
        elif unif < 50/100:
            fare = random.uniform(7.85, 10.5)
        elif unif < 75/100:
            fare = random.uniform(10.5, 26.0)
        else:
            fare = random.uniform(26.0, 263.0)
        if unif < 445/549:
            parch = 0.0
        elif unif < (53+445)/549:
            parch = 1.0
        elif unif < (40+53+445)/549:
            parch = 2.0
        else:
            parch = round(random.uniform(3.0, 6.0))
        if unif < 398/549:
            sibsp = 0.0
        elif unif < (97+398)/549:
            sibsp = 1.0
        else:
            sibsp = round(random.uniform(2.0, 6.0))
        if unif < 427/549:
            embarked = 'S'
        elif unif < (75+427)/549:
            embarked = 'C'
        else:
            embarked = 'Q'

    df = pd.DataFrame({ "passengerid": id, "sex": [sex], "age": [age], "pclass": [pclass], "fare": [fare],
                       "parch":[round(parch)], "sibsp": [round(sibsp)], "embarked": [embarked]
                      })
    df['survived'] = round(survived)
    return df



import hopsworks

project = hopsworks.login()
fs = project.get_feature_store()
titanic_fg = fs.get_feature_group(name="titanic", version=1)

df = titanic_fg.read()
id = df['passengerid'].max() + 1 
print(f'passengerid: {id}')
titanic_df = generate_random_passenger(id)
titanic_fg.insert(titanic_df, wait=True)

def remove_last_line_from_string(s):
    return s[:s.rfind('\n')]
passenger_details = remove_last_line_from_string(str(titanic_df.iloc[0]))
with open(f'titanic.html', 'w', newline='\n') as file:
    file.write(f'<h2>Generated passenger({"Survivor" if titanic_df.iloc[0].survived == 1 else "Non-Survivor"})</h2>')
    file.write('<pre>')
    file.write(passenger_details)
    file.write('</pre>')
