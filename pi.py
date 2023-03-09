from mpi4py import MPI
import random
from decimal import Decimal

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()


N = 1000000 // size
count = 0

# Generate random points using stratified sampling and count the number of points inside the circle
for i in range(N):
    xi = Decimal(i + rank * N + random.uniform(0, 1)) / Decimal(N * size)
    yi = Decimal(random.uniform(0, 1))
    if xi**2 + yi**2 <= 1:
        count += 1

# Send the count from each process to the root process
if rank != 0:
    comm.send(count, dest=0)
else:
    total_count = count
    for i in range(1, size):
        count_received = comm.recv(source=i)
        print("Source: "+str(i)+" Count of points: "+str(count_received))
        total_count += count_received

# Compute the final estimate of pi on the root process
if rank == 0:
    pi = 4 * total_count / Decimal(N * size) 
    print("Estimated value of pi:", pi)
