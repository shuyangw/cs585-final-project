from rnn import vectorize, Model
from preprocessor import Preprocessor

import tensorflow as tf
import numpy as np

import os
import sys
import time

class Experiment(object):
    def __init__(
            self, subreddit, sample_size, percentile, custom_file="", custom=False, 
            seq_length=100
        ):

        self.subreddit = subreddit
        self.sample_size = sample_size
        self.percentile = percentile
        self.seq_length = seq_length

        dataset, vocab, char2idx, idx2char, text_as_int = None, None, None, None, None

        if custom:
            dataset, vocab, char2idx, idx2char, text_as_int = self.preprocess(
                custom=True, custom_file=custom_file
            )
        else:
            dataset, vocab, char2idx, idx2char, text_as_int = self.preprocess()
            
        self.dataset = dataset
        self.vocab = vocab
        self.char2idx = char2idx
        self.idx2char = idx2char
        self.text_as_it = text_as_int

    def _split_input_target(self, chunk):
        input_text = chunk[:-1]
        target_text = chunk[1:]

        return input_text, target_text

    def setup_vectorized_data(self, vocab, char2idx, idx2char, text_as_int):
        chunks = tf.data.Dataset.from_tensor_slices(text_as_int).batch(
            self.seq_length+1, drop_remainder=True
        )
        
        dataset = chunks.map(self._split_input_target)

        return dataset, vocab, char2idx, idx2char, text_as_int

    def preprocess(self, custom_file="", custom=False):
        print("Preprocessing")

        if custom:
            pp = Preprocessor(self.subreddit, self.sample_size, self.percentile,
                custom=True, custom_file=custom_file
            )
            output, _ = pp.process(custom=True, custom_file=custom_file)
            output = [(str(output[i]), 0) for i in range(len(output))]
            vocab, char2idx, idx2char, text_as_int = vectorize(output)

            return self.setup_vectorized_data(
                vocab, char2idx, idx2char, text_as_int
            )
        else:
            pp = Preprocessor(self.subreddit, self.sample_size, self.percentile)
            comments, num = pp.process()
            good_comments = pp.statistics(comments)

            print(num)
            print(len(comments))
            print(len(good_comments))

            vocab, char2idx, idx2char, text_as_int = vectorize(good_comments)
            return self.setup_vectorized_data(
                vocab, char2idx, idx2char, text_as_int
            )

    def regular_train(self, save=True, epochs=5):
        print("Regular training")
        batch_size = 1
        buffer_size = 10000
        self.dataset = self.dataset.shuffle(buffer_size).batch(
            batch_size, drop_remainder=True
        )

        vocab_size = len(self.vocab)
        embedding_dim = 256
        units = 1024

        model = Model(vocab_size, embedding_dim, units)
 
        optimizer = tf.train.AdamOptimizer()
        def loss_function(real, preds):
            return tf.losses.sparse_softmax_cross_entropy(
                labels=real, logits=preds
            )

        model.build(tf.TensorShape([batch_size, self.seq_length]))

        checkpoint_dir = './training_checkpoints'
        losses = []
        iterations = []
        iteration = 0
        for epoch in range(epochs):
            start = time.time()
        
            # initializing the hidden state at the start of every epoch
            # initally hidden is None
            hidden = model.reset_states()
            
            for (batch, (inp, target)) in enumerate(self.dataset):
                with tf.GradientTape() as tape:
                    # feeding the hidden state back into the model
                    # This is the interesting step
                    predictions = model(inp)
                    loss = loss_function(target, predictions)
                    
                grads = tape.gradient(loss, model.variables)
                optimizer.apply_gradients(zip(grads, model.variables))

                if batch % 100 == 0:
                    print ('Epoch {} Batch {} Loss {:.4f}'.format(epoch+1,
                                                                    batch,
                                                                    loss))

                    losses.append(loss)
                    iterations.append(iteration)
                    iteration += 1
            print ('Epoch {}'.format(epoch+1))
            print ('Time taken for 1 epoch {} sec\n'.format(time.time()-start))

        if save:
            model.save_weights(os.path.join(checkpoint_dir, "ckpt"))

        return model, losses, iterations

    def predict(self, model, num_generate, start_string, out=False):
        print("Predicting...")
        num_generate = num_generate
        start_string = "I"
        input_eval = [self.char2idx[s] for s in start_string]
        input_eval = tf.expand_dims(input_eval, 0)
        text_generated = []
        temperature = 1.0

        model.reset_states()
        for i in range(num_generate):
            predictions = model(input_eval)
            # remove the batch dimension
            predictions = tf.squeeze(predictions, 0)

            # using a multinomial distribution to predict the word returned by the model
            predictions = predictions / temperature
            predicted_id = tf.multinomial(predictions, num_samples=1)[-1,0].numpy()
            
            # We pass the predicted word as the next input to the model
            # along with the previous hidden state
            input_eval = tf.expand_dims([predicted_id], 0)
            text_generated.append(self.idx2char[predicted_id])

        print (start_string + ''.join(text_generated))
        
        if out:
            if not os.path.exists("outputs/" + str(self.sample_size) + ".txt"):
                output = open("outputs/" + str(self.sample_size) + ".txt", "w+", encoding="utf-8")
                output.write(start_string + ''.join(text_generated))
                output.close()
            else:
                count = 1
                while os.path.exists("outputs/" + str(self.sample_size) + ".txt"):
                    count += 1
                output = open("outputs/" + str(self.sample_size) + str(count) + ".txt", "w+", encoding="utf-8")
                output.write(start_string + ''.join(text_generated))
                output.close()
        