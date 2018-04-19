"""TrackML randomized submissions from truth"""

__authors__ = ['Moritz Kiehn']

import pandas
import numpy
import numpy.random

def _make_submission(mapping, track_ids, renumber=True):
    """Create a submission DataFrame with hit_id and track_id columns.

    Optionally renumbers the track_id to random small integers.
    """
    hit_ids = mapping['hit_id']
    if renumber:
        unique_ids, inverse = numpy.unique(track_ids, return_inverse=True)
        numbers = numpy.arange(1, len(unique_ids) + 1, dtype=unique_ids.dtype)
        numpy.random.shuffle(numbers)
        track_ids = numbers[inverse]
    return pandas.DataFrame({'hit_id': hit_ids, 'track_id': track_ids})

def set_seed(seed):
    """Set the random seed used for randomness in this module."""
    numpy.random.seed(seed)

def random_solution(truth, ntracks):
    """Generate a completely random solution with the given number of particles.

    Parameters
    ----------
    truth : pandas.DataFrame
        Truth mapping must contain hit_id and particle_id columns.
    ntracks : int
        Number of tracks the submission should contain.
    """
    ids = numpy.random.randint(1, nparticles + 1, size=len(mapping), dtype='i4')
    return _make_submission(truth, ids, renumber=False)

def drop_hits(truth, probability):
    """Drop hits from each track with a certain probability.

    Each dropped hit is assigned to a new particle that only contains this hit.

    Parameters
    ----------
    truth : pandas.DataFrame
        Truth mapping must contain hit_id and particle_id columns.
    probability : float
        The probability for a single hit to be dropped from the track.
    """
    out = numpy.array(truth['particle_id'], copy=True)
    dropped_mask = (numpy.random.random_sample(len(out)) < probability)
    dropped_count = numpy.count_nonzero(dropped_mask)
    fakeid0 = numpy.max(out) + 1
    fakeids = numpy.arange(fakeid0, fakeid0 + dropped_count, dtype='i8')
    # replace masked particle ids with fakes ones
    numpy.place(out, dropped_mask, fakeids)
    return _make_submission(truth, out)

def shuffle_hits(truth, probability):
    """Randomly assign hits to a wrong particle with a certain probability.

    Parameters
    ----------
    truth : pandas.DataFrame
        Truth mapping must contain hit_id and particle_id columns.
    probability : float
        The probability for a single hit to be reassigned to a different track.
    """
    out = numpy.array(truth['particle_id'], copy=True)
    shuffled_mask = (numpy.random.random_sample(len(out)) < probability)
    shuffled_count = numpy.count_nonzero(shuffled_mask)
    wrongparticles = numpy.random.choice(numpy.unique(out), size=shuffled_count)
    # replace masked particle ids with random valid ids
    numpy.place(out, shuffled_mask, wrongparticles)
    return _make_submission(truth, out)