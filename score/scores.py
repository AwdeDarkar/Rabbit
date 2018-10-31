"""
SCORES
====================================================================================================

Tools to score a list of predictions.

----------------------------------------------------------------------------------------------------

**Created**
    10.26.18
**Updated**
    10.26.18 by Darkar
**Author**
    Darkar
"""

import numpy as np
from sklearn import metrics

def score_brier(predictions):
    """ Use sklearn's brier score """
    maxlen = 0
    for pred in predictions:
        if len(pred.probabilities) > maxlen:
            maxlen = len(pred.probabilities)

    probs = np.zeros(len(predictions), maxlen)
    trues = np.zeros(len(predictions), maxlen)
    for i, pred in enumerate(predictions):
        probs[i], trues[i] = pred.get_vectors(maxlen)

    return metrics.brier_score_loss(trues, probs)
