FROM conda/miniconda3

RUN apt-get update && \
    apt-get install -y --no-install-recommends

SHELL ["/bin/bash", "-c"]

COPY audioset_aug.yml audioset_aug.yml

ARG CONDA_ENV="audioset_aug"

RUN conda env create -n ${CONDA_ENV} -f ${CONDA_ENV}.yml \
    && echo "source activate ${CONDA_ENV}" > ~/.bashrc \
    && rm -fr *.yml ~/.cache/pip /var/lib/apt/lists/* ~/conda

WORKDIR /audioset_augmentor

ENTRYPOINT [ "/bin/bash" ]