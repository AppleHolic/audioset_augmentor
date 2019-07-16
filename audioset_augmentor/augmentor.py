import numpy as np
import os
import glob
from scipy.io import wavfile
from audioset_augmentor.preprocess import load_default_config


AUDIO_DIR = None
AUDIO_LIST = None
AUDIO_SR = None


def __setup_audio_setting():
    global DATA_DIR, AUDIO_LIST, AUDIO_SR
    config = load_default_config()
    master_dir = config['master_path']

    AUDIO_DIR = os.path.join(master_dir, 'data', 'non-human')
    AUDIO_LIST = glob.glob(os.path.join(AUDIO_DIR, '*.wav'))
    AUDIO_SR = config['target_sr']


__setup_audio_setting()


def augment(wav: np.ndarray, amp: float = 0.5) -> np.ndarray:
    """

    :param wav: original wave-form numpy array
    :param amp: amp for audioset wave
    :return: combined wave
    """
    rand_idx = np.random.randint(0, len(AUDIO_LIST))
    r_audio = AUDIO_LIST[rand_idx]
    sr, r_wav = wavfile.read(r_audio)
    # random crop
    if len(wav) > len(r_wav):
        b_idx = np.random.randint(0, len(r_wav) - len(wav))
    else:
        b_idx = 0
    # stereo to mono
    if len(r_wav.shape) > 1:
        r_wav = np.mean(r_wav, axis=1)
    return np.clip(wav + r_wav[b_idx:b_idx+len(wav)] * amp, -1.0, 1.0)
