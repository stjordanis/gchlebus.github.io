# -*- coding: utf-8 -*-
__author__ = 'gchlebus'

from evaluation import evaluate
import numpy as np

def test_zero_input():
  tp, fp, correspondences, jaccard_indices, fp_indicies = evaluate(np.zeros(shape=(1,1)), np.zeros(shape=(1,1)))
  assert tp == 0
  assert fp == 0


def test_empty_refmask():
  tp, fp, correspondences, jaccard_indices, fp_indicies = evaluate(np.zeros(shape=(1,1)), np.ones(shape=(1,1)))
  assert tp == 0
  assert fp == 1

def test_empty_testmask():
  tp, fp, correspondences, jaccard_indices, fp_indicies = evaluate(np.ones(shape=(1,1)), np.zeros(shape=(1,1)))
  assert tp == 0
  assert fp == 0

def test_one_ref_one_test_1():
  '''
  ref   test
  1 0   1 0
  0 0   0 0
  '''
  refmask = np.zeros(shape=(2,2))
  testmask = np.zeros(shape=(2,2))
  refmask[0,0] = 1
  testmask[0,0] = 1
  tp, fp, correspondences, jaccard_indices, fp_indicies = evaluate(refmask, testmask)
  assert tp == 1
  assert fp == 0

def test_one_ref_one_test_2():
  '''
  ref   test
  1 0   0 0
  0 0   1 0
  '''
  refmask = np.zeros(shape=(2,2))
  testmask = np.zeros(shape=(2,2))
  refmask[0,0] = 1
  testmask[1,0] = 1
  tp, fp, correspondences, jaccard_indices, fp_indicies = evaluate(refmask, testmask)
  assert tp == 0
  assert fp == 1


def test_one_ref_one_test_1():
  '''
  ref   test
  1 0   1 1
  0 0   1 1
  '''
  refmask = np.zeros(shape=(2,2))
  testmask = np.ones(shape=(2,2))
  refmask[0,0] = 1
  tp, fp, correspondences, jaccard_indices, fp_indicies = evaluate(refmask, testmask)
  assert tp == 0
  assert fp == 1


def test_one_ref_two_test():
  '''
  ref     test
  1 0 0   1 0 0
  0 0 0   0 0 0
  0 0 0   0 0 2
  '''
  refmask = np.zeros(shape=(3,3))
  testmask = np.zeros(shape=(3,3))
  refmask[0,0] = 1 
  testmask[0,0] = 1
  testmask[2,2] = 2
  tp, fp, correspondences, jaccard_indices, fp_indicies = evaluate(refmask, testmask)
  assert tp == 1
  assert fp == 1


def test_two_ref_two_test_1():
  '''
  ref     test
  1 0 0   1 0 0
  0 0 0   0 0 0
  0 0 2   0 0 2
  '''
  refmask = np.zeros(shape=(3,3))
  testmask = np.zeros(shape=(3,3))
  refmask[0,0] = 1 
  refmask[2,2] = 2
  testmask[0,0] = 1
  testmask[2,2] = 2
  tp, fp, correspondences, jaccard_indices, fp_indicies = evaluate(refmask, testmask)
  assert tp == 2
  assert fp == 0


def test_two_ref_one_test_2():
  '''
  ref     test
  1 1 0   1 1 1
  0 0 0   0 0 1
  0 0 2   0 0 1
  '''
  refmask = np.zeros(shape=(3,3))
  testmask = np.ones(shape=(3,3))
  refmask[0,0] = 1
  refmask[0,1] = 1 
  refmask[2,2] = 2
  testmask[1,0] = 0
  testmask[2,0] = 0
  testmask[1,1] = 0
  testmask[2,1] = 0
  tp, fp, correspondences, jaccard_indices, fp_indicies =  evaluate(refmask, testmask)
  assert tp == 2
  assert fp == 0

def test_one_ref_two_test_2():
  '''
  ref     test
  1 1 1   1 1 1
  1 1 1   0 0 0
  1 1 1   2 2 2
  '''
  refmask = np.ones(shape=(3,3))
  testmask = np.array([
    [1, 1, 1],
    [0, 0, 0],
    [2, 2, 2]
  ])
  tp, fp, correspondences, jaccard_indices, fp_indicies =  evaluate(refmask, testmask)
  assert tp == 1
  assert fp == 0
  assert correspondences == [[[1],[1,2]]]

def test_two_ref_two_test():
  '''
  ref     test
  1 1 1   1 1 1
  1 1 1   0 0 0
  1 1 1   2 2 2
  0 0 0   2 2 2
  2 2 2   2 2 2
  '''
  refmask = np.array([
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1],
    [0, 0, 0],
    [2, 2, 2]
  ])
  testmask = np.array([
    [1, 1, 1],
    [0, 0, 0],
    [2, 2, 2],
    [2, 2, 2],
    [2, 2, 2],
  ])
  tp, fp, correspondences, jaccard_indices, fp_indicies =  evaluate(refmask, testmask)
  assert tp == 2
  assert fp == 0
  assert correspondences == [[[1,2],[1,2]]]

def test_three_ref_three_test():
  '''
  ref     test
  1 1 1   1 1 1
  1 1 1   0 0 0
  1 1 1   2 2 2
  0 0 0   2 2 2
  2 2 2   2 2 2
  2 2 2   2 2 2 
  0 0 0   0 0 0
  0 0 0   3 3 3
  3 3 3   0 0 0
  '''
  refmask = np.array([
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1],
    [0, 0, 0],
    [2, 2, 2],
    [2, 2, 2],
    [0, 0, 0],
    [0, 0, 0],
    [3, 3, 3],
  ])
  testmask = np.array([
    [1, 1, 1],
    [0, 0, 0],
    [2, 2, 2],
    [2, 2, 2],
    [2, 2, 2],
    [2, 2, 2],
    [0, 0, 0],
    [3, 3, 3],
    [0, 0, 0]
  ])
  tp, fp, correspondences, jaccard_indices, fp_indicies =  evaluate(refmask, testmask)
  assert tp == 2
  assert fp == 1
  assert correspondences == [[[1,2],[1,2]]]