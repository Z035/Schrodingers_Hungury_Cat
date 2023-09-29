import dimod
import dwave.inspector


def main():
    service = QiskitRuntimeService()
    backend = service.get_backend("ibmq_qasm_simulator")


if __name__ == '__main__':
    main()
