from rnn import vectorize, Model
from preprocessor import Preprocessor

import numpy as np
import tensorflow as tf

import os
import sys
import time

if __name__ == '__main__':
    pp = Preprocessor('leagueoflegends', 5e5, 75)
    comments = pp.process()
    good_comments = pp.statistics(comments)

    vocab, char2idx, idx2char, text_as_int = vectorize(good_comments)

    seq_length = 100
    chunks = tf.data.Dataset.from_tensor_slices(text_as_int).batch(seq_length+1, drop_remainder=True)
    def split_input_target(chunk):
        input_text = chunk[:-1]
        target_text = chunk[1:]
        return input_text, target_text

    dataset = chunks.map(split_input_target)

    batch_size = 1
    buffer_size = 10000
    dataset = dataset.shuffle(buffer_size).batch(batch_size, drop_remainder=True)

    vocab_size = len(vocab)
    embedding_dim = 256
    units = 1024

    model = Model(vocab_size, embedding_dim, units)

    optimizer = tf.train.AdamOptimizer()
    def loss_function(real, preds):
        return tf.losses.sparse_softmax_cross_entropy(labels=real, logits=preds)

    model.build(tf.TensorShape([batch_size, seq_length]))

    checkpoint_dir = 'training_checkpoints'
    EPOCHS = 5

    for epoch in range(EPOCHS):
        start = time.time()
    
    # initializing the hidden state at the start of every epoch
    # initally hidden is None
    hidden = model.reset_states()
    
    for (batch, (inp, target)) in enumerate(dataset):
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
    saving (checkpoint) the model every 5 epochs
    if (epoch + 1) % 5 == 0:
      model.save_weights(checkpoint_prefix)

    print ('Epoch {} Loss {:.4f}'.format(epoch+1, loss))
    print ('Time taken for 1 epoch {} sec\n'.format(time.time() - start))

    num_generate = 200
    start_string = "s"
    input_eval = [char2idx[s] for s in start_string]
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
        
        text_generated.append(idx2char[predicted_id])

    print (start_string + ''.join(text_generated))