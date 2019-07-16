[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2FAppleHolic%2Faudioset_augmentor)](https://hits.seeyoufarm.com)



### Audio Augmentation using AudioSet

- AudioSet
  - Google's audio dataset that manually annotated audio events
  - ontology : https://github.com/audioset/ontology

- Goal
  - Augment with various sound situation for speech related tasks.

- Few things gonna be fixed on source...


#### How to Use

- Installation
  - install ffmpeg version 4, and this package

``` bash
$ apt install -y software-properties-common
$ add-apt-repository ppa:jonathonf/ffmpeg-4
$ apt update
$ apt install -y ffmpeg
$ pip install -e .
```

- Download
  - Audioset give us separated meta information that label balanced or not.
  - default : balanced

``` bash
$ python audioset_augmentor/download.py --help
```

- Preprocess Audio
  - Process adjust volume, sample rate, file type on audio files.

``` bash
$ python audioset_augmentor/preprocess.py --help
```

- After all, you should set master_dir on assets/default.json for using augment function.

#### License

- 'Audioset' license is announced on https://research.google.com/audioset/download.html

  - File List

    1. assets/balanced_train_segments.csv
    2. assets/unbalanced_train_segments.csv
    3. assets/ontology.json

> The dataset is made available by Google Inc. under a Creative Commons Attribution 4.0 International (CC BY 4.0) license, while the ontology is available under a Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0) license.

- Other sources are under MIT License
