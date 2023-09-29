from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit_research.protein_folding.interactions.miyazawa_jernigan_interaction import (
    MiyazawaJerniganInteraction,
)
from qiskit_research.protein_folding.peptide.peptide import Peptide
from qiskit_research.protein_folding.protein_folding_problem import (
    ProteinFoldingProblem,
)

from qiskit_research.protein_folding.penalty_parameters import PenaltyParameters
from qiskit.utils import algorithm_globals

from qiskit.circuit.library import RealAmplitudes
from qiskit.algorithms.optimizers import COBYLA
from qiskit.algorithms.minimum_eigensolvers import SamplingVQE
from qiskit_ibm_runtime import Sampler, Session
from qiskit_ibm_runtime import QiskitRuntimeService

# IBM Quantum channel; set to default
QiskitRuntimeService.save_account(channel="ibm_quantum",
                                  token="",
                                  overwrite=True)

counts = []
values = []


def store_intermediate_result(eval_count, parameters, mean, std):
    counts.append(eval_count)
    values.append(mean)


def main():
    # Initializing Peptide Chain
    algorithm_globals.random_seed = 23
    main_chain = "IMVAEARAAAA"
    side_chains = [""] * 11

    # Defining interactions & penalty
    mj_interaction = MiyazawaJerniganInteraction()
    penalty_back = 10
    penalty_chiral = 10
    penalty_1 = 10
    penalty_terms = PenaltyParameters(penalty_chiral, penalty_back, penalty_1)

    peptide = Peptide(main_chain, side_chains)

    protein_folding_problem = ProteinFoldingProblem(peptide, mj_interaction, penalty_terms)
    qubit_op = protein_folding_problem.qubit_op()

    print(qubit_op)

    optimizer = COBYLA(maxiter=50)
    # set variational ansatz
    ansatz = RealAmplitudes(reps=1)

    with Session(backend="ibmq_qasm_simulator") as session:
        sampler = Sampler(session=session)

        # initialize VQE
        vqe = SamplingVQE(
            sampler,
            ansatz=ansatz,
            optimizer=optimizer,
            aggregation=0.1,
            callback=store_intermediate_result,
        )

        raw_result = vqe.compute_minimum_eigenvalue(qubit_op)
        print(raw_result)

        # noinspection PyTypeChecker
        result = protein_folding_problem.interpret(raw_result=raw_result)

        # Close the session only if all jobs are finished and
        # you don't need to run more in the session.
        session.close()

    # Visualize
    fig = result.get_figure(title="Protein Structure", ticks=False, grid=True)
    fig.get_axes()[0].view_init(10, 70)
    fig.savefig("folding_fig.png")


if __name__ == '__main__':
    main()
