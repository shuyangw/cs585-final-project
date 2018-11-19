import tensorflow as tf
import numpy as np

tf.enable_eager_execution()

"""
comment: score
"""
def vectorize(comments):
    # print("Vectorizing")
    # vocab = set()
    # #Create the vocab
    # text = ""
    # for comment in comments:
    #     vocab = vocab.union(set(comment[0]))
    # vocab = sorted(vocab)
    # char2idx = {u:i for i, u in enumerate(vocab)}
    # idx2char = np.asarray(vocab)
    # text_as_int = np.array([char2idx[c] for c in text])

    # print("Finished vectorizing")
    # return vocab, char2idx, idx2char, text_as_int

    text = ""
    for comment in comments:
        text += comment[0]

    vocab = sorted(set(text))

    char2idx = {u:i for i, u in enumerate(vocab)}
    idx2char = np.array(vocab)
    
    text_as_int = np.array([char2idx[c] for c in text])

    return vocab, char2idx, idx2char, text_as_int

class Model(tf.keras.Model):
    def __init__(self, vocab_size, embedding_dim, units):
        super(Model, self).__init__()

        self.units = units

        self.embedding = tf.keras.layers.Embedding(vocab_size, embedding_dim)

        if tf.test.is_gpu_available():
            self.LSTM1 = tf.keras.layers.CuDNNLSTM(self.units, 
                                                return_sequences=True, 
                                                recurrent_initializer='glorot_uniform',
                                                stateful=True)
        else:
            self.LSTM1 = tf.keras.layers.LSTM(self.units, 
                                            return_sequences=True, 
                                            recurrent_activation='sigmoid', 
                                            recurrent_initializer='glorot_uniform', 
                                            stateful=True)

        self.fc = tf.keras.layers.Dense(vocab_size)

    def call(self, x):
        embedding = self.embedding(x)
        output1 = self.LSTM1(embedding)
        prediction = self.fc(output1)

        return prediction