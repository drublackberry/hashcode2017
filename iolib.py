#!/usr/bin/env python

"""
I/O functions for Hashcode 2017.
"""

import numpy as np
import pandas as pd
import os

INPUT_DIR = os.path.join(".", "input")

def read_scenario(scen_name):
    fname = os.path.join(INPUT_DIR, scen_name + ".in")
    with open(fname, 'r') as fp:
        V, E, R, C, X = [int(x) for x in fp.readline().strip().split()]
        v_sizes = [int(x) for x in fp.readline().strip().split()]
    #print(V, E, R, C, X)
    #print(len(v_sizes))

    # for each endnode
    start = 2
    endpoint_cache_lats = []
    vec_L_d = np.ones(E, dtype=np.float64) * np.nan
    for e in range(E):
        L_d, K = np.genfromtxt(fname, skip_header=start, max_rows=1, dtype=np.int64)
        vec_L_d[e] = L_d
        #print(L_d, K, e)
        if K > 0:
            foo = np.genfromtxt(fname, skip_header=start+1, max_rows=K, dtype=np.int64)
            if len(foo.shape) == 1:
                foo = foo.reshape(1, len(foo))
        else:
            foo = []
        endpoint_cache_lats.append(foo)
        #print("****\n", foo)
        start += 1 + K
    assert(len(endpoint_cache_lats) == E)

    # Now read requests
    requests = np.genfromtxt(fname, skip_header=start, max_rows=R)

    L = np.ones([E, C]) * np.nan
    for e in range(E):
        lats = endpoint_cache_lats[e]
        if len(lat):
            L[e, lats[:, 0]] = lats[:, 1]

    R_n = np.ones([E, V]) * np.nan
    req = requests.astype(np.int64)

    R_n[req[:, 1], req[:, 0]] = requests[:, 2]

    data = {}
    data['R_n'] = pd.DataFrame(R_n)
    data['L_d'] = pd.DataFrame(vec_L_d)
    data['L'] = pd.DataFrame(L)
    data['V'] = V
    data['E'] = E
    data['R'] = R
    data['C'] = C
    data['X'] = X
    data['v_size'] = pd.DataFrame(v_sizes)
    return data


class OutputBuffer(object):

    def __init__(self, prefix, output_dir):
        self.prefix = prefix
        self.output_dir = output_dir
        self.result = None

    def generate_output(self, storage):
        # storage is a V X C matrix
        stuff = {}
        for c in storage.columns:
            storage_c = storage[c]
            stuff[c] = list(storage_c[storage_c>0].index)
        self.result = dict([(k, v) for (k, v) in stuff.items() if len(v) > 0])

    def write_to_file(self, fname=None):
        if fname is None:
            fname = os.path.join(self.output_dir, self.prefix + ".out")
        else:
            fname = os.path.join(self.output_dir, self.prefix + fname + ".out")
        with open(fname, 'w') as fp:
            fp.write("%d\n" % len(self.result))
            for c, line in self.result.items():
                fp.write("%d " % c)
                fp.write(" ".join(["%d" % n for n in line]))
                fp.write("\n")

if __name__ == "__main__":
    # test
    data = read_scenario("me_at_the_zoo")
    print(data.keys())
    for k in data.keys():
        print(data[k])
