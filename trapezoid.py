import numpy
import sys
import math
from mpi4py import MPI
from mpi4py.MPI import ANY_SOURCE

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# function to integrate
def f(x):
    return 4 / (1 + math.pow(x, 2))


def integrate(a, b, n):
    integral = 0
    step = (b - a) / n
    for i in range(1, int(n)):
        x = a + i * step
        integral = integral + (f(x - step)+f(x))*step*0.5
    return integral

def main():
    # takes in command-line arguments [a,b,n]
    a = float(sys.argv[1])
    b = float(sys.argv[2])
    n = int(sys.argv[3])

    step_size = (b - a) / n
    # current_n is the number of rectangles
    current_n = n / size

    current_a = a + rank * current_n * step_size  # start point for certain process
    current_b = current_a + current_n * step_size  # end point

    integral = numpy.zeros(1)
    received = numpy.zeros(1)

    integral[0] = integrate(current_a, current_b, current_n)
    # root node receives results from all processes and sums them
    if rank == 0:
        total = integral[0]
        for i in range(1, size):
            comm.Recv(received, ANY_SOURCE)
            total += received[0]
    else:
        # other process send their result
        comm.Send(integral, 0)

    if comm.rank == 0:
        return "Success!, integral is equal to {0}".format(total)

if __name__ == '__main__':
    main()