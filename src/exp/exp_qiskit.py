import time
import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt

from exp_qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from exp_qiskit.algorithms.minimum_eigensolvers import VQE
from exp_qiskit.algorithms.optimizers import SPSA
from exp_qiskit.primitives import BaseEstimator

from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit_ibm_runtime import Estimator, Session

# Pre-defined ansatz circuit for exp
from exp_qiskit.circuit.library import RealAmplitudes


def get_ansatz():
    qreg = QuantumRegister(3)
    creg = ClassicalRegister(3)
    circuit = QuantumCircuit(qreg, creg)

    return circuit


def show_circuit(circuit):
    figure = circuit.draw(output='mpl')
    figure.savefig("graph.png")


def main():
    ansatz = RealAmplitudes(num_qubits=4)
    show_circuit(ansatz)
    estimator = BaseEstimator()
    optimizer = SPSA(maxiter=1000)
    vqe = VQE(estimator, ansatz, optimizer)



if __name__ == '__main__':
    main()
