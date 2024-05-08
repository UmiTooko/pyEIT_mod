import matplotlib.pyplot as plt
import numpy as np

# Assuming 'ds_n' is your NumPy array
ds_n = np.random.normal(0, 1, 1000)  # Example data for demonstration

# Create subplots with shared y-axis
fig, axs = plt.subplots(2, 2, sharey=True, tight_layout=True)

# Plot histogram on the first subplot with its own y-axis
axs[0, 0].hist(ds_n, bins=100, color='blue')
axs[0, 0].set_title('Histogram')

# Create a twin y-axis for the first subplot
axs_twin = axs[0, 0].twinx()
axs_twin.set_ylabel('Frequency (twin)')

# Plot cumulative histogram on the second subplot with its own y-axis
axs[0, 1].hist(ds_n, bins=100, color='green', cumulative=True)
axs[0, 1].set_title('Cumulative Histogram')

# Create a twin y-axis for the second subplot
axs_twin = axs[0, 1].twinx()
axs_twin.set_ylabel('Cumulative Frequency (twin)')

# Plot probability density function (PDF) on the third subplot with its own y-axis
axs[1, 0].hist(ds_n, bins=100, color='red', density=True)


plt.show()