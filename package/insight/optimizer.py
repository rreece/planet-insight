"""
optimizer

Hyperparameter optimization

author: Ryan Reece <ryan.reece@cern.ch>
created: Jan 20, 2018
"""

import numpy as np
np.random.seed(777) # for DEBUG

import math
import time


#______________________________________________________________________________
def next_hyperparams(space, prev_hparams=None, prev_loss=None, n_workers=1):
    while True:
        _keys = space.keys()
        _keys.sort()
        new_hparams = dict()
        for _key in _keys:
            _val = None
            x1 = space[_key][0]
            x2 = space[_key][1]
            dx = space[_key][2]
            if dx is None:
                _val = x1 + (x2 - x1)*np.random.rand()
            elif isinstance(dx, int):
                _val = np.random.random_integers(x1, x2)
            else:
                assert False
            new_hparams[_key] = _val
        yield new_hparams


#______________________________________________________________________________
def get_loss(hps):
    """
    Franke function
    https://github.com/sigopt/sigopt-python/blob/master/sigopt/examples/franke.py
    http://www.sfu.ca/~ssurjano/franke2d.html
    """

    def franke_function(x, y):
        return (
          .75 * math.exp(-(9. * x - 2.) ** 2. / 4.0 - (9. * y - 2.) ** 2. / 4.0) +
          .75 * math.exp(-(9. * x + 1.) ** 2. / 49.0 - (9. * y + 1.) / 10.0) +
          .5 * math.exp(-(9. * x - 7.) ** 2. / 4.0 - (9. * y - 3.) ** 2. / 4.0) -
          .2 * math.exp(-(9. * x - 4.) ** 2. - (9.0 * y - 7.) ** 2.)
        )

    x = hps['x']
    y = hps['y']

    loss = franke_function(x, y) 
#    time.sleep(1)

    return loss


#______________________________________________________________________________
def calc_best_hyperparams(hparams_list, loss_list):
    best_hparams = None
    best_loss = 1e99
    assert len(hparams_list) == len(loss_list)
    for hparams, loss in zip(hparams_list, loss_list):
        if loss < best_loss:
            best_loss = loss
            best_hparams = hparams
    return best_hparams, best_loss


#______________________________________________________________________________
def main():
    space = {
        'x' : (0, 1, None),
        'y' : (0, 1, None),
        }
    max_steps = 50
    keys = space.keys()
    keys.sort()
    prev_hparams = list()
    prev_loss = list()
    for i_step, hps in enumerate(next_hyperparams(space, prev_hparams, prev_loss)):
        print 'step %i' % i_step
        for k in keys:
            v = hps[k]
            print '%s = %5g' % (k, v)
        loss = get_loss(hps)
        print 'loss', loss
        prev_hparams.append(hps)
        prev_loss.append(loss)
        if i_step >= max_steps-1:
            break

    best_hparams, best_loss = calc_best_hyperparams(prev_hparams, prev_loss)
    keys = best_hparams.keys()
    keys.sort()
    print 'best_hparams :'
    for k in keys:
        v = best_hparams[k]
        print '%s = %5g' % (k, v)
    print 'best_loss = %g' % best_loss


#______________________________________________________________________________
if __name__ == "__main__":
    main()

