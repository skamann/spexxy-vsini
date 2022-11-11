import logging
import argparse
import os
import numpy as np
from scipy.interpolate import UnivariateSpline

from spexxy.grid import Grid
from spexxy.data import SpectrumFits
from spexxy.interpolator.spline import calc_2nd_derivs_spline

log = logging.getLogger(__name__)


def add_parser(subparsers):
    # create parser
    parser = subparsers.add_parser('2ndderivs', help='Calculate 2nd derivativates for a given grid along its 1st axis',
                                   formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('input', type=str, help='Input grid')
    parser.add_argument('output', type=str, help='Output directory, in which a file grid is written')
    parser.add_argument('--norm-to-mean', action='store_true', help='Norm input spectra to mean.')

    # argparse wrapper for create_grid
    def run(args):
        calc_2nd_derivs(args.input, args.output, args.norm_to_mean)
    parser.set_defaults(func=run)


def calc_2nd_derivs(ingrid: str, outdir: str, norm_to_mean: bool = False):
    # load grid
    grid = Grid.load(ingrid)

    # outdir and grid file
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    with open(os.path.join(outdir, 'grid.csv'), 'w') as f:
        f.write('Filename,' + ','.join(grid.axis_names()) + '\n')

    # get first axis
    axis = grid.axes()[0]
    log.info('First axis is %s with %d values.', axis.name, len(axis.values))

    # get all parameter tuples
    all_params = grid.all()

    # load first spectrum to get wavelength array
    ref_spec = grid(all_params[0])
    log.info('Spectra in grid contain %d wavelength points.', len(ref_spec.wave))

    # get all parameter combinations without first parameter
    filtered_params = list(set([tuple(p[1:]) for p in all_params]))
    log.info('Found %d parameter combinations excluding 1st parameter.', len(filtered_params))

    # loop filtered params
    for i, params in enumerate(filtered_params, 1):
        log.info('(%d/%d) Calculating 2nd derivatives for %s...', i, len(filtered_params),
                 ' '.join(['%s=%.2f' % (k, v) for k, v in zip(grid.axis_names()[1:], params)]))

        # load all spectra with these parameters
        data = []
        avail_values = []
        for value in axis.values:
            try:
                # load spectrum
                spec = grid(tuple([value] + list(params)))

                # norm?
                if norm_to_mean:
                    spec.norm_to_mean()

                # append flux to data
                data.append(spec.flux)
                avail_values.append(value)

            except KeyError:
                # could not load spectrum
                continue

        # log
        log.info('Found %d different values for %s.', len(avail_values), axis.name)

        # calculate 2nd derivatives from spline
        derivs = calc_2nd_derivs_spline(avail_values, data)

        # loop spectra
        log.info('Writing spectra...')
        for i, value in enumerate(avail_values):
            # create spectrum
            spec = SpectrumFits(spec=ref_spec, flux=derivs[i, :])

            # create filename
            filename = 'spec_' + '_'.join(['%.2f' % p for p in [value] + list(params)]) + '.fits'

            # save it
            spec.save(os.path.join(outdir, filename))

            # add to CSV
            with open(os.path.join(outdir, 'grid.csv'), 'a') as csv:
                csv.write(filename + ',' + str(value) + ',' + ','.join([str(p) for p in params]) + '\n')
