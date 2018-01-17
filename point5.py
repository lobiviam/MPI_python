import os
from timeit import default_timer as get_time

b_iterator = range(1, 5)
algorithms_iterator = ['gauss.py', 'simpson.py', 'trapezoid.py', 'rectangle.py']

# clear stats file
f = open("last_point_data_local_machine.csv", "w")
f.write('')
f.close()
# ready to write in clear stats file
f = open("last_point_data_local_machine.csv", "a")
f.write("algo_name, b, avg_time \n")

for alg in algorithms_iterator:
    for b in b_iterator:
        average_time = 0
        for i in range(0, 20):
            time_start = get_time()
            msg = os.system("mpiexec -n 4 python {0} 0.0 {1} 400 0.01".format(alg,b))
            average_time += (get_time() - time_start)
        average_time /= 20
        f.write("{0}, {1}, {2} \n".format(alg, b, average_time))
f.close()
print('\n Last point data generating completed!')
