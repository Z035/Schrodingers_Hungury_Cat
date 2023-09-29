import cirq
import random


def rot_x_layer(length, half_turns):
    """Yields X rotations by half_turns on a square grid of given length."""

    # Define the gate once and then re-use it for each Operation.
    rot = cirq.XPowGate(exponent=half_turns)

    # Create an X rotation Operation for each qubit in the grid.
    for i in range(length):
        for j in range(length):
            yield rot(cirq.GridQubit(i, j))


def rand2d(rows, cols):
    return [[random.choice([+1, -1]) for _ in range(cols)] for _ in range(rows)]


def random_instance(length):
    # transverse field terms
    h = rand2d(length, length)
    # links within a row
    jr = rand2d(length - 1, length)
    # links within a column
    jc = rand2d(length, length - 1)
    return h, jr, jc


def prepare_plus_layer(length):
    for i in range(length):
        for j in range(length):
            yield cirq.H(cirq.GridQubit(i, j))


def get_ansatz():
    pass


def main():
    # define qubits & circuit
    qubits = cirq.LineQubit.range(3)
    circuit = cirq.Circuit()

    for i in range(3):
        circuit.append(cirq.H(qubits[i]))

    print(circuit)



if __name__ == '__main__':
    main()

    # random instance try
    """
    h, jr, jc = random_instance(3)
    print(f'transverse fields: {h}')
    print(f'row j fields: {jr}')
    print(f'column j fields: {jc}')
    """
