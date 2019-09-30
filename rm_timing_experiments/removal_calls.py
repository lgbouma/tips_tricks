import numpy as np
import datetime
import os, sys, subprocess
from glob import glob

import multiprocessing as mp

def touch(fpath, times=None):
    fhandle = open(fpath, 'a')
    try:
        os.utime(fpath, times)
    finally:
        fhandle.close()

def make_many_files(N_files=1000):

    # first, make many files
    tempdir = '/home/luke/temp/'
    if not os.path.exists(tempdir):
        os.mkdir(tempdir)

    fpaths = []
    for f in range(0,N_files):
        fpath = os.path.join(tempdir,str(f)+'.txt')
        touch(fpath)
        fpaths.append(fpath)

    return fpaths

def _touch_worker(task):
    f = task
    touch(fpath)


def parallel_make_many_files(N_files=1000, nworkers=16, maxworkertasks=1000):

    # first, make many files
    tempdir = '/home/luke/temp/'
    if not os.path.exists(tempdir):
        os.mkdir(tempdir)

    tasks = [os.path.join(tempdir,str(f)+'.txt') for f in range(0,N_files)]

    fpaths = tasks

    pool = mp.Pool(nworkers,maxtasksperchild=maxworkertasks)
    results = pool.map(_touch_worker, tasks)

    pool.close()
    pool.join()

    return fpaths



def chunks_generator(l, n):
    """Yield successive n-sized chunks from l"""
    for i in range(0, len(l), n):
        max_ind = i+n
        if max_ind > len(l) -1:
            max_ind = len(l)
        yield l[i:max_ind], i, max_ind


def _rm_chunk_worker(task):
    # given a list of <~ 10,000 file names (and start/end inds for verbosity),
    # remove them.
    chunkfiles, i, max_ind = task

    fpathstr = ' '.join(chunkfiles)
    cmdtorun = 'rm {}'.format(fpathstr)
    subprocess.run(cmdtorun.split(' '))

    print('rm {} to {}...'.format(i, max_ind))

    return 1


def rm_named_files(filepaths, N_chunk=int(1e4), nworkers=1, maxworkertasks=1000):
    """
    given a list of files, delete them.

    under the hood:
    * if you have <=1e4 files, does a simple long-form rm call.
    * if you have >1e4 files, splits the list of files into chunks, does
    multiple long-form rm calls.
    """

    N_to_rm = len(filepaths)

    if not isinstance(filepaths,list):
        raise AssertionError

    if N_to_rm <= N_chunk:

        subprocess.run(['rm']+filepaths)

        print('called rm on {} files'.format(N_to_rm))

    elif N_to_rm > N_chunk and nworkers==1:

        for chunkfiles, i, max_ind in chunks_generator(filepaths, N_chunk):

            print('rm {} to {}...'.format(i, max_ind))

            fpathstr = ' '.join(chunkfiles)
            cmdtorun = 'rm {}'.format(fpathstr)
            subprocess.run(cmdtorun.split(' '))

        print('called rm on {} files'.format(N_to_rm))

    elif N_to_rm > N_chunk and nworkers > 1:

        # make a list of the chunks/sublists (these will be "tasks").
        tasks = []
        for chunkfiles, i, max_ind in chunks_generator(filepaths, N_chunk):
            tasks.append((chunkfiles, i, max_ind))

        pool = mp.Pool(nworkers,maxtasksperchild=maxworkertasks)
        results = pool.map(_rm_chunk_worker, tasks)

        pool.close()
        pool.join()

        print('called rm on {} files'.format(N_to_rm))

    return 1


def main():

    # make files, delete them individually by passing them all thru rm
    for N_files in list(map(int,[1e3,1e4,9.8e4])):

        # make files, delete them by directory removal
        fpaths = parallel_make_many_files(N_files=N_files)
        cmdtorun = 'rm -rf /home/luke/temp'
        t0 = datetime.datetime.now()
        returncode = os.system(cmdtorun)
        t1 = datetime.datetime.now()
        tdelt = (t1-t0).total_seconds()
        print('rm -rf directory, {} files: {} seconds'.format(N_files, tdelt))

        # make files, delete them individually by passing them all thru rm
        nworkers = 1
        fpaths = parallel_make_many_files(N_files=N_files)
        t0 = datetime.datetime.now()
        rm_named_files(fpaths, N_chunk=int(2e4), nworkers=nworkers)
        t1 = datetime.datetime.now()
        tdelt = (t1-t0).total_seconds()
        print('rm INDIVIDUAL files {} worker, {} files: {} seconds'.
              format(nworkers, N_files, tdelt))

        # same but multithread
        nworkers = 16
        fpaths = parallel_make_many_files(N_files=N_files)
        t0 = datetime.datetime.now()
        rm_named_files(fpaths, N_chunk=int(2e4), nworkers=nworkers)
        t1 = datetime.datetime.now()
        tdelt = (t1-t0).total_seconds()
        print('rm INDIVIDUAL files {} workers, {} files: {} seconds'.
              format(nworkers, N_files, tdelt))


if __name__ == "__main__":
    main()
