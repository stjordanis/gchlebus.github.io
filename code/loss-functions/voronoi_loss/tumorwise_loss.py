# -*- coding: utf-8 -*-
__author__ = 'gchlebus'

import tensorflow as tf
import numpy as np

def load_data():
  data = np.load('images.npz')
  voronoi = data['voronoi'][:, np.newaxis]
  labels = data['labels'][:, np.newaxis]
  labels = np.concatenate([labels==0, labels==1], axis=1).astype(np.float32)
  pred = data['prediction'][:, np.newaxis]
  pred = np.concatenate([pred==0, pred==1], axis=1).astype(np.float32)
  return voronoi, labels, pred


def cond(i, iter_count, *args):
  return tf.less(i, iter_count)

def body(i, iter_count, dicesum, unique_ids, voronoi, labels, pred):
  idx = unique_ids[i]
  mask = tf.cast(tf.equal(voronoi, idx), tf.float32)
  masked_labels = (labels * mask)[:, 1:]
  masked_pred = (pred * mask)[:, 1:]

  true_fg = tf.reduce_sum(masked_labels, axis=(0,2,3))
  pred_fg = tf.reduce_sum(masked_pred, axis=(0,2,3))
  intersection = tf.reduce_sum(masked_labels * masked_pred, axis=(0,2,3))

  eps = 0
  dice = (2*intersection + eps) / (true_fg + pred_fg + eps)
  dice = tf.reduce_sum(dice)
  dice = tf.Print(dice, [dice], message='dice=')
  dicesum = tf.add(dicesum, dice)
  return tf.add(i, 1), iter_count, dicesum, unique_ids, voronoi, labels, pred

def cond1(patch_index, patch_count, *args):
  return tf.less(patch_index, patch_count)

def loop1(patch_index, patch_count, sum_dice, counter, voronoi, labels, pred):
  idx = slice(patch_index, patch_index+1)
  voronoi_patch = voronoi[idx]
  labels_patch = labels[idx]
  pred_patch = pred[idx]
  voronoi_ids, _ = tf.unique(tf.reshape(voronoi_patch, [-1]))
  _, _, sum_dice, counter, *_ = tf.while_loop(cond2, loop2, [
    tf.constant(0), voronoi_ids, sum_dice, counter, voronoi_patch, labels_patch, pred_patch
    ])
  return [tf.add(patch_index, 1), patch_count, sum_dice, counter, voronoi, labels, pred]

def cond2(voronoi_index, voronoi_ids, *args):
  return tf.less(voronoi_index, tf.size(voronoi_ids))

def loop2(voronoi_index, voronoi_ids, sum_dice, counter, voronoi, labels, pred):
  mask = tf.cast(tf.equal(voronoi, voronoi_ids[voronoi_index]), tf.float32)
  masked_labels = (mask * labels)[:,1:]
  masked_pred = (mask * pred)[:,1:]
  true_fg = tf.reduce_sum(masked_labels, axis=(0,2,3))
  pred_fg = tf.reduce_sum(masked_pred, axis=(0,2,3))
  intersection = tf.reduce_sum(masked_labels * masked_pred, axis=(0,2,3))
  eps = 0
  dice = (2*intersection + eps) / (true_fg + pred_fg + eps)
  dice = tf.reduce_sum(dice)
  dice = tf.Print(dice, [dice], message='dice=')
  return tf.add(voronoi_index, 1), voronoi_ids, tf.add(sum_dice, dice), tf.add(counter, 1), voronoi, labels, pred

if __name__ == '__main__':
  voronoi, labels, pred = load_data()
  print('voronoi.shape', voronoi.shape)
  print('labels.shape', labels.shape)
  print('pred.shape', pred.shape)

  voronoi_ph = tf.placeholder(tf.float32, shape=[None, 1, None, None])
  labels_ph = tf.placeholder(tf.float32, shape=[None, 2, None, None])
  pred_ph = tf.placeholder(tf.float32, shape=[None, 2, None, None])

  # i = tf.constant(0)
  # initdicesum = tf.constant(0, dtype=tf.float32)
  # dice_per_patch = []
  # for patch_index in range(2):
  #   idx = slice(patch_index, patch_index+1)
  #   unique_ids, _ = tf.unique(tf.reshape(voronoi_ph[idx], [-1]))
  #   size = tf.size(unique_ids)
  #   _, _, dicesum, *_ = tf.while_loop(cond, body, [i, size, initdicesum, unique_ids, voronoi_ph[idx], labels_ph[idx], pred_ph[idx]])
  #   dice = dicesum / tf.cast(size, tf.float32)
  #   dice_per_patch.append(dice)
  # final_dice = tf.reduce_mean(dice_per_patch)

  _, _, sum_dice, counter, *_ = tf.while_loop(cond1, loop1, [
    tf.constant(0), tf.shape(labels)[0], tf.constant(0, tf.float32), tf.constant(0, tf.float32),
    voronoi_ph, labels_ph, pred_ph
  ])
  final_dice = sum_dice / counter
  with tf.Session() as s:
    feed_dict = {
      voronoi_ph: voronoi,
      labels_ph: labels,
      pred_ph: pred
    }
    s.run(tf.global_variables_initializer())
    ret= s.run(final_dice, feed_dict=feed_dict)
    print('First run', ret)
    ret= s.run(final_dice, feed_dict=feed_dict)
    print('Second run', ret)