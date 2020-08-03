#This program implements a kalman filter to a 1 dimension move
# update is a function that sense (gain information)
# predict is function that represents robot move (loss information)

def update(mean1, var1, mean2, var2):
    """ 
    Inputs:
        mean1: this is a priori distribution mean.
        var1: variance of the priori distribution
        mean2: mean of the distribution probability that the 
        measurement is z given x (P (z | x))
        var2: variance of the distribution probability 
        that the measurement is z given x (P (z | x))
    Output:
        A list with new values to represent the posterior 
        distribution of probability after sense
    """
    new_mean = float(var2 * mean1 + var1 * mean2) / (var1 + var2)
    new_var = 1./(1./var1 + 1./var2)
    return [new_mean, new_var]

def predict(mean1, var1, mean2, var2):
    """ 
    Inputs:
        mean1: this is a priori distribution mean.
        var1: variance of the priori distribution
        mean2: mean of the distribution probability that the 
        measurement is z given x (P (z | x))
        var2: variance of the distribution probability 
        that the measurement is z given x (P (z | x))
    Output:
        A list with new values to represent the posterior 
        distribution of probability after move
    """
    new_mean = mean1 + mean2
    new_var = var1 + var2
    return [new_mean, new_var]

# Test
measurements = [5., 6., 7., 9., 10.] 
motion = [1., 1., 2., 1., 1.]
measurement_sig = 4. # variance of measurement
motion_sig = 2. # variance of motion
mu = 0. # Initial mean
sig = 10000. # Initial variance

for measurement, move  in zip(measurements, motion):
    [mu, sig] = update(mu, sig, measurement, measurement_sig)
    [mu, sig] = predict(mu, sig, move, motion_sig)

print [mu, sig]
