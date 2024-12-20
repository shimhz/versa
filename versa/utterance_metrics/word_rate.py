#!/usr/bin/env python3

# Copyright 2024 Jiatong Shi
#  Apache 2.0  (http://www.apache.org/licenses/LICENSE-2.0)

import logging

import librosa
import numpy as np
import torch

try:
    import whisper
except ImportError:
    logging.warning(
        "Whisper is not properly installed. Please install following https://github.com/openai/whisper"
    )
    whisper = None

from espnet2.text.cleaner import TextCleaner


TARGET_FS = 16000
CHUNK_SIZE = 30  # seconds


def whisper_wer_setup(
    model_tag="default", beam_size=5, text_cleaner="whisper_basic", use_gpu=True
):
    if model_tag == "default":
        model_tag = "large"
    device = "cuda" if use_gpu else "cpu"
    if whisper is None:
        raise RuntimeError(
            "Whisper WER is used for evaluation while openai-whisper is not installed"
        )
    model = whisper.load_model(model_tag, device=device)
    textcleaner = TextCleaner(text_cleaner)
    wer_utils = {"model": model, "cleaner": textcleaner, "beam_size": beam_size}
    return wer_utils

def whisper_word_rate(wer_utils, pred_x, cache_text, fs=16000):
    """Calculate the word rate from ASR results.

    Args:
        wer_utils (dict): a utility dict for WER calculation.
            including: whisper model ("model"), text cleaner ("textcleaner"), and
            beam size ("beam size")
        pred_x (np.ndarray): test signal (time,)
        cache_text (string): transcription from cache (previous modules)
        fs (int): sampling rate in Hz
    Returns:
        ret (dict): ditionary containing the speaking word rate
    """
    if cache_text is not None:
        inf_text = cache_text
    else:
        if fs != TARGET_FS:
            pred_x = librosa.resample(pred_x, orig_sr=fs, target_sr=TARGET_FS)
            fs = TARGET_FS
        with torch.no_grad():
            inf_text = wer_utils["model"].transcribe(
                pred_x, fs, chunk_size=CHUNK_SIZE, beam_size=wer_utils["beam_size"]
            )
    return {"speaking_word_rate": len(inf_text.split()) / (len(pred_x) / fs)}

if __name__ == "__main__":
    a = np.random.random(16000)
    wer_utils = whisper_wer_setup()
    print("metrics: {}".format(whisper_word_rate(wer_utils, a, 16000)))