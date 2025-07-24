import cv2
import numpy as np
import matplotlib.pyplot as plt

def ROI1(imglink):
    # === Load the image ===
    image_path = imglink  # Replace with your image path
    img = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # === Convert to HSV color space for easier color segmentation ===
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # === Define color range for blue/cyan-like tones (tune if needed) ===
    lower_blue = np.array([90, 50, 50])
    upper_blue = np.array([130, 255, 255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # === Find contours of the mask ===
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # === Create an empty mask and draw the largest contour ===
    roi_mask = np.zeros_like(mask)
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        cv2.drawContours(roi_mask, [largest_contour], -1, 255, thickness=cv2.FILLED)

    # === Apply the ROI mask to the original image ===
    masked_img = cv2.bitwise_and(img_rgb, img_rgb, mask=roi_mask)

    # === Show results ===
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    axes[0].imshow(img_rgb)
    axes[0].set_title("Original Image")
    axes[0].axis("off")

    axes[1].imshow(mask, cmap='gray')
    axes[1].set_title("Blue-like Region Mask")
    axes[1].axis("off")

    axes[2].imshow(masked_img)
    axes[2].set_title("Extracted ROI")
    axes[2].axis("off")

    plt.tight_layout()
    plt.show()


def ROI2(imglink):


    # === Step 1: Load grayscale image ===
    image_path = imglink  # Replace with your image path
    gray_img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # === Step 2: Normalize grayscale to range [0, 10] ===
    img_scaled = cv2.normalize(gray_img.astype('float32'), None, alpha=0, beta=10, norm_type=cv2.NORM_MINMAX)
  

    img_scaled = 10 - img_scaled
    print(np.max(img_scaled))
    # === Step 3: Create mask for values <= 5 (i.e., inside the boundary) ===
    threshold_value = 5
    mask_inner = (img_scaled >= threshold_value).astype(np.uint8) * 255  # Binary mask

    # === Step 4: Find outer contour to define boundary ===
    contours, _ = cv2.findContours(mask_inner, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    roi_mask = np.zeros_like(gray_img)
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        cv2.drawContours(roi_mask, [largest_contour], -1, 255, thickness=cv2.FILLED)

    # === Step 5: Load original image in color and apply ROI mask ===
    original_img = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB)
    roi_result = cv2.bitwise_and(img_rgb, img_rgb, mask=roi_mask)




    
    # === Calculate ROI Mean and Ratio ===
    roi_scaled_values = img_scaled[roi_mask == 255]
    with open ('temptemp.txt','w') as f:
        for a in roi_scaled_values:   
            f.write("{}".format(a))
            f.write('\n')             

    
    reality_mean = np.mean(roi_scaled_values)
    ideality_value = 10.0
    reality_to_ideality_ratio =  reality_mean / ideality_value
    print(roi_scaled_values)
    # === Print result ===
    print(f"Mean value of ROI (Reality): {reality_mean:.3f}")
    print(f"Ideality value: {ideality_value}")
    print(f"(Reality / Ideality Ratio): {reality_to_ideality_ratio:.3f}")

    # === Step 6: Display results ===
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # Scaled image (0–10)
    axes[0].imshow(img_scaled, cmap='viridis')
    axes[0].set_title("Scaled Image (0=White to 10=Dark Blue)")
    axes[0].axis("off")

    # Binary mask (<= 5)
    axes[1].imshow(mask_inner, cmap='gray')
    axes[1].set_title("Mask (>= 5)")
    axes[1].axis("off")

    # Final ROI
    axes[2].imshow(roi_result)
    axes[2].set_title("Extracted ROI")
    axes[2].axis("off")

    plt.tight_layout()
    plt.show()



def main():
    imglink = 'image.png'
    ROI2(imglink)
if __name__ == "__main__":
    main()