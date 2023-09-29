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
from qiskit.primitives import Sampler

counts = []
values = []


def store_intermediate_result(eval_count, parameters, mean, std):
    counts.append(eval_count)
    values.append(mean)


def main():
    # Initializing Peptide Chain
    algorithm_globals.random_seed = 23
    main_chain = "IMVAEAR"
    side_chains = [""] * 7

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

    optimizer = COBYLA(maxiter=5)
    # set variational ansatz
    ansatz = RealAmplitudes(reps=1)

    # initialize VQE
    vqe = SamplingVQE(
        Sampler(),
        ansatz=ansatz,
        optimizer=optimizer,
        aggregation=0.1,
        callback=store_intermediate_result,
    )

    raw_result = vqe.compute_minimum_eigenvalue(qubit_op)
    print(raw_result)

    result = protein_folding_problem.interpret(raw_result=raw_result)

    # Visualize
    fig = result.get_figure(title="Protein Structure", ticks=False, grid=True)
    fig.get_axes()[0].view_init(10, 70)
    fig.savefig("folding_fig.png")


if __name__ == '__main__':
    main()
