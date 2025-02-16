import requests
import cv2
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Example: You would download the images from DuckDuckGo and process them here
# Assuming you have the URLs of images, download them and process each one

def download_image(url):
    resp = requests.get(url)
    img_array = np.asarray(bytearray(resp.content), dtype=np.uint8)
    return cv2.imdecode(img_array, -1)

def extract_face_embeddings(image):
    # Placeholder: Use a facial recognition model like FaceNet or OpenCV's Haar Cascades for face detection
    # Extract embeddings for each detected face (this step requires a model for face recognition)
    embeddings = []  # Should be replaced with actual embeddings
    return embeddings

def compare_faces(embedding1, embedding2):
    return cosine_similarity([embedding1], [embedding2])[0][0]

# Example: You'd download images, extract embeddings, and then compare embeddings
image_urls = ["image1_url", "image2_url"]  # Replace with actual DuckDuckGo image URLs
unique_faces = []

for url in image_urls:
    image = download_image(url)
    face_embeddings = extract_face_embeddings(image)
    
    for embedding in face_embeddings:
        is_unique = True
        for unique_face in unique_faces:
            if compare_faces(embedding, unique_face) > 0.8:  # Adjust threshold
                is_unique = False
                break
        if is_unique:
            unique_faces.append(embedding)

print(f"Number of unique people: {len(unique_faces)}")
