#!/usr/bin/env python3

# Copyright 2024 Jiatong Shi
#  Apache 2.0  (http://www.apache.org/licenses/LICENSE-2.0)

import logging

import librosa
import numpy as np
import torch

try:
    from noresqa_versa import Noresqa
except ImportError:
    logging.warning(
        "noresqa is not installed. Please use `tools/install_scoreq.sh` to install"
    )
    Noresqa = None


def noresqa(pred_x, gt_x, fs):
    # NOTE(hyejin): current model only have 16k options
    if fs != 16000:
        gt_x = librosa.resample(gt_x, orig_sr=fs, target_sr=16000)
        pred_x = librosa.resample(pred_x, orig_sr=fs, target_sr=16000)

    return {
        "noresqa_score": Noresqa(metric_type=0, test_path=pred_x, ref_path=gt_x)[1],
        "noresqa_mos": Noresqa(metric_type=1, test_path=pred_x, ref_path=gt_x),
    }


if __name__ == "__main__":
    a = np.random.random(16000)
    b = np.random.random(16000)
    fs = 16000
    metric_nr = scoreq_nr(nr_model, a, fs)
    metric_ref = scoreq_ref(ref_model, a, b, fs)
    print(metric_nr)
    print(metric_ref)
