#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np


def jaccard_sim(bin_features1, bin_features2):
    """ Calcula a similaridade de Jaccard. 

    Exemplos
    --------

    >>> a = [True, True, False, False]
    >>> b = [True, False, False, False]
    >>> jaccard_sim(a, b)
    0.5
    
    """
    
    bin_features1, bin_features2 = __preprocessing(bin_features1, bin_features2)

    intercecao = np.logical_and(bin_features1, bin_features2)

    uniao = np.logical_or(bin_features1, bin_features2)

    return intercecao.sum() / float(uniao.sum())

def hamming_dist(bin_features1, bin_features2):
    """ Conta o número de features que não correspondem.
    
    Exemplos
    --------

    >>> a = [True, True, False, False]
    >>> b = [True, False, False, False]
    >>> hamming_dist(a, b)
    1
    
    """
    bin_features1, bin_features2 = __preprocessing(bin_features1, bin_features2)

    uniao_exclusiva = np.logical_xor(bin_features1, bin_features2)

    return uniao_exclusiva.sum()

def simpson_corr(bin_features1, bin_features2):
    """ Calcula correlação por simpson.
    
    Exemplos
    --------

    >>> a = [True, True, False, False, False]
    >>> b = [True, False, True, True, False]
    >>> simpson_corr(a, b)
    0.5
    
    """
    bin_features1, bin_features2 = __preprocessing(bin_features1, bin_features2)

    intercecao = np.logical_and(bin_features1, bin_features2)
    valores01 = np.logical_and(np.logical_not(bin_features1), bin_features2)
    valores10 = np.logical_and(bin_features1, np.logical_not(bin_features2))
    denominador = min(intercecao.sum()+valores01.sum(), intercecao.sum()+valores10.sum())
    if denominador == 0:
        denominador = 1
    result = intercecao.sum()/float(denominador)

    return result

def __preprocessing(bin_features1, bin_features2):
    bin_features1 = np.asarray(bin_features1)
    bin_features2 = np.asarray(bin_features2)
    if bin_features1.shape != bin_features2.shape:
        raise ValueError("Tamanhos diferentes: entradas tem que ter o mesmo tamanho.")
    return bin_features1, bin_features2


if __name__ == '__main__':
    import doctest
    doctest.testmod()