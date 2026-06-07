import os
import numpy as np
import pickle
from tqdm import tqdm

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from tensorflow.keras.preprocessing.image import load_img, img_to_array


# -----------------------------
# Load captions
# -----------------------------
def load_captions(path):
    captions = {}

    with open(path, "r", encoding="utf-8") as f:
        data = f.read().split("\n")

   for line in data:

    # Skip header row
    if line.startswith("image,"):
        continue

    tokens = line.split(",")

    if len(tokens) < 2:
        continue

    img_id = tokens[0].split(".")[0]
    caption = " ".join(tokens[1:]).lower().strip()

    caption = "startseq " + caption + " endseq"

    if img_id not in captions:
        captions[img_id] = []

    captions[img_id].append(caption)

return captions

# -----------------------------
# ResNet50 Feature Extractor
# -----------------------------
cnn_model = ResNet50(
    weights="imagenet",
    include_top=False,
    pooling="avg"
)


def extract_features(directory):
    features = {}

    image_list = os.listdir(directory)

    for img_name in tqdm(image_list):

        img_path = os.path.join(directory, img_name)

        try:
            img = load_img(img_path, target_size=(224, 224))
            img = img_to_array(img)

            img = np.expand_dims(img, axis=0)
            img = preprocess_input(img)

            feature = cnn_model.predict(img, verbose=0)

            image_id = img_name.split(".")[0]

            features[image_id] = feature.flatten()

        except Exception as e:
            print(f"Error processing {img_name}: {e}")

    return features


# -----------------------------
# Create Tokenizer
# -----------------------------
def create_tokenizer(captions):

    all_captions = []

    for key in captions:
        all_captions.extend(captions[key])

    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(all_captions)

    return tokenizer


# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":

    print("Loading captions...")

    captions = load_captions("dataset/captions.txt")

    print(f"Images with captions: {len(captions)}")

    print("Extracting ResNet50 features...")

    features = extract_features("dataset/Images")

    print(f"Features extracted: {len(features)}")

    print("Creating tokenizer...")

    tokenizer = create_tokenizer(captions)

    print("Saving files...")

    with open("features.pkl", "wb") as f:
        pickle.dump(features, f)

    with open("tokenizer.pkl", "wb") as f:
        pickle.dump(tokenizer, f)

    with open("captions.pkl", "wb") as f:
        pickle.dump(captions, f)

    print("\nPreprocessing Done ✔")
    print("features.pkl saved")
    print("tokenizer.pkl saved")
    print("captions.pkl saved")