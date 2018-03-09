import argparse
import os.path
import sys
import re
import time

import qiskit

if sys.version_info < (3,0):
    raise Exception("Please use Python version 3 or greater.")

def runBenchmark(name, qubit, backend, depth):
    
    if depth > 0 : 
        qasm = name + "/" + name + "_n" + str(qubit) + "_d" + str(depth) + ".qasm"
    else:
        qasm = name + "/" + name + "_n" + str(qubit) + ".qasm"
    
    if not os.path.exists(qasm):
        return False
    
    qp = qiskit.QuantumProgram()
    
    if backend.startswith("ibmqx"):
        import Qconfig
        qp.set_api(Qconfig.APItoken, Qconfig.config['url'])
    elif not backend.startswith("local"):
        raise Exception('only ibmqx or local simulators are supported')
        
    qp.load_qasm_file(qasm, name=name)
    
    start = time.time() 
    ret = qp.execute([name], backend=backend, shots=1, max_credits=5, hpc=None, timeout=60*60*24)
    elapsed = time.time() - start
    
    if not ret.get_circuit_status(0) == "DONE":
        return False
    
    if backend.startswith("ibmqx"):
        elapsed = ret.get_data(name)["time"]
    
    print(name + "," + backend + "," + str(qubit) + "," + str(depth) + "," + str(elapsed), flush=True)
    
    return True

def parse_args():
    parser = argparse.ArgumentParser(
        description=("Evaluate the performance of simulator with and prints a report."))
    
    parser.add_argument('-a', '--name', default='qft', help='benchmark name')
    parser.add_argument('-s', '--start', default='4', help='minimum qubits for evaluation')
    parser.add_argument('-e', '--end', default='10', help='maximum qubits for evaluation')
    parser.add_argument('-d', '--depth', default='0', help='depth')
    parser.add_argument('-b', '--backend', default='local_qasm_simulator', help='backend name')
    
    return parser.parse_args();

def _main():
    args = parse_args()
    
    for qubit in range(int(args.start), int(args.end)):
        if not runBenchmark(name=args.name, qubit=qubit, backend=args.backend, depth=int(args.depth)):
            break

def main():
    try:
        _main()
    except KeyboardInterrupt:
        print("Benchmark suite interrupted: exit!")
        sys.exit(1)

if __name__ == "__main__":
  main()
