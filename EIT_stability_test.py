import numpy as np
import matplotlib.pyplot as plt

def normalized_arr(arr):
    arr = np.array(arr, dtype=float)
    min_val = arr.min()
    max_val = arr.max()
    
    if min_val == max_val:
        # All values are the same → return zeros
        return np.full(len(arr), 0.5)
    else:
        return (arr - min_val) / (max_val - min_val)


# Read and parse the file
filename = 'data/data_v1_ok.txt'

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


Input = np.array(Input)  # shape: (num_frames, 208)
IdealInput = np.tile(Input[0],(100,1))

# Validate dimensions
assert Input.shape[1] == 208, f"Each frame must have 208 values, found {Input.shape[1]}"
# Extract by column (index 0 to 207)
ExtractData = [Input[:, i] for i in range(208)]  # list of arrays, one for each index
ExtractData = np.array(ExtractData)

IdealExtractData = [IdealInput[:, i] for i in range(208)]  # list of arrays, one for each index
IdealExtractData = np.array(IdealExtractData)


if 1:
    NormalizedExtractData = []
    for idx in range(len(ExtractData)):
        ExtractDataMeans = np.mean(ExtractData[idx])
        ExtractDataStd = ExtractData[idx].std(ddof=0)
        NormalizedExtractData.append(ExtractDataStd/ExtractDataMeans)
    # Calculate mean and variance across each row (i.e., across frames)
    means = np.mean(ExtractData, axis=1)       # shape: (208,)
    variances = np.var(ExtractData, axis=1)    # shape: (208,)
    std_devi = np.sqrt(variances)
    noise_mean = np.mean(std_devi)

    SNRs = 20 * np.log10(means / (std_devi+1e-32))    



    fig, ((ax1), (ax2), (ax3), (ax4)) = plt.subplots(4, 1, figsize=(6, 6), sharex=True)

    ax1.set_title("Data")
    ax1.plot(ExtractData, color='green')
    ax1.set_xlim(0,200)
    ax1.set_ylim(-1,3)

    ax2.set_title("Noise's level")
    ax2.plot(NormalizedExtractData, color='pink')
    ax2.set_ylim(-0.1,1)

    ax3.set_title("SNRs")
    ax3.plot(SNRs, color='red')
    ax3.set_ylim(0,50)

    ax4.set_title("Standard Deviation")

    ax4.plot(std_devi, color='blue')
    ax4.set_ylim(-0.1,1.1)



if 1:
    multipliers = [0.95, 0.975, 1.025, 1.05]
    multipliers_ = [0.25, 0.5, 1.5, 1.75]
    NormalizedGoodExtractData = []
    random_factors = np.random.choice(multipliers, size=IdealExtractData.shape)
    GoodExtractData = IdealExtractData*random_factors
    for idx in range(len(GoodExtractData)):
        GoodExtractDataMeans = np.mean(GoodExtractData[idx])
        GoodExtractDataStd = GoodExtractData[idx].std(ddof=0)

        NormalizedGoodExtractData.append(GoodExtractDataStd/GoodExtractDataMeans)

    # Calculate mean and variance across each row (i.e., across frames)
    means = np.mean(GoodExtractData, axis=1)       # shape: (208,)
    variances = np.var(GoodExtractData, axis=1)    # shape: (208,)
    std_devi = np.sqrt(variances)
    noise_mean = np.mean(std_devi) 
    SNRs = 20 * np.log10(means / (std_devi+1e-32))  


    fig, ((ax1), (ax2), (ax3), (ax4)) = plt.subplots(4, 1, figsize=(6, 6), sharex=True)

    ax1.set_title("Data")

    ax1.plot(GoodExtractData, color='green')
    ax1.set_xlim(0,200)
    ax1.set_ylim(-1,3)


    ax2.set_title("Noise's level")
    ax2.plot(NormalizedGoodExtractData, color='pink')
    ax2.set_ylim(0,2)

    ax3.set_title("SNRs")
    ax3.plot(SNRs, color='red')
    ax3.set_ylim(0,50)

    ax4.plot(std_devi, color='blue')
    ax4.set_ylim(-0.1,1.1)


if 1:
    NormalizedIdealExtractData = []
    for idx in range(len(IdealExtractData)):
        IdealExtractDataMeans = np.mean(IdealExtractData[idx])
        IdealExtractDataStd = IdealExtractData[idx].std(ddof=0)

        NormalizedIdealExtractData.append(IdealExtractDataStd/IdealExtractDataMeans)

    print(IdealExtractData)
    # Calculate mean and variance across each row (i.e., across frames)
    means = np.mean(IdealExtractData, axis=1)       # shape: (208,)
    variances = np.var(IdealExtractData, axis=1)    # shape: (208,)
    std_devi = np.sqrt(variances)
    noise_mean = np.mean(std_devi) 

    # Caluculate SNRs
    SNRs = 20 * np.log10(means / (std_devi+1e-32))        
     
    fig, ((ax1), (ax2), (ax3), (ax4)) = plt.subplots(4, 1, figsize=(6, 6), sharex=True)

    ax1.set_title("Data")

    ax1.plot(IdealExtractData, color='green')
    ax1.set_xlim(0,200)
    ax1.set_ylim(-1,3)

    ax2.set_title("Noise's level")
    ax2.plot(NormalizedIdealExtractData, color='pink')
    ax2.set_ylim(-0.1,1.1)

    ax3.set_title("SNRs")
    ax3.plot(SNRs, color='red')
    #ax3.set_ylim(-0.1,1.1)

    ax4.plot(std_devi, color='blue')
    ax4.set_ylim(-0.1,1.1)










                           
       





plt.show()

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






