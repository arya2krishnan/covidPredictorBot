import numpy as np
import pandas as pd
from sklearn import linear_model

from sympy import *

# Make numpy printouts easier to read.
np.set_printoptions(precision=3, suppress=True)


def predictor():
    # initialize dataframe for prediction model
    df = pd.read_csv('https://api.covidtracking.com/v1/us/daily.csv')
    positive_increase_change = []
    for i in range(len(df.index) - 1):
        positive_increase_change.append(df['positiveIncrease'].tolist()[i] - df['positiveIncrease'].tolist()[i + 1])
    positive_increase_change.append(0)

    df.insert(3, 'positiveIncreaseDifference', positive_increase_change, True)
    df = df[df['date'] >= 20200401]

    def add_num_days_col():
        """Adds a column to dataframe with days for later calculations"""
        days = []
        for i in range(len(df.index)):
            days.append(i + 1)
        days.reverse()
        df.insert(0, "days", days, True)

    add_num_days_col()
    df.dropna()

    # creating training and eval set
    train_dataset = df.copy()
    test_dataset = df.loc[:14, :]

    train_features = train_dataset.copy()

    train_features = train_features[
        ['positiveIncrease', 'pending', 'positiveIncreaseDifference', 'positive', 'hospitalizedCurrently',
         'hospitalizedIncrease']]

    train_labels = train_features.pop('positiveIncrease')

    regr = linear_model.LinearRegression()
    regr.fit(train_features, train_labels)
    intercept = regr.intercept_
    coef = regr.coef_


    # prediction with sklearn
    result = 0
    rand_range = np.random.choice(range(10, 14))
    for i in range(rand_range):
        New_Positive_Increase_Difference = train_dataset['positiveIncreaseDifference'][i]
        New_pending = train_dataset['pending'][i]
        New_Positive = train_dataset['positive'][i]
        New_hospitalized = train_dataset['hospitalizedCurrently'][i]
        New_hospitalized_inc = train_dataset['hospitalizedIncrease'][i]
        result += regr.predict([[New_Positive_Increase_Difference, New_pending, New_Positive, New_hospitalized,
                                 New_hospitalized_inc]])[0]

    result_mean = result / rand_range

    x_1 = df.loc[:, 'days'].values
    y_1 = df.loc[:, 'positive'].values
    y_2 = df.loc[:, 'recovered'].values

    z1 = np.polyfit(x_1, y_1, 2)
    z2 = np.polyfit(x_1, y_2, 2)

    x = symbols('x')
    predictions = solve(
        z1[0] * x ** 2 + z1[1] * x + z1[2] - z2[0] * x ** 2 - z2[1] * x - z2[2], x)



    final_predict = predictions[0]



    return round(-final_predict), round(result_mean, 0), \
           train_dataset['positiveIncreaseDifference'][0], train_dataset['pending'][0], \
           train_dataset['hospitalizedIncrease'][0], df['positive'][0]

