import click
import logging
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from sklearn.externals import joblib
import yaml
import pandas as pd

from ..plotting import (
    plot_regressor_confusion,
    plot_bias_resolution,
    plot_feature_importances,
)


@click.command()
@click.argument('configuration_path', type=click.Path(exists=True, dir_okay=False))
@click.argument('performance_path', type=click.Path(exists=True, dir_okay=False))
@click.argument('model_path', type=click.Path(exists=True, dir_okay=False))
@click.option('-o', '--output', type=click.Path(exists=False, dir_okay=False))
@click.option('-k', '--key', help='HDF5 key for pandas hdf5', default='table')
def main(configuration_path, performance_path, model_path, output, key):
    ''' Create some performance evaluation plots for the separator '''
    logging.basicConfig(level=logging.INFO)
    log = logging.getLogger()

    log.info('Loading perfomance data')
    df = pd.read_hdf(performance_path, key)

    log.info('Loading model')
    model = joblib.load(model_path)

    with open(configuration_path) as f:
        config = yaml.load(f)

    figures = []

    # Plot confusion
    figures.append(plt.figure())
    ax = figures[-1].add_subplot(1, 1, 1)
    ax.set_title('Reconstructed vs. True Energy (log color scale)')
    plot_regressor_confusion(df, ax=ax)

    # Plot confusion
    figures.append(plt.figure())
    ax = figures[-1].add_subplot(1, 1, 1)
    ax.set_title('Reconstructed vs. True Energy (linear color scale)')
    plot_regressor_confusion(df, log_z=False, ax=ax)

    # Plot bias/resolution
    figures.append(plt.figure())
    ax = figures[-1].add_subplot(1, 1, 1)
    ax.set_title('Bias and Resolution')
    plot_bias_resolution(df, bins=15, ax=ax)

    # Plot feature importances
    figures.append(plt.figure())
    ax = figures[-1].add_subplot(1, 1, 1)

    plot_feature_importances(model, config['training_variables'], ax=ax)

    if output is None:
        plt.show()
    else:
        with PdfPages(output) as pdf:
            for fig in figures:
                pdf.savefig(fig)