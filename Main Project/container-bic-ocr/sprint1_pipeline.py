import cv2
import easyocr
import numpy as np

def extract_container_code(image_path, bbox):
    """
    Crops the container image based on the bounding box and extracts the BIC code.
    bbox format: [x_min, y_min, width, height]
    """
    # Load the 416x416 image
    img = cv2.imread(image_path)
    if img is None:
        return "Error: Image not found."
    
    # Extract coordinates and crop
    x, y, w, h = map(int, bbox)
    crop_img = img[y:y+h, x:x+w]
    
    # Initialize EasyOCR (runs on CPU if GPU is unavailable)
    reader = easyocr.Reader(['en']) 
    results = reader.readtext(crop_img)
    
    extracted_text = []
    for (box, text, prob) in results:
        if prob > 0.45:  # Filter out low-confidence readings
            extracted_text.append(text)
            
    # Combine detected text into a single string
    final_code = "".join(extracted_text).replace(" ", "").upper()
    return final_code

if __name__ == "__main__":
    # Example usage using the reference image name from your Roboflow export
    test_image = "./dataset/train/image_901193.png" 
    
    # Example bounding box (x, y, width, height)
    test_bbox = [50, 100, 250, 60] 
    
    try:
        bic_code = extract_container_code(test_image, test_bbox)
        print(f"Extracted Container Code: {bic_code}")
    except Exception as e:
        print(f"Pipeline test failed: {e}")