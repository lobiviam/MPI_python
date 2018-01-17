import os
from timeit import default_timer as get_time

core_n_iterator = range(1, 8)
algorithms_iterator = ['gauss.py', 'simpson.py', 'trapezoid.py', 'rectangle.py']

# clear stats file
f = open("first_point_data_local_machine.csv", "w")
f.write('')
f.close()
# ready to write in clear stats file
f = open("first_point_data_local_machine.csv", "a")
f.write("algo_name, core_n, avg_time \n")

for alg in algorithms_iterator:
    for core_n in core_n_iterator:
        average_time = 0
        for i in range(0, 20):
            time_start = get_time()
            msg = os.system("mpiexec -n {0} python {1} 0.0 1.0 400000".format(core_n, alg))
            average_time += (get_time() - time_start)
        average_time /= 20
        f.write("{0}, {1}, {2} \n".format(alg, core_n, average_time))
f.close()
print('\n First point data generating completed!')
