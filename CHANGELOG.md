## Changelog

### v2.5 (2020-07-14)
* Split MainRoutine into MainRoutine and FilesRoutine, allowing for routines that don't run on files.
* Added a SynspecGrid which can synthesize spectra using Synspec
* Added some command line tools
* Keep FITS headers when copying a SpectrumFitsHDU

### v2.4.1 (2020-06-19)
* Minor fix for lmfit call

### v2.4 (2020-06-10)
* Re-organized isochrones classes, added MultiIsochrone for external files.
* Added different polynomials and sanity check to "isochrone apply".
* Moved executables into their own module and use entry_points instead of scripts in setup.py.
* Added new continuum class PeakToPeak (by B. Giesers).
* Fixed FitsSpectrum to allow for setting the primary HDU.
* Some smaller changes.

### v2.3 (2019-11-15)
* Added iterative fitting in MultiMain (by B. Bischoff).
* Added new classes WeightFromGrid and WeightFromGridNearest (by B. Bischoff).
* Some bug fixes.

### v2.2 (2019-02-04)
* Renamed PhoenixGrid to FilesGrid and generalized it.
* Added Isochrone class and CLI methods.
* Added MaskNegative, that automatically masks negative pixels in spectra.
* In SplineInterpolator, calculate 2nd derivatives with more than just the direct neighbors.
* Added possibility to create PDF with one plot at each iteration. 
* Fixed bug about not plotting masks at end of spectra. 
* Added workaround for loading YAML config into an OrderedDict. Should be obsolete with Python 3.7.
* Changed output behaviour of main routines.
* Added "success" column to output of paramsfit.
* Fixed bug with handling valid pixels in paramsfit.
* Added new WeightFromSNR, which estimates pixel weights from flux and SNR.
* Multiple minor/major bug fixes.

### v2.1 (2018-11-26)
* Showing default values in help on command line.
* Moving fixing of parameters in ParamsFit from the constructor into the actual call, so that it is done after
  initializing the components.
* In ParamsFit, always allow parameters that are requested to be fitted to vary in the optimization. This gets important
  for the new "MultiMain", where a once fixed parameter can be allowed to vary in the next fit.
* Introduced new Weight classes, which handle weights for each pixel in a spectrum. Multiple weights are multiplied.
* Added two Weight classes: WeightFromSigma loads the SIGMA array from the FITS file (which acts the same as the
  default behaviour in the previous *spexxy* version), and WeightRanges assigns weights for given wavelength ranges.
* Updated documentation.

### v2.0 (2018-11-16)
* First published *spexxy* version.
