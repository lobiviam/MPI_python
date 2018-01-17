import numpy
import sys
from mpi4py import MPI
from mpi4py.MPI import ANY_SOURCE
import math

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()


# define a function to integrate
def f(x):
    return 4 / (1 + x * x)


def integrate(a, b, n):
    h = (b - a) / n
    integral = 0
    z = h / math.sqrt(3)
    for i in range(1, int(n)):
        x = a + i * h
        x_12 = x - 0.5 * h
        integral = integral + (f(x_12 - z) +
                               f(x_12 + z)) * (h / 2)
    return integral


def main():
    # takes in command-line arguments [a,b,n]
    a = float(sys.argv[1])
    b = float(sys.argv[2])
    if len(sys.argv) == 5:
        step_size = float(sys.argv[4])
        n = (b - a) / step_size
    else:
        n = int(sys.argv[3])

    step_size = (b - a) / n
    local_n = n / size

    # calculate the interval that each process handles
    local_a = a + rank * local_n * step_size  # start point for certain process
    local_b = local_a + local_n * step_size  # end point

    integral = numpy.zeros(1)
    received = numpy.zeros(1)

    # each process integrates its own interval
    integral[0] = integrate(local_a, local_b, local_n)

    # root node receives results from all processes and sums them
    if rank == 0:
        total = integral[0]
        for i in range(1, size):
            comm.Recv(received, ANY_SOURCE)
            total += received[0]
    else:
        # all other process send their result
        comm.Send(integral, 0)

    # root process prints results
    if comm.rank == 0:
        return "Success!, integral is equal to {0}".format(total)


if __name__ == '__main__':
    main()
