# Multiprocessing

Saving the images as png files allows to create the images in a different order than their framenumber, allowing the parallelization of generating the plots. Therefore, I used the module `multiprocessing` to speed up the code.

## Results
The results obtained for a set of 212 profile.data files were:
- PvsNMovie_mpi (NUM_THREADS=3):
  - real  1m34.974s; 1m35.719s
  - user  3m30.644s; 3m30.440s
  - sys	  0m16.888s; 0m16.820s
- PvsNMovie_mpi (NUM_THREADS=4):
  - real  1m16.779s; 1m16.034s
  - user  3m32.880s; 3m31.668s
  - sys	  0m16.904s; 0m17.100s
- PvsNMovie_mpi(NUM_THREADS=1):
  - real  4m5.477s
  - user  3m53.200s
  - sys   0m15.636s 
