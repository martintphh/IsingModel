import numpy as np

def find_burn_in(observable, expectation_value, sigma, window=250):
    lower = expectation_value - sigma
    upper = expectation_value + sigma

    for i in range(window, len(observable)):
        window_slice = observable[i-window:i]
        if ((window_slice >= lower) & (window_slice <= upper)).all():
            return i  #erster index ab dem es stabil ist

    return None 


def moving_average(data, window):
    return np.convolve(data, np.ones(window) / window, mode="valid")