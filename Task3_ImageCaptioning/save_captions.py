import pickle
from preprocess import load_captions

captions = load_captions("dataset/captions.txt")

with open("captions.pkl", "wb") as f:
    pickle.dump(captions, f)

print("captions.pkl saved")
print("Number of images:", len(captions))