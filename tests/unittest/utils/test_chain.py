import pytest
from hypothesis import given
from hypothesis import strategies as st

from pytomation.utils.chain import chain_process


@pytest.fixture
def simple_chain():
    """Fixture to create a simple chain that modifies the context."""

    def chain_fn(handler, ctx):
        # Simple chain that just forwards a string as the context
        handler("simple_chain_context")

    return chain_fn


@pytest.fixture
def context_chain():
    """Fixture to create a chain that uses and modifies context."""

    def chain_fn(handler, ctx):
        # Chain that modifies context
        new_ctx = f"{ctx}_modified" if ctx else "default_modified"
        handler(new_ctx)

    return chain_fn


@pytest.fixture
def complex_chain():
    """Fixture to create a complex chain that forwards the context and processes."""

    def chain_fn(handler, ctx):
        # Chain that performs some processing on context
        if ctx:
            new_ctx = ctx * 2  # Duplicate the context string
        else:
            new_ctx = "default_context"
        handler(new_ctx)

    return chain_fn


# Regular tests with pre-defined values


@pytest.mark.parametrize(
    "initial_context, expected_output",
    [
        (None, "simple_chain_context"),
        ("start", "simple_chain_context"),
    ],
)
def test_simple_chain(simple_chain, initial_context, expected_output):
    """Test simple chain that forwards a context."""
    result = chain_process([simple_chain], initial_context)
    assert result == expected_output


@pytest.mark.parametrize(
    "initial_context, expected_output",
    [
        (None, "default_modified"),
        ("start", "start_modified"),
    ],
)
def test_context_chain(context_chain, initial_context, expected_output):
    """Test chain that modifies context based on input."""
    result = chain_process([context_chain], initial_context)
    assert result == expected_output


@pytest.mark.parametrize(
    "chains, initial_context, expected_output",
    [
        ([], None, None),  # No chains, should return None
        ([], "start", "start"),  # No chains but initial context, should return initial context
        (["simple"], None, "simple_chain_context"),
        (["context"], "start", "start_modified"),
        (["context", "complex"], "start", "start_modifiedstart_modified"),
    ],
)
def test_multiple_chains(chains, initial_context, expected_output, simple_chain, context_chain, complex_chain):
    """Test multiple chains where one chain modifies the context and another processes it."""

    # Create the list of chain functions based on the provided strings
    chain_map = {"simple": simple_chain, "context": context_chain, "complex": complex_chain}

    chain_funcs = [chain_map[chain] for chain in chains]

    result = chain_process(chain_funcs, initial_context)
    assert result == expected_output


def test_empty_chain():
    """Test an empty chain to ensure process behaves correctly."""
    result = chain_process([], None)
    assert result is None

    result_with_ctx = chain_process([], "initial_ctx")
    assert result_with_ctx == "initial_ctx"


@pytest.mark.parametrize(
    "chains, expected_exception",
    [
        (None, TypeError),  # Passing None as chains should raise TypeError
        ([None], TypeError),  # Invalid chain (None) should raise a TypeError
    ],
)
def test_invalid_chains(chains, expected_exception):
    """Test edge cases with invalid chain input."""
    with pytest.raises(expected_exception):
        chain_process(chains)


# Fuzzy Tests with Hypothesis for Randomized Input Testing


@given(
    initial_context=st.one_of(st.none(), st.text(), st.integers(), st.floats(), st.booleans()),
    chain_output=st.one_of(st.text(), st.integers(), st.none()),
)
def test_fuzzy_single_chain(initial_context, chain_output):
    """Test process with a single chain that outputs random types."""

    def fuzzy_chain(handler, ctx):
        # Chain that forwards random data
        handler(chain_output)

    result = chain_process([fuzzy_chain], initial_context)
    assert result == chain_output


@given(
    initial_context=st.one_of(st.none(), st.text(), st.integers(), st.floats(), st.booleans()),
    chain_outputs=st.lists(st.one_of(st.text(), st.integers(), st.floats(), st.none()), min_size=1, max_size=10),
)
def test_fuzzy_multiple_chains(initial_context, chain_outputs):
    """Test process with multiple chains that output random types."""

    def create_fuzzy_chain(output):
        def fuzzy_chain(handler, ctx):
            handler(output)

        return fuzzy_chain

    # Create chains based on the random outputs
    chains = [create_fuzzy_chain(output) for output in chain_outputs]

    # The final result should be the last output in the chain
    result = chain_process(chains, initial_context)
    assert result == chain_outputs[-1]


@given(
    initial_context=st.one_of(st.none(), st.text(), st.integers(), st.floats(), st.booleans()),
    malformed_chain=st.one_of(st.none(), st.text(), st.integers(), st.floats(), st.booleans()),
)
def test_fuzzy_invalid_chain_input(initial_context, malformed_chain):
    """Test process with invalid chain inputs to ensure it handles errors gracefully."""

    # We expect that if the chain is malformed, an exception will occur
    with pytest.raises(TypeError):
        chain_process([malformed_chain], initial_context)


@given(
    chain_outputs=st.lists(
        st.one_of(st.text(), st.integers(), st.none(), st.floats(), st.dictionaries(keys=st.text(), values=st.text())),
        min_size=0,
        max_size=5,
    ),
    initial_context=st.one_of(st.none(), st.text(), st.integers(), st.floats(), st.booleans()),
)
def test_fuzzy_complex_chain_behavior(chain_outputs, initial_context):
    """Test process with random complex outputs to stress the system."""

    def create_fuzzy_chain(output):
        def fuzzy_chain(handler, ctx):
            handler(output)

        return fuzzy_chain

    chains = [create_fuzzy_chain(output) for output in chain_outputs]

    if chains:
        # The last output should be the result
        result = chain_process(chains, initial_context)
        assert result == chain_outputs[-1]
    else:
        # If no chains, should return initial context
        result = chain_process(chains, initial_context)
        assert result == initial_context


@given(
    invalid_chains=st.lists(
        st.one_of(st.none(), st.text(), st.integers(), st.floats(), st.dictionaries(keys=st.text(), values=st.text())),
        min_size=1,
    )
)
def test_fuzzy_invalid_chains(invalid_chains):
    """Fuzz test with invalid chain types to ensure it raises appropriate errors."""
    with pytest.raises(TypeError):
        chain_process(invalid_chains, None)
