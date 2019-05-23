import numpy as np
from scipy.optimize import minimize
import warnings
import sys

NLS_ERROR_TOL = 1e-5
SHORT_END_TOL = 0.0025


class NS(object):

    '''Nelson-Siegel class
    takes time to maturity x and yield y as inputs
    whet called returns a function NS,
    which itself returns fitted values of yields
    for a given time(times) to maturity
    '''

    def __init__(self, x_fit, y_fit, curve_type='ns'):
        self.x = np.array(x_fit)
        self.y = np.array(y_fit)
        self.curve_type = curve_type
        self.ns_params = self.fit_ns()

    def __call__(self, x_new):
        return self.y_ns(x_new, self.ns_params)

    def y_ns(self, x, params):

        '''Nelson-Siegel(-Svensson) function
        '''

        beta_0 = params[0]
        beta_1 = params[1]
        beta_2 = params[2]
        tau = params[3]
        t = x / tau
        if t.any() == 0:
            Y = beta_0 + beta_1
        else:
            Y = beta_0
            Y += beta_1 * (1 - np.exp(-t)) / t
            Y += beta_2 * ((1 - np.exp(-t)) / t - np.exp(-t))
            if len(params) == 6:
                beta_3 = params[4]
                tau_2 = params[5]
                t_2 = x / tau_2
                Y += beta_3 * ((1 - np.exp(-t_2)) / t_2 - np.exp(-t_2))
        return Y

    def nls(self, params):

        '''Sum of squared residuals
        for Non-linear least squares estimation
        of NS(S) function parameters
        '''

        Y_fit = list(map(lambda x: self.y_ns(x, params), self.x))
        eps = np.sum(list(map(lambda i: (Y_fit[i] - self.y[i]) ** 2, range(len(Y_fit)))))
        return eps

    def fit_ns(self):

        '''Estimation of NS(S) curve parameters
        '''

        if self.curve_type == 'ns':
            params = minimize(self.nls, [0, 0, 0, 1]).x
        elif self.curve_type == 'nss':
            params = minimize(self.nls, [0, 0, 0, 1, 0, 1]).x
        if self.nls(params) > NLS_ERROR_TOL:
            warnings.warn('###The yield curve is fitted with large errors###')
        if abs(params[0] + params[1] - self.y[0]) > SHORT_END_TOL:
            warnings.warn('###The yield curve is badly fitted on the short end###')
        return params
