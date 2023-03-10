'''
Code taken directly from StarGAN-Voice-Conversion repo.
main.py modified specifically for Spraakbanken audio data.
@AugustSemrau for DTU course #02466.
'''

import os
import argparse
from solver import Solver
from data_loader import get_loader, TestDataset
from torch.backends import cudnn


def str2bool(v):
    return v.lower() in ('true')

def main(config):
    # For fast training.
    cudnn.benchmark = True

    # Create directories if not exist.
    if not os.path.exists(config.log_dir):
        os.makedirs(config.log_dir)
    if not os.path.exists(config.model_save_dir):
        os.makedirs(config.model_save_dir)
    if not os.path.exists(config.sample_dir):
        os.makedirs(config.sample_dir)

    # Data loader.
    train_loader = get_loader(config.train_data_dir, config.batch_size, 'train', num_workers=config.num_workers)
    # test_loader = TestDataset(config.test_data_dir, config.wav_dir, src_spk="r5650082", trg_spk="r5650072")
    test_loader = TestDataset(config.test_data_dir, config.wav_dir, src_spk="r6110049", trg_spk="r6110050")


    # Solver for training and testing StarGAN.
    solver = Solver(train_loader, test_loader, config)

    if config.mode == 'train':
        solver.train()

    # elif config.mode == 'test':
    #     solver.test()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # Model configuration.
    parser.add_argument('--num_speakers', type=int, default=25, help='dimension of speaker labels')  # Specified
    parser.add_argument('--lambda_cls', type=float, default=10, help='weight for domain classification loss')  # Specified
    parser.add_argument('--lambda_rec', type=float, default=10, help='weight for reconstruction loss')  # Specified
    parser.add_argument('--lambda_gp', type=float, default=10, help='weight for gradient penalty')  # Specified
    parser.add_argument('--sampling_rate', type=int, default=16000, help='sampling rate')

    # Training configuration.
    parser.add_argument('--batch_size', type=int, default=32, help='mini-batch size')  # Specified to original value
    parser.add_argument('--num_iters', type=int, default=200000, help='number of total iterations for training D')
    parser.add_argument('--num_iters_decay', type=int, default=100000, help='number of iterations for decaying lr')
    parser.add_argument('--g_lr', type=float, default=0.0001, help='learning rate for G')
    parser.add_argument('--d_lr', type=float, default=0.0001, help='learning rate for D')
    parser.add_argument('--n_critic', type=int, default=5, help='number of D updates per each G update')
    parser.add_argument('--beta1', type=float, default=0.5, help='beta1 for Adam optimizer')
    parser.add_argument('--beta2', type=float, default=0.999, help='beta2 for Adam optimizer')
    parser.add_argument('--resume_iters', type=int, default=None, help='resume training from this step')

    # Test configuration.
    parser.add_argument('--test_iters', type=int, default=100000, help='test model from this step')

    # Miscellaneous.
    parser.add_argument('--num_workers', type=int, default=1)
    parser.add_argument('--mode', type=str, default='train', choices=['train', 'test'])
    parser.add_argument('--use_tensorboard', type=str2bool, default=True)

    # Directories on August's machine
    # parser.add_argument('--train_data_dir', type=str, default='../../../preprocessed_data/stargan/spraakbanken/mc/train')
    # parser.add_argument('--test_data_dir', type=str, default='../../../preprocessed_data/stargan/spraakbanken/mc/test')
    # parser.add_argument('--wav_dir', type=str, default="../../../speaker_data/Spraakbanken-Corpus")
    # parser.add_argument('--log_dir', type=str, default='../../../trained_models/stargan/logs/spraakbanken')
    # parser.add_argument('--model_save_dir', type=str, default='../../../trained_models/stargan/spraakbanken')
    # parser.add_argument('--sample_dir', type=str, default='../../../trained_models/stargan/samples/spraakbanken')

    # Directories on SSH normal Spraakbanken dataset
    # parser.add_argument('--train_data_dir', type=str, default='/work1/s183921/preprocessed_data/stargan/spraakbanken/mc/train')
    # parser.add_argument('--test_data_dir', type=str, default='/work1/s183921/preprocessed_data/stargan/spraakbanken/mc/test')
    # parser.add_argument('--wav_dir', type=str, default="/work1/s183921/speaker_data/Spraakbanken-Corpus")
    # parser.add_argument('--log_dir', type=str, default='/work1/s183921/trained_models/stargan/logs/spraakbanken')
    # parser.add_argument('--model_save_dir', type=str, default='/work1/s183921/trained_models/stargan/spraakbanken')
    # parser.add_argument('--sample_dir', type=str, default='/work1/s183921/trained_models/stargan/samples/spraakbanken')

    # Directories on SSH spraakbanken-Test dataset
    parser.add_argument('--train_data_dir', type=str, default='/work1/s183921/preprocessed_data/stargan/spraakbanken/mc-Test-All-1/train')
    parser.add_argument('--test_data_dir', type=str, default='/work1/s183921/preprocessed_data/stargan/spraakbanken/mc-Test-All-1/test')
    parser.add_argument('--wav_dir', type=str, default="/work1/s183921/speaker_data/Spraakbanken-Corpus-Test")
    parser.add_argument('--log_dir', type=str, default='/work1/s183921/trained_models/stargan/logs/spraakbanken')
    parser.add_argument('--model_save_dir', type=str, default='/work1/s183921/trained_models/stargan/spraakbanken-Test-25-Final')
    parser.add_argument('--sample_dir', type=str, default='/work1/s183921/trained_models/stargan/samples/spraakbanken-Test-25-Final')


    # Step size.
    parser.add_argument('--log_step', type=int, default=10)
    parser.add_argument('--sample_step', type=int, default=1000)
    parser.add_argument('--model_save_step', type=int, default=5000)  # Specified, changed from 1000 to 10000
    parser.add_argument('--lr_update_step', type=int, default=1000)

    config = parser.parse_args()
    # print(config)
    main(config)
