# emacs: -*- mode: python-mode; py-indent-offset: 4; tab-width: 4; indent-tabs-mode: nil -*-
# ex: set sts=4 ts=4 sw=4 et:
""" Network analysis-related methods """

from neurosynth.analysis import meta

def coactivation(dataset, seed, threshold=0.0, outroot=None, r=6):
  """ Compute and save coactivation map given input image as seed.

  This is essentially just a wrapper for a meta-analysis defined
  by the contrast between those studies that activate within the seed
  and those that don't.

  Args:
    dataset: a Dataset instance containing study and activation data.
    seed: either a Nifti or Analyze image defining the boundaries of the
      seed, or a list of triples (x/y/z) defining the seed(s). Note that 
      voxels do not need to be contiguous to define a seed--all supra-
      threshold voxels will be lumped together.
    threshold: optional float indicating the threshold above which voxels
      are considered to be part of the seed ROI (default = 0)
    r: optional integer indicating radius (in mm) of spheres to grow 
      (only used if seed is a list of coordinates).
    outroot: optional string to prepend to all coactivation images.
      If none, defaults to using the first part of the seed filename.

  Output:
    A set of meta-analysis images identical to that generated by 
    meta.MetaAnalysis.
  """

  if isinstance(seed, basestring):
    ids = dataset.get_ids_by_mask(seed, threshold=threshold)
  else:
    ids = dataset.get_ids_by_peaks(seed, r=r, threshold=threshold)

  ma = meta.MetaAnalysis(dataset, ids)
  if outroot is None:
    outroot = seed.split('.')[0] + "_coact"
  ma.save_results(outroot)
