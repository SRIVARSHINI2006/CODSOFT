import numpy as np
import pickle
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical
from model import build_model


# Load data
features = pickle.load(open("features.pkl", "rb"))
tokenizer = pickle.load(open("tokenizer.pkl", "rb"))

captions = pickle.load(open("captions.pkl", "rb"))  # optional if saved

vocab_size = len(tokenizer.word_index) + 1
max_length = 34  # adjust based on dataset


def data_generator(captions, features, tokenizer, max_length, vocab_size):
    while True:
        X1, X2, y = [], [], []

        for key, caps in captions.items():
            feature = features[key]

            for cap in caps:
                seq = tokenizer.texts_to_sequences([cap])[0]

                for i in range(1, len(seq)):
                    in_seq = seq[:i]
                    out_seq = seq[i]

                    in_seq = pad_sequences([in_seq], maxlen=max_length)[0]
                    out_seq = to_categorical([out_seq], num_classes=vocab_size)[0]

                    X1.append(feature)
                    X2.append(in_seq)
                    y.append(out_seq)

        yield ([np.array(X1), np.array(X2)], np.array(y))


# Build model
model = build_model(vocab_size, max_length)
model.summary()


# Train
steps = len(captions)

model.fit(
    data_generator(captions, features, tokenizer, max_length, vocab_size),
    epochs=10,
    steps_per_epoch=steps
)

model.save("model.h5")
print("Model trained ✔")