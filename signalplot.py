import numpy as np
from matplotlib import pyplot as plt

def main():
    fig, axes = plt.subplots(3,1,tight_layout=True)
    v0 = np.loadtxt('data/ref_data.txt').flatten()
    v1 = np.loadtxt('data/diff_data.txt').flatten()
    v2 = v1 - v0
    t = np.linspace(0,208,208)
    print(v0)
    print(t)
    axes[0].set_ylim(0,7)
    axes[1].set_ylim(0,7)
    axes[2].set_ylim(-3,3)

    axes[0].set_ylabel('Voltage (V)')
    axes[1].set_ylabel('Voltage (V)')
    axes[2].set_ylabel('Voltage (V)')

    axes[0].set_xlabel('Measurement counts')
    axes[1].set_xlabel('Measurement counts')
    axes[2].set_xlabel('Measurement counts')
    
    axes[0].title.set_text('(a) Refference Voltage | V0')
    axes[1].title.set_text('(b) Difference Voltage | V1')
    axes[2].title.set_text('(c) V1 - V0')
    
    axes[0].plot(t,v0)
    axes[1].plot(t,v1)
    axes[2].plot(t,v2)
    plt.show()
    return





















def box_blur(image):
    """
    Apply a 3x3 box blur to a grayscale image.

    Parameters:
        image (list of lists): A 2D list representing a grayscale image.

    Returns:
        list of lists: A 2D list with the blurred image.
    """
    height = len(image)
    width = len(image[0])

    # Create a new image initialized to zero
    blurred_image = [[0 for _ in range(width)] for _ in range(height)]

    # Apply the box blur
    for i in range(1, height - 1):
        for j in range(1, width - 1):
            window_sum = (
                image[i - 1][j - 1] + image[i - 1][j] + image[i - 1][j + 1] +
                image[i][j - 1] + image[i][j] + image[i][j + 1] +
                image[i + 1][j - 1] + image[i + 1][j] + image[i + 1][j + 1]
            )
            blurred_image[i][j] = window_sum // 9

    return blurred_image



def sobel_filter(image):
    """
    Apply the Sobel filter to a grayscale image.

    Parameters:
        image (list of lists): A 2D list representing a grayscale image.

    Returns:
        list of lists: A 2D list with the Sobel-filtered image.
    """
    height = len(image)
    width = len(image[0])
    # Initialize the result image
    result = [[0 for _ in range(width)] for _ in range(height)]
    # Define Sobel kernels

    sobel_x = [[-1, 0, 1] , [-2, 0, 2] , [-1, 0, 1]]
    sobel_y = [[-1, -2, -1] , [0, 0, 0] , [1, 2, 1]]
    for i in range(1, height - 1):
        for j in range(1, width - 1):
            gx = 0
            gy = 0
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    gx += image[i + dx][j + dy] * sobel_x[dx + 1][dy + 1]
                    gy += image[i + dx][j + dy] * sobel_y[dx + 1][dy + 1]
            result[i][j] = min(255, int((gx * gx + gy * gy) ** 0.5))
    return result





if __name__ == "__main__":
    
    main()