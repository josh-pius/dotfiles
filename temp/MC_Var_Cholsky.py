import numpy as np
import pandas as pd
import datetime as dt
import yfinance as yf
import matplotlib.pyplot as plt
from scipy.stats import norm

# Based on Ryan O'Connell's video https://youtu.be/X8aNFXJEENs?si=OFGziU12nIA1GUne

# Set time range
years=15
endDate =  dt.datetime.now()
startDate = endDate - dt.timedelta(days=365 * years)

# List of tickers
tickers = ['SPY', 'BND', 'GLD', 'QQQ', 'VTI']

adj_close_df = pd.DataFrame()
for ticker in tickers:
    data = yf.download(ticker, start = startDate, end = endDate)
    #print(data.columns)
    adj_close_df[ticker] = data['Close']

#print(adj_close_df)
# Compute daily log returns
log_returns = np.log(adj_close_df/adj_close_df.shift(1))
log_returns = log_returns.dropna()
#print(log_returns)

# Expected returns
def expected_return(weights, log_returns):
    return np.sum(log_returns.mean()*weights)


# Function to compute portfolios standard deviation
def standard_deviation(weights, cov_matrix):
    variance = weights.T @ cov_matrix @ weights
    return np.sqrt(variance)

# Create cov matrix
cov_matrix = log_returns.cov()
#print(cov_matrix)

# --- Correlated Monte Carlo via Cholesky ---

# Vector of daily means (log-return) and daily covariance matrix
mu_vec = log_returns.mean().values                  # shape (n,)
Sigma  = cov_matrix.values                          # shape (n,n)

# Cholesky factor of daily covariance (Sigma = L @ L.T)
try:
        L = np.linalg.cholesky(Sigma)
except np.linalg.LinAlgError:
    # tiny jitter if numerical issues
    eps = 1e-12
    for _ in range(8):
        try:
            L = np.linalg.cholesky(Sigma + np.eye(Sigma.shape[0]) * eps)
            break
        except np.linalg.LinAlgError:
            eps *= 10
    else:
        raise

# Monte Carlo draws: independent standard normals, then correlate
simulations = 10000
Z = np.random.normal(size=(len(tickers), simulations))     # iid N(0,1)
Y = L @ Z                                                  # correlated shocks; Cov(Y)=Sigma

# Multi-asset return scenarios over 'days'
# log-returns are additive in time: mean scales by days, covariance by sqrt(days)
days=6
R = (mu_vec[:, None] * days) + (Y * np.sqrt(days))         # shape (n, sims)

# Create equally weighted portfolio and find total portfolio expected returns
portfolio_value = 100000
weights = np.array([1/len(tickers)]*len(tickers))
portfolio_expected_returns = expected_return(weights,log_returns)
portfolio_std_dev = standard_deviation(weights, cov_matrix)

# Portfolio return scenarios and $ P&L
port_ret = weights @ R                                     # shape (sims,)
scenarioReturn = portfolio_value * port_ret

# VaR
confidence_interval = 0.95
VaR = -np.percentile(scenarioReturn, 100 * (1 - confidence_interval))
print(VaR)

# Plot
plt.hist(scenarioReturn, bins=50, density=True)
plt.xlabel('Scenario Gain/loss ($)')
plt.ylabel('Frequency')
plt.title(f'Distribution of Portfolio Gain/Loss over {days} Days')
plt.axvline(-VaR, linestyle='dashed', linewidth=2,
                    label=f'VaR at {confidence_interval:0%} confidence level')
plt.legend()
plt.show()


