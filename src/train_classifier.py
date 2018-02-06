#!/usr/bin/env python
import argparse
import os
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--result_dir', help='Output directory for images and model checkpoints [default: .]', default='.')
parser.add_argument('--epochs', type=int, default=10, help='number of epochs to train for [default: 10]')
parser.add_argument('--aux_dataset', help='Path to aux_dataset file [default: None]')

options = vars(parser.parse_args())

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from dataloader import FlexibleCustomDataloader
from training import train_classifier
from networks import build_networks, save_networks, get_optimizers
from options import load_options, get_current_epoch
from counterfactual import generate_counterfactual

options = load_options(options)
dataloader = FlexibleCustomDataloader(fold='train', **options)
networks = build_networks(dataloader.num_classes, **options)
optimizers = get_optimizers(networks, **options)

start_epoch = get_current_epoch(options['result_dir']) + 1
for epoch in range(start_epoch, start_epoch + options['epochs']):
    train_classifier(networks, optimizers, dataloader, epoch=epoch, **options)
    # TODO: Deal with wasteful copies of the non-classifier networks
    save_networks(networks, epoch, options['result_dir'])