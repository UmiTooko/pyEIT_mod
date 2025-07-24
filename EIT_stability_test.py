import numpy as np


# Read and parse the file
filename = 'data/_perforrmance_diff.txt'

Input = []  # To hold all flattened frames

with open(filename, 'r') as file:
    current_frame = []
    for line in file:
        line = line.strip()
        if line == 's':
            if current_frame:
                Input.append(current_frame)
                current_frame = []
        else:
            numbers = [float(num) for num in line.split()]
            current_frame.extend(numbers)
    if current_frame:  # Append the last frame
        Input.append(current_frame)


print(Input)

Input = np.array(Input)  # shape: (num_frames, 208)

# Validate dimensions
assert Input.shape[1] == 208, f"Each frame must have 208 values, found {Input.shape[1]}"
# Extract by column (index 0 to 207)
ExtractData = [Input[:, i] for i in range(208)]  # list of arrays, one for each index
print(ExtractData)

#Calculated Means

ExtractData = np.array(ExtractData)

# Calculate mean and variance across each row (i.e., across frames)
means = np.mean(ExtractData, axis=1)       # shape: (208,)
variances = np.var(ExtractData, axis=1)    # shape: (208,)




# Caluculate SNRs
SNRs = 20 * np.log10(means / variances)
SNRs = np.round(SNRs, 7)
print(SNRs)







# Example shape
rows, cols = 16, 13  # 

# Assuming means and variances are already 1D numpy arrays of length 208
# Convert them into 2D format
means_2d = means.reshape((rows, cols))
variances_2d = variances.reshape((rows, cols))
SNRs_2d = SNRs.reshape((rows, cols))

# Open file to write
with open("mean_variance_matrix.txt", "w") as f:
    f.write("Mean Values\n")
    f.write("-" * 80 + "\n")
    for row in means_2d:
        f.write("  ".join(f"{val:7.6f}" for val in row) + "\n")

    f.write("\nVariance Values\n")
    f.write("-" * 80 + "\n")
    for row in variances_2d:
        f.write("  ".join(f"{val:7.6f}" for val in row) + "\n")


    f.write("\nSNRs Values\n")
    f.write("-" * 80 + "\n")
    for row in SNRs_2d:
        f.write("  ".join(f"{val:7.6f}" for val in row) + "\n")






