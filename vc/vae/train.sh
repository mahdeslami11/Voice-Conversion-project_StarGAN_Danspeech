#Load preprocess configurations to know segment size
. /work1/s183921/fagprojekt2020/preprocess/spraakbanken/vae/preprocess.config

python3 main.py -c config.yaml -d /work1/s183921/preprocessed_data/vae/spraakbanken -train_set train_$segment_size -train_index_file train_samples_$segment_size.json -store_model_path /work1/s183921/trained_models/vae/model -t vae_model -iters 1000 -summary_step 200
