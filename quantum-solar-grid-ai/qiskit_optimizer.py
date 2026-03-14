from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

def optimize_decision(energy_data):
    """
    Uses a 2-qubit quantum circuit to simulate a decision for energy management.

    Decision mapping:
    00 = use solar
    01 = store energy
    10 = sell energy
    11 = buy from grid

    Args:
        energy_data (dict): Dictionary containing energy simulation data (not used in this simple demo).

    Returns:
        dict: A dictionary with decision_code and decision_text.
    """
    # Create a 2-qubit quantum circuit
    qc = QuantumCircuit(2, 2)

    # Initialize qubits in superposition with Hadamard gates
    qc.h(0)
    qc.h(1)

    # Measure the qubits
    qc.measure([0, 1], [0, 1])

    # Use Aer simulator
    simulator = AerSimulator()
    compiled_circuit = transpile(qc, simulator)
    job = simulator.run(compiled_circuit, shots=1)
    result = job.result()
    counts = result.get_counts(qc)

    # Get the measured outcome (only one shot, so one result)
    decision_code = list(counts.keys())[0]

    # Build a list of candidate decisions based on energy conditions.
    solar = energy_data.get('solar_generation', 0)
    consumption = energy_data.get('consumption', 0)
    battery = energy_data.get('battery_level', 0)

    # Define candidate decision codes based on current data
    candidates = []

    # If solar output is higher than consumption, favor storing/selling
    if solar >= consumption:
        if battery < 70:
            candidates = ["01", "00"]  # store or use solar
        else:
            candidates = ["10", "00"]  # sell or use solar
    else:
        # When consumption exceeds solar, prefer using stored power and/or buying
        if battery > 30:
            candidates = ["00", "11"]  # use battery or buy
        else:
            candidates = ["11"]  # buy from grid

    # If candidates are empty for some reason, fallback to all decisions
    if not candidates:
        candidates = ["00", "01", "10", "11"]

    # Use quantum randomness to pick one of the candidates
    index = int(decision_code, 2) % len(candidates)
    decision_code = candidates[index]

    decision_map = {
        "00": "Use Solar Energy",
        "01": "Store Energy in Battery",
        "10": "Sell Energy to Grid",
        "11": "Buy Electricity from Grid"
    }

    decision_text = decision_map.get(decision_code, "Unknown Decision")

    return {
        "decision_code": decision_code,
        "decision_text": decision_text
    }