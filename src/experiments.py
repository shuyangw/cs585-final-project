from rnn import vectorize, Model
from preprocessor import Preprocessor

import tensorflow as tf
import numpy as np

import os
import sys
import time

class Experiment(object):
    def __init__(self, subreddit, sample_size, percentile):
        self.subreddit = subreddit
        self.sample_size = sample_size
        self.percentile = percentile

        dataset, vocab, char2idx, idx2char, text_as_int = self.preprocess()
        self.dataset = dataset
        self.vocab = vocab
        self.char2idx = char2idx
        self.idx2char = idx2char
        self.text_as_it = text_as_int

        #Possible hyp param
        self.seq_length = 100

    def _split_input_target(self, chunk):
        input_text = chunk[:-1]
        target_text = chunk[1:]

        return input_text, target_text

    def preprocess(self):
        pp = Preprocessor(self.subreddit, self.sample_size, self.percentile)
        comments = pp.process()
        good_comments = pp.statistics(comments)

        vocab, char2idx, idx2char, text_as_int = vectorize(good_comments)

        self.seq_length = 100
        chunks = tf.data.Dataset.from_tensor_slices(text_as_int).batch(self.seq_length+1, drop_remainder=True)
        
        dataset = chunks.map(self._split_input_target)

        return dataset, vocab, char2idx, idx2char, text_as_int

    def regular_train(self, save=True, epochs=5):
        batch_size = 1
        buffer_size = 10000
        self.dataset = self.dataset.shuffle(buffer_size).batch(batch_size, drop_remainder=True)

        vocab_size = len(self.vocab)
        embedding_dim = 256
        units = 1024

        model = Model(vocab_size, embedding_dim, units)

        optimizer = tf.train.AdamOptimizer()
        def loss_function(real, preds):
            return tf.losses.sparse_softmax_cross_entropy(labels=real, logits=preds)

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
            # saving (checkpoint) the model every 5 epochs
            # if (epoch + 1) % 5 == 0:
            #   model.save_weights(checkpoint_prefix)

            print ('Epoch {} Loss {:.4f}'.format(epoch+1, loss))
            print ('Time taken for 1 epoch {} sec\n'.format(time.time() - start))

        if save:
            model.save_weights(os.path.join(checkpoint_dir, "ckpt"))

        return model, losses, iterations

    def predict(self, model, num_generate, start_string, out=False):
        num_generate = 1000
        start_string = "s"
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
            output = open("output.txt", "w+", encoding="utf-8")
            output.write(start_string + ''.join(text_generated))
        