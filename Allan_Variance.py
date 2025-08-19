import numpy as np
import matplotlib.pyplot as plt

def read_frames(filename):
    frames = []
    current = []

    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if line == "s":  # new frame
                if current:
                    frames.append(np.array(current, dtype=float))
                    current = []
            elif line:  # non-empty row
                current.append([float(x) for x in line.split()])
        # Add last frame if not closed
        if current:
            frames.append(np.array(current, dtype=float))

    return frames

def mean_matrix(frames):
    stacked = np.stack(frames, axis=0)  # shape: (n_frames, rows, cols)
    return stacked.mean(axis=0)


def allan_variance(data, tau0, max_num_clusters=None):
    """
    Compute Allan variance for a given time series.

    Parameters
    ----------
    data : array-like
        Input time series (frequency deviations, angular rate, etc).
    tau0 : float
        Base sampling period (time between data points).
    max_num_clusters : int, optional
        Max number of averaging times to consider (default: length//2).

    Returns
    -------
    tau : ndarray
        Averaging times.
    adev : ndarray
        Allan deviation (sqrt of Allan variance).
    """

    N = len(data)
    if max_num_clusters is None:
        max_num_clusters = N // 2

    # Possible cluster sizes
    m_values = np.logspace(0, np.log10(max_num_clusters), num=50, dtype=int)
    m_values = np.unique(m_values)  # remove duplicates
    print(m_values)
    adev = []
    tau = []

    for m in m_values:
        if m < 1 or 2*m >= N:
            continue

        # Cluster averages
        cluster_avg = np.array([np.mean(data[i:i+m]) for i in range(0, N-m+1, m)])
        
        # Allan variance formula
        diff_sq = np.diff(cluster_avg)**2
        allan_var = 0.5 * np.mean(diff_sq)

        adev.append(np.sqrt(allan_var))
        tau.append(m * tau0)

    return np.array(tau), np.array(adev)


if __name__ == "__main__":
    
    # Length of the 1D matrix
    n = 100000

    # Step 1: initialize with all 3s
    arr = np.full(n, 3.0)

    # Step 2: random multipliers between 0.5 and 1.5
    multipliers = np.random.uniform(0.9,1.1, size=n)

    # Step 3: elementwise multiply
    IdealData = arr * multipliers

    print(IdealData)




    # === 1. Simulate synthetic data (white noise + random walk) ===
    np.random.seed(0)
    N = 10000  # number of samples
    tau0 = 1.0  # base sampling time (s)
    # Read and parse the file
    filename = 'data/stability.txt'
    frames = read_frames(filename)
    frames = np.array(frames)
    print(frames)
    print("============================")
    print(frames[0,0,0])
    


    reshaped = frames.reshape(frames.shape[0], -1)  # (4, 9)

# Step 2: transpose to get desired orientation
    signals = reshaped.T 
    avg_signals = []
    print("00000000000000000000000000000000000000000")
    for i in range(len(signals)):
        avg_signals.append(np.mean(signals[i]))

    ## White Gaussian noise
    #white_noise = np.random.normal(0, 1e-3, N)

    ## Random walk noise (integrated white noise)
    #random_walk = np.cumsum(np.random.normal(0, 1e-5, N))

    ## Combined signal
    #signal = white_noise + random_walk
    #plt.plot(signal)
    #plt.show()
    # === 2. Compute Allan deviation ===
    tau, adev = allan_variance(avg_signals, tau0)
    log_tau = np.log10(tau)
    log_adev = np.log10(adev)

    # Local slopes between adjacent log-log points
    slopes = np.diff(log_adev) / np.diff(log_tau)

    # Measure fluctuation of slopes
    slope_std = np.std(slopes)
    print("Slope fluctuation (std):", slope_std)

    # === 3. Plot result ===
    plt.figure(figsize=(8, 6))
    plt.loglog(tau, adev, "o-", label="Allan Deviation")
    plt.xlabel("Averaging Time $\\tau$ [s]")
    plt.ylabel("Allan Deviation")
    plt.title("Allan Deviation Example (synthetic data)")
    plt.grid(True, which="both", ls="--")
    plt.legend()
    plt.show()
