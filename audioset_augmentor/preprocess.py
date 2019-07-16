import os
import fire
import json
from ffmpeg_normalize import FFmpegNormalize
from typing import Dict, Any, List, Tuple

from audioset_augmentor.commons import do_multiprocess
from audioset_augmentor.download import get_audio_info


ASSET_DEFAULT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../assets/default.json')


def load_default_config(file_path: str = None):
    global ASSET_DEFAULT
    if not file_path:
        file_path = ASSET_DEFAULT
    with open(file_path, 'r') as r:
        configs = json.load(r)
    return configs


def load_ontology(file_path: str = 'assets/ontology.json') -> Dict[str, Any]:
    with open(file_path, 'r') as r:
        ont_config = json.load(r)
    result = {}
    for conf in ont_config:
        id_ = conf['id']
        del conf['id']
        result[id_] = conf
    return result


def get_human_ids(root_id: str = '/m/0dgw9r') -> List[str]:
    ont_config = load_ontology()

    # get child ids
    ids = [root_id] + ont_config[root_id]['child_ids']

    for child_id in ids:
        if 'child_ids' in ont_config[child_id]:
            ids += ont_config[child_id]['child_ids']

        for grandchild_id in ont_config[child_id]['child_ids']:
            if 'child_ids' in ont_config[grandchild_id]:
                ids += get_human_ids(grandchild_id)

    return list(set(ids))


def worker(args: Tuple[str, str], out_sr: int = 22050, min_size: int = 1000000):
    in_path, out_path = args
    # filter
    if not os.path.exists(in_path):
        return
    if os.path.getsize(in_path) < min_size:
        return
    norm = FFmpegNormalize(normalization_type='rms', audio_codec='pcm_f32le', sample_rate=out_sr)
    norm.add_media_file(in_path, out_path)
    norm.run_normalization()


def main(master_dir: str, out_dir: str, meta_path: str = 'assets/balanced_train_segments.csv'):
    # load config
    meta_info = get_audio_info(meta_path)

    # make dirs
    os.makedirs(os.path.join(out_dir, 'human'), exist_ok=True)
    os.makedirs(os.path.join(out_dir, 'non-human'), exist_ok=True)

    # make args
    args_list = []
    human_ids = get_human_ids()
    for item in meta_info.iterrows():
        renamed_yt_id = item[1]['YTID'].replace('-', 'XX')
        tag_id = item[1]['positive_labels'].split(',')
        is_human_sample = any([i in human_ids for i in tag_id])

        # make item
        subdir = 'human' if is_human_sample else 'non-human'
        in_path = os.path.join(master_dir, '{}.wav'.format(renamed_yt_id))
        out_path = os.path.join(out_dir, subdir, '{}.wav'.format(renamed_yt_id))
        args_list.append((in_path, out_path))

    # do multi-proc preprocess
    do_multiprocess(worker, args_list, num_proc=8, delay=None)


if __name__ == '__main__':
    fire.Fire(main)
