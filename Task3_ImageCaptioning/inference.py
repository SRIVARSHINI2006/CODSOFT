import numpy as np
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input

# Load models
model = load_model("model.h5")
tokenizer = pickle.load(open("tokenizer.pkl", "rb"))
features_model = ResNet50(weights='imagenet', include_top=False, pooling='avg')

max_length = 34


def extract_feature(img_path):
    img = load_img(img_path, target_size=(224, 224))
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = preprocess_input(img)

    feature = features_model.predict(img, verbose=0)
    return feature


def generate_caption(photo):
    in_text = "startseq"

    for i in range(max_length):
        sequence = tokenizer.texts_to_sequences([in_text])[0]
        sequence = pad_sequences([sequence], maxlen=max_length)

        yhat = model.predict([photo, sequence], verbose=0)
        yhat = np.argmax(yhat)

        word = None
        for w, index in tokenizer.word_index.items():
            if index == yhat:
                word = w
                break

        if word is None:
            break

        in_text += " " + word

        if word == "endseq":
            break

    return in_text


if __name__ == "__main__":
    img_path = "test.jpg"

    photo = extract_feature(img_path)
    caption = generate_caption(photo.reshape(1, -1))

    print("Caption:", caption)