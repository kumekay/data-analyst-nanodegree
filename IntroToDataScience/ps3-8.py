import numpy as np
import pandas
from ggplot import *
import scipy
import statsmodels.api as sm

"""
In this question, you need to:
1) implement the compute_cost() and gradient_descent() procedures
2) Select features (in the predictions procedure) and make predictions.

"""

def normalize_features(df):
    """
    Normalize the features in the data set.
    """
    mu = df.mean()
    sigma = df.std()

    if (sigma == 0).any():
        raise Exception("One or more features had the same value for all samples, and thus could " + \
                         "not be normalized. Please do not include features with only a single value " + \
                         "in your model.")
    df_normalized = (df - df.mean()) / df.std()

    return df_normalized, mu, sigma

def compute_cost(features, values, theta):
    """
    Compute the cost function given a set of features / values,
    and the values for our thetas.

    This can be the same code as the compute_cost function in the lesson #3 exercises,
    but feel free to implement your own.
    """
    m = len(values)
    h = np.dot(features,theta)
    cost = np.square(h - values).sum()/(2*m)
    grad = np.dot(h-values,features)/m;
    return cost, grad

def predictions(weather_turnstile):


    features = weather_turnstile[['rain', 'fog', 'Hour', 'mintempi']]
    features['mintempi2'] = features['mintempi']**2

    values = weather_turnstile['ENTRIESn_hourly']

    m = len(values)

    # Add UNIT to features using dummy variables
    dummy_units = pandas.get_dummies(weather_turnstile['UNIT'], prefix='unit')
    features = features.join(dummy_units)


    features, mu, sigma = normalize_features(features)
    features['ones'] = np.ones(m) # Add a column of 1s (y intercept)

    # Convert features and values to numpy arrays
    features_array = np.array(features)
    values_array = np.array(values)

    # Set values for alpha, number of iterations.
    # alpha = 0.1 # please feel free to change this value
    # num_iterations = 75 # please feel free to change this value

    # Initialize theta, perform gradient descent
    theta= np.zeros(len(features.columns))
    # theta_gradient_descent, cost_history = gradient_descent(features_array,
                                                            # values_array,
                                                            # theta_gradient_descent,
                                                            # alpha,
                                                            # num_iterations)

    cost = lambda theta: compute_cost(features_array, values_array, theta)

    theta, nfeval, rc = scipy.optimize.fmin_tnc(cost, theta)

    prediction = np.dot(features_array, theta)
    r_squared = 1 - np.sum((values_array - prediction)**2)/np.sum((values_array-np.mean(values_array))**2)
    return prediction, r_squared


if __name__ == "__main__":
    f = open('turnstile_data_master_with_weather.csv', 'r')
    df = pandas.read_csv(f)
    prediction, r_squared = predictions(df)
    print r_squared
