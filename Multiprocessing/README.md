# Multiprocessing

Saving the images as png files allows to create the images in a different order than their framenumber, allowing the parallelization of generating the plots. Therefore, I used the module `multiprocessing` to speed up the code.

## Results
The performance comparison was done using two different sets of data. The first set had 212 profile.data files. The computation times were:
- PvsNMovie:
  - real  3m45.757s
  - user  3m51.436s
  - sys   0m3.992s
- PvsNMovie\_mpi(NUM\_THREADS=1):
  - real  4m21.415s
  - user  4m6.408s
  - sys  0m16.680s 
- PvsNMovie\_mpi (NUM\_THREADS=2):
  - real  2m22.177s
  - user  3m55.800s
  - sys   0m17.716s 
- PvsNMovie\_mpi (NUM\_THREADS=4):
  - real  2m2.966s
  - user  4m11.132s
  - sys   0m24.684s

The second set had 1420 profile.data files:
- PvsNMovie:
  - real  16m21.470s
  - user  17m7.600s
  - sys   0m6.220s
- PvsNMovie\_mpi(NUM\_THREADS=4):
  - real  5m56.876s
  - user  13m21.008s
  - sys   1m3.092s 
