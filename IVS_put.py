# Import libraries
import numpy as np
import scipy.stats as si
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.optimize import minimize

# Black-Scholes model
def black_scholes_put(S, X, t, r, sigma):
    d1 = (np.log(S / X) + (r + 0.5 * sigma ** 2) * t) / (sigma * np.sqrt(t))
    d2 = d1 - sigma * np.sqrt(t)
    return X * np.exp(-r * t) * si.norm.cdf(-d2) - S * si.norm.cdf(-d1)

def implied_volatility(P, S, X, t, r):
    """Numerically solve for implied volatility."""
    func = lambda sigma: (black_scholes_put(S, X, t, r, sigma) - P) ** 2
    result = minimize(func, x0=0.2, bounds=[(0.01, 3.0)])
    return result.x[0] if result.success else np.nan

# Default parameters
S = 100 
r = 0.05 
P = 10 

S_min = 0.80
S_max = 1.20
t_max = 1.0

# Define ranges for strike prices and expirations
X_values = np.linspace(S_min * S, S_max * S, 20)
T_values = np.linspace(0.1, t_max, 20)

# Compute implied volatilities
implied_vols = np.zeros((len(X_values), len(T_values)))
for i, X in enumerate(X_values):
    for j, t in enumerate(T_values):
        implied_vols[i, j] = implied_volatility(P, S, X, t, r)

# Create 3D plot
X_mesh, T_mesh = np.meshgrid(T_values, X_values)
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(T_mesh, X_mesh, implied_vols, cmap='viridis')
ax.set_xlabel('Strike Price (X)')
ax.set_ylabel('Time to Expiration (t)')
ax.set_zlabel('Implied Volatility')
ax.set_title('Implied Volatility Surface')
plt.show()
