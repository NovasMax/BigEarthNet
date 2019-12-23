# -*- coding: utf-8 -*-
#
# BigEarthNet class to create tf.data.Dataset based on the TFRecord files. 
#
# Author: Gencer Sumbul, http://www.user.tu-berlin.de/gencersumbul/
# Email: gencer.suembuel@tu-berlin.de
# Date: 23 Dec 2019
# Version: 1.0.1

import tensorflow as tf

BAND_STATS = {
            'mean': {
                'B01': 340.76769064,
                'B02': 429.9430203,
                'B03': 614.21682446,
                'B04': 590.23569706,
                'B05': 950.68368468,
                'B06': 1792.46290469,
                'B07': 2075.46795189,
                'B08': 2218.94553375,
                'B8A': 2266.46036911,
                'B09': 2246.0605464,
                'B11': 1594.42694882,
                'B12': 1009.32729131
            },
            'std': {
                'B01': 554.81258967,
                'B02': 572.41639287,
                'B03': 582.87945694,
                'B04': 675.88746967,
                'B05': 729.89827633,
                'B06': 1096.01480586,
                'B07': 1273.45393088,
                'B08': 1365.45589904,
                'B8A': 1356.13789355,
                'B09': 1302.3292881,
                'B11': 1079.19066363,
                'B12': 818.86747235
            }
        }

class BigEarthNet:
    def __init__(self, TFRecord_paths, batch_size, nb_epoch, shuffle_buffer_size):     
        dataset = tf.data.TFRecordDataset(TFRecord_paths)
        if shuffle_buffer_size > 0:
            dataset = dataset.shuffle(buffer_size=shuffle_buffer_size)
        dataset = dataset.repeat(nb_epoch)

        dataset = dataset.map(
            self.parse_function, num_parallel_calls=10)

        dataset = dataset.batch(batch_size, drop_remainder=False)
        self.dataset = dataset.prefetch(10)
        self.batch_iterator = self.dataset.make_one_shot_iterator()
       
    def parse_function(self, example_proto):
        parsed_features = tf.parse_single_example(
                example_proto, 
                {
                    'B01': tf.FixedLenFeature([20*20], tf.int64),
                    'B02': tf.FixedLenFeature([120*120], tf.int64),
                    'B03': tf.FixedLenFeature([120*120], tf.int64),
                    'B04': tf.FixedLenFeature([120*120], tf.int64),
                    'B05': tf.FixedLenFeature([60*60], tf.int64),
                    'B06': tf.FixedLenFeature([60*60], tf.int64),
                    'B07': tf.FixedLenFeature([60*60], tf.int64),
                    'B08': tf.FixedLenFeature([120*120], tf.int64),
                    'B8A': tf.FixedLenFeature([60*60], tf.int64),
                    'B09': tf.FixedLenFeature([20*20], tf.int64),
                    'B11': tf.FixedLenFeature([60*60], tf.int64),
                    'B12': tf.FixedLenFeature([60*60], tf.int64),
                    'original_labels': tf.VarLenFeature(dtype=tf.string),
                    'original_labels_multi_hot': tf.FixedLenFeature([43], tf.int64),
                    'patch_name': tf.VarLenFeature(dtype=tf.string)
                }
            )

        return {
            'B01': tf.reshape(parsed_features['B01'], [20, 20]),
            'B02': tf.reshape(parsed_features['B02'], [120, 120]),
            'B03': tf.reshape(parsed_features['B03'], [120, 120]),
            'B04': tf.reshape(parsed_features['B04'], [120, 120]),
            'B05': tf.reshape(parsed_features['B05'], [60, 60]),
            'B06': tf.reshape(parsed_features['B06'], [60, 60]),
            'B07': tf.reshape(parsed_features['B07'], [60, 60]),
            'B08': tf.reshape(parsed_features['B08'], [120, 120]),
            'B8A': tf.reshape(parsed_features['B8A'], [60, 60]),
            'B09': tf.reshape(parsed_features['B09'], [20, 20]),
            'B11': tf.reshape(parsed_features['B11'], [60, 60]),
            'B12': tf.reshape(parsed_features['B12'], [60, 60]),
            'original_labels_multi_hot': parsed_features['original_labels_multi_hot'],
            'original_labels': parsed_features['original_labels'],
            'patch_name': parsed_features['patch_name']
        }