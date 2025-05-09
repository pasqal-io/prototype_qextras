from __future__ import annotations

from dataclasses import dataclass, field, fields
from logging import getLogger
from typing import Callable, Type

from sympy import Basic

from qadence.blocks.analog import AnalogBlock
from qadence.blocks.primitive import ParametricBlock
from qadence.operations import RX, AnalogRX
from qadence.parameters import Parameter
from qadence.types import (
    AnsatzType,
    BasisSet,
    MultivariateStrategy,
    ReuploadScaling,
    Strategy,
)

logger = getLogger(__file__)


@dataclass
class FeatureMapConfig:
    num_features: int = 0
    """
    Number of feature parameters to be encoded.

    Defaults to 0. Thus, no feature parameters are encoded.
    """

    basis_set: BasisSet | dict[str, BasisSet] = BasisSet.FOURIER
    """
    Basis set for feature encoding.

    Takes qadence.BasisSet.
    Give a single BasisSet to use the same for all features.
    Give a dict of (str, BasisSet) where the key is the name of the variable and the
    value is the BasisSet to use for encoding that feature.
    BasisSet.FOURIER for Fourier encoding.
    BasisSet.CHEBYSHEV for Chebyshev encoding.
    """

    reupload_scaling: ReuploadScaling | dict[str, ReuploadScaling] = ReuploadScaling.CONSTANT
    """
    Scaling for encoding the same feature on different qubits.

    Scaling used to encode the same feature on different qubits in the
    same layer of the feature maps. Takes qadence.ReuploadScaling.
    Give a single ReuploadScaling to use the same for all features.
    Give a dict of (str, ReuploadScaling) where the key is the name of the variable and the
    value is the ReuploadScaling to use for encoding that feature.
    ReuploadScaling.CONSTANT for constant scaling.
    ReuploadScaling.TOWER for linearly increasing scaling.
    ReuploadScaling.EXP for exponentially increasing scaling.
    """

    feature_range: tuple[float, float] | dict[str, tuple[float, float]] | None = None
    """
    Range of data that the input data is assumed to come from.

    Give a single tuple to use the same range for all features.
    Give a dict of (str, tuple) where the key is the name of the variable and the
    value is the feature range to use for that feature.
    """

    target_range: tuple[float, float] | dict[str, tuple[float, float]] | None = None
    """
    Range of data the data encoder assumes as natural range.

    Give a single tuple to use the same range for all features.
    Give a dict of (str, tuple) where the key is the name of the variable and the
    value is the target range to use for that feature.
    """

    multivariate_strategy: MultivariateStrategy = MultivariateStrategy.PARALLEL
    """
    The encoding strategy in case of multi-variate function.

    Takes qadence.MultivariateStrategy.
    If PARALLEL, the features are encoded in one block of rotation gates
    with the register being split in sub-registers for each feature.
    If SERIES, the features are encoded sequentially using the full register for each feature, with
    an ansatz block between them. PARALLEL is allowed only for DIGITAL `feature_map_strategy`.
    """

    feature_map_strategy: Strategy = Strategy.DIGITAL
    """
    Strategy for feature map.

    Accepts DIGITAL, ANALOG or RYDBERG. Defaults to DIGITAL.
    If the strategy is incompatible with the `operation` chosen, then `operation`
    gets preference and the given strategy is ignored.
    """

    param_prefix: str | None = None
    """
    String prefix to create trainable parameters in Feature Map.

    A string prefix to create trainable parameters multiplying the feature parameter
    inside the feature-encoding function. Note that currently this does not take into
    account the domain of the feature-encoding function.
    Defaults to `None` and thus, the feature map is not trainable.
    Note that this is separate from the name of the parameter.
    The user can provide a single prefix for all features, and it will be appended
    by appropriate feature name automatically.
    """

    num_repeats: int | dict[str, int] = 0
    """
    Number of feature map layers repeated in the data reuploading step.

    If all features are to be repeated the same number of times, then can give a single
    `int`. For different number of repetitions for each feature, provide a dict
    of (str, int) where the key is the name of the variable and the value is the
    number of repetitions for that feature.
    This amounts to the number of additional reuploads. So if `num_repeats` is N,
    the data gets uploaded N+1 times. Defaults to no repetition.
    """

    operation: Callable[[Parameter | Basic], AnalogBlock] | Type[RX] | None = None
    """
    Type of operation.

    Choose among the analog or digital rotations or a custom
    callable function returning an AnalogBlock instance. If the type of operation is
    incompatible with the `strategy` chosen, then `operation` gets preference and
    the given strategy is ignored.
    """

    inputs: list[Basic | str] | None = None
    """
    List that indicates the order of variables of the tensors that are passed.

    Optional if a single feature is being encoded, required otherwise. Given input tensors
    `xs = torch.rand(batch_size, input_size:=2)` a QNN with `inputs=["t", "x"]` will
    assign `t, x = xs[:,0], xs[:,1]`.
    """

    tag: str | None = None
    """
    String to indicate the name tag of the feature map.

    Defaults to None, in which case no tag will be applied.
    """

    def __post_init__(self) -> None:
        if self.multivariate_strategy == MultivariateStrategy.PARALLEL and self.num_features > 1:
            assert (
                self.feature_map_strategy == Strategy.DIGITAL
            ), "For parallel encoding of multiple features, the `feature_map_strategy` must be \
                  of `Strategy.DIGITAL`."

        if self.operation is None:
            if self.feature_map_strategy == Strategy.DIGITAL:
                self.operation = RX
            elif self.feature_map_strategy == Strategy.ANALOG:
                self.operation = AnalogRX  # type: ignore[assignment]

        else:
            if self.feature_map_strategy == Strategy.DIGITAL:
                if isinstance(self.operation, AnalogBlock):
                    logger.warning(
                        "The `operation` is of type `AnalogBlock` but the `feature_map_strategy` is\
                        `Strategy.DIGITAL`. The `feature_map_strategy` will be modified and given \
                        operation will be used."
                    )

                    self.feature_map_strategy = Strategy.ANALOG

            elif self.feature_map_strategy == Strategy.ANALOG:
                if isinstance(self.operation, ParametricBlock):
                    logger.warning(
                        "The `operation` is a digital gate but the `feature_map_strategy` is\
                        `Strategy.ANALOG`. The `feature_map_strategy` will be modified and given\
                        operation will be used."
                    )

                    self.feature_map_strategy = Strategy.DIGITAL

            elif self.feature_map_strategy == Strategy.RYDBERG:
                if self.operation is not None:
                    logger.warning(
                        f"feature_map_strategy is `Strategy.RYDBERG` which does not take any\
                        operation. But an operation {self.operation} is provided. The \
                        `feature_map_strategy` will be modified and given operation will be used."
                    )

                    if isinstance(self.operation, AnalogBlock):
                        self.feature_map_strategy = Strategy.ANALOG
                    else:
                        self.feature_map_strategy = Strategy.DIGITAL

        if self.inputs is not None:
            assert (
                len(self.inputs) == self.num_features
            ), "Inputs list must be of same size as the number of features"
        else:
            if self.num_features == 0:
                self.inputs = []
            elif self.num_features == 1:
                self.inputs = ["x"]
            else:
                raise ValueError(
                    """
                    Your QNN has more than one input. Please provide a list of inputs in the order
                    of your tensor domain. For example, if you want to pass
                    `xs = torch.rand(batch_size, input_size:=3)` to you QNN, where
                    ```
                    t = x[:,0]
                    x = x[:,1]
                    y = x[:,2]
                    ```
                    you have to specify
                    ```
                    inputs=["t", "x", "y"]
                    ```
                    You can also pass a list of sympy symbols.
                """
                )

        property_list = [
            "basis_set",
            "reupload_scaling",
            "feature_range",
            "target_range",
            "num_repeats",
        ]

        for target_field in fields(self):
            if target_field.name in property_list:
                prop = getattr(self, target_field.name)
                if isinstance(prop, dict):
                    assert set(prop.keys()) == set(
                        self.inputs
                    ), f"The keys in {target_field.name} must be the same as the inputs provided. \
                    Alternatively, provide a single value of {target_field.name} to use the same\
                    {target_field.name} for all features."
                else:
                    prop = {key: prop for key in self.inputs}
                    setattr(self, target_field.name, prop)


@dataclass
class AnsatzConfig:
    depth: int = 1
    """Number of layers of the ansatz."""

    ansatz_type: AnsatzType = AnsatzType.HEA
    """What type of ansatz.

    `AnsatzType.HEA` for Hardware Efficient Ansatz.
    `AnsatzType.IIA` for Identity Intialized Ansatz.
    `AnsatzType.ALA` for Alternating Layer Ansatz.
    """

    ansatz_strategy: Strategy = Strategy.DIGITAL
    """Ansatz strategy.

    `Strategy.DIGITAL` for fully digital ansatz. Required if `ansatz_type` is `AnsatzType.ALA`.
    `Strategy.SDAQC` for analog entangling block. Only available for `AnsatzType.HEA` or
    `AnsatzType.ALA`.
    `Strategy.RYDBERG` for fully rydberg hea ansatz. Only available for `AnsatzType.HEA`.
    """

    strategy_args: dict = field(default_factory=dict)
    """
    A dictionary containing keyword arguments to the function creating the ansatz.

    Details about each below.

    For `Strategy.DIGITAL` strategy, accepts the following:
        periodic (bool): if the qubits should be linked periodically.
            periodic=False is not supported in emu-c.
        operations (list): list of operations to cycle through in the
            digital single-qubit rotations of each layer.
            Defaults to  [RX, RY, RX] for hea and [RX, RY] for iia.
        entangler (AbstractBlock): 2-qubit entangling operation.
            Supports CNOT, CZ, CRX, CRY, CRZ, CPHASE. Controlld rotations
            will have variational parameters on the rotation angles.
            Defaults to CNOT

    For `Strategy.SDAQC` strategy, accepts the following:
        operations (list): list of operations to cycle through in the
            digital single-qubit rotations of each layer.
            Defaults to  [RX, RY, RX] for hea and [RX, RY] for iia.
        entangler (AbstractBlock): Hamiltonian generator for the
            analog entangling layer. Time parameter is considered variational.
            Defaults to NN interaction.

    For `Strategy.RYDBERG` strategy, accepts the following:
        addressable_detuning: whether to turn on the trainable semi-local addressing pattern
            on the detuning (n_i terms in the Hamiltonian).
            Defaults to True.
        addressable_drive: whether to turn on the trainable semi-local addressing pattern
            on the drive (sigma_i^x terms in the Hamiltonian).
            Defaults to False.
        tunable_phase: whether to have a tunable phase to get both sigma^x and sigma^y rotations
            in the drive term. If False, only a sigma^x term will be included in the drive part
            of the Hamiltonian generator.
            Defaults to False.
    """
    # The default for a dataclass can not be a mutable object without using this default_factory.

    m_block_qubits: int | None = None
    """
    The number of qubits in the local entangling block of an Alternating Layer Ansatz (ALA).

    Only used when `ansatz_type` is `AnsatzType.ALA`.
    """

    param_prefix: str = "theta"
    """The base bame of the variational parameter."""

    tag: str | None = None
    """
    String to indicate the name tag of the ansatz.

    Defaults to None, in which case no tag will be applied.
    """

    def __post_init__(self) -> None:
        if self.ansatz_type == AnsatzType.IIA:
            assert (
                self.ansatz_strategy != Strategy.RYDBERG
            ), "Rydberg strategy not allowed for Identity-initialized ansatz."

        if self.ansatz_type == AnsatzType.ALA:
            assert (
                self.ansatz_strategy == Strategy.DIGITAL
            ), f"{self.ansatz_strategy} not allowed for Alternating Layer Ansatz.\
            Only `Strategy.DIGITAL` allowed."

            assert (
                self.m_block_qubits is not None
            ), "m_block_qubits must be specified for Alternating Layer Ansatz."
