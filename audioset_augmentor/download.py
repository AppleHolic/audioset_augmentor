import fire
import pandas as pd
import os

from itertools import repeat
from typing import Tuple
from youtube_dl import YoutubeDL
from audioset_augmentor.commons import do_multiprocess


def youtube_url_bone(yt_id: str) -> str:
    return 'https://www.youtube.com/watch?v={}'.format(yt_id)


def choose_hid_url(meta_info, min_bit_rate: int = 32) -> str:
    # select audio format only
    meta_info = [item for item in meta_info if 'audio' in item['format_note']]

    # filter minimum bit rate
    meta_info = [item for item in meta_info if item['abr'] >= min_bit_rate]

    # choose miminum file size
    choosed_item = sorted(meta_info, key=lambda x: x['filesize'])[0]

    # return final url
    return choosed_item['url']


def process_ffmpeg(url: str, file_path: str, begin: str = '', playtime: str = '',
                   fmt: str = 'pcm_f32le', timeout: int = 2):
    # command
    begin = '-ss {}'.format(begin) if begin else begin
    playtime = '-t {}'.format(playtime) if playtime else playtime

    command = 'ffmpeg -i \'{}\' -c copy -c:a {} -timeout {} {} {} {}'.format(url, fmt, timeout, begin, playtime,
                                                                             file_path)
    os.system(command)


def get_audio_info(file_path: str) -> pd.DataFrame:
    # read csv
    return pd.read_csv(file_path, sep=', ')


def time_formatter(meta_item, allowed_playtime: float = 10.0) -> Tuple[str, str]:
    # get begin, end seconds
    begin, end = int(meta_item['start_seconds']), int(meta_item['end_seconds'])
    playtime = end - begin
    assert playtime == allowed_playtime, 'playtime is not allowed'

    # convert
    # minutes
    minutes, seconds = begin // 60, begin % 60
    # hours
    hours, minutes = minutes // 60, minutes % 60

    # formatting, return
    formatter = lambda h, m, s: '{:02d}:{:02d}:{:02d}.00'.format(h, m, s)
    return formatter(hours, minutes, seconds), formatter(0, 0, playtime)


def download_partial_audio(args: Tuple[pd.Series, str]):
    # get youtube id
    item_tuple, savedir = args
    item = item_tuple[1]
    id_ = item['YTID']

    try:
        # get meta info
        with YoutubeDL(params={'forceurl': True}) as ydl:
            url = youtube_url_bone(id_)
            res = ydl.extract_info(url, download=False, process=False)
            # get hidden url
            hid_url = choose_hid_url(res['formats'])
            # format time
            begin, playtime = time_formatter(item)
    except Exception:
        return

    # process ffmpeg
    try:
        process_ffmpeg(hid_url, os.path.join(savedir, '{}.wav'.format(id_.replace('-', 'XX'))), begin=begin, playtime=playtime)
    except Exception:
        print('Maybe download error')


def main(file_path: str = 'assets/balanced_train_segments.csv', savedir: str = '.data',
         num_proc: int = 4, delay: float = 0.05, multiply: int = 1):
    # makedir
    os.makedirs(savedir, exist_ok=True)

    # parse real urls
    print('Parse audio information ...')
    item = get_audio_info(file_path)

    # to list
    print('Make arguments ...')
    item_list = list(zip(list(item.iterrows()), repeat(savedir, times=len(item))))

    # download with multi process
    do_multiprocess(download_partial_audio, item_list, num_proc=num_proc, delay=delay, multiply=multiply)
    print('Finish !')


if __name__ == '__main__':
    fire.Fire(main)
