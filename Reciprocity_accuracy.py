import numpy as np

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


def symmetry_diff_percentage(matrix):
    rows, cols = matrix.shape
    diffs = []

    for i in range(cols // 2):
        left = matrix[:, i]
        right = matrix[:, -(i+1)]
        print("At line {}: Left: {}, Right: {}".format(i, left, right))
        # difference relative to average of the pair
        diff = np.abs(left - right) / ((left + right) / 2) * 100
        print(diff)
        diffs.append(diff)

    return np.array(diffs).T  # shape: (rows, cols//2)


if __name__ == "__main__":
    # === change this to your txt file path ===
    filename = "data/stability.txt"

    # Step 1: read all frames
    frames = read_frames(filename)

    # Step 2: mean matrix
    mean_mat = mean_matrix(frames)

    # Step 3: calculate symmetry difference
    diff_matrix = symmetry_diff_percentage(mean_mat)

    # Show results
    np.set_printoptions(precision=2, suppress=True)
    print("Mean matrix:\n", mean_mat)
    print("\nSymmetry difference (%):\n", diff_matrix)
