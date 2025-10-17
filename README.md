# IEEE 9 Bus System Analysis using Python

This repository contains a Python implementation for **steady state** and **transient analysis** of the IEEE 9 Bus System using **pandapower**, providing similar functionality to MATLAB Simulink power system analysis tools.

## Overview

The IEEE 9-bus system (also known as the WSCC 9-bus system) is a standard test case used in power system analysis. This implementation provides:

- **Steady State Analysis**: Power flow calculations to determine the operating point
- **Transient Analysis**: Dynamic simulation to analyze system response to disturbances
- **Visualization**: Comprehensive plots of voltage profiles, power flows, and dynamic behavior

## System Description

The IEEE 9 Bus System consists of:
- **9 buses** (3 generator buses, 3 load buses, 3 transmission buses)
- **3 generators** (including slack bus)
- **3 transformers** connecting generators to the transmission network
- **6 transmission lines**
- **3 loads** (at buses 5, 6, and 8)

## Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Install Dependencies

```bash
pip install -r requirements.txt
```

The required packages are:
- `pandapower` - Power system analysis library
- `matplotlib` - Plotting and visualization
- `numpy` - Numerical computations
- `pandas` - Data manipulation
- `scipy` - Scientific computing

## Usage

### Basic Usage

Run the complete analysis with default parameters:

```bash
python ieee9_bus_system.py
```

This will:
1. Create the IEEE 9 bus system model
2. Perform steady state power flow analysis
3. Perform transient analysis with a simulated fault
4. Generate visualization plots saved as PNG files

### Output Files

The script generates the following output files:
- `steady_state_results.png` - Steady state analysis visualization
- `transient_results.png` - Transient analysis visualization
- `network_topology.png` - Network topology diagram (if supported)

### Customizing the Analysis

You can modify the analysis parameters by editing the `main()` function in `ieee9_bus_system.py`:

```python
# Customize transient analysis parameters
transient_results = transient_analysis(
    net, 
    duration=10.0,      # Total simulation time (seconds)
    time_step=0.01,     # Time step for simulation (seconds)
    fault_time=1.0,     # Time when fault occurs (seconds)
    fault_duration=0.1, # Duration of fault (seconds)
    fault_bus=4         # Bus number where fault occurs
)
```

## Features

### 1. Steady State Analysis

The steady state analysis performs power flow calculations to determine:
- Bus voltages (magnitude and angle)
- Active and reactive power flows in lines and transformers
- Generator outputs
- System losses
- Line and transformer loading percentages

**Example Output:**
```
*** Bus Voltage Results ***
   vm_pu  va_degree      p_mw    q_mvar
0  1.040      0.000    71.644    27.046
1  1.025      4.665   163.000    6.654
...

*** System Losses ***
Line Losses: 5.8234 MW
Transformer Losses: 0.9123 MW
Total System Losses: 6.7357 MW
```

### 2. Transient Analysis

The transient analysis simulates the dynamic response of the system to disturbances:
- Simulates a fault at a specified bus
- Tracks voltage dynamics during and after the fault
- Monitors generator power output changes
- Analyzes line loading variations over time

The simulation captures the system's behavior similar to time-domain analysis in MATLAB Simulink.

### 3. Visualization

#### Steady State Results
- **Bus Voltage Profile**: Voltage magnitudes at all buses with acceptable limits
- **Voltage Angles**: Phase angles at all buses
- **Line Loading**: Percentage loading of transmission lines
- **Generation vs Load**: Comparison of total generation and load

#### Transient Results
- **Voltage Dynamics**: Bus voltages over time showing fault response
- **Generator Dynamics**: Active power output variations
- **Line Loading Dynamics**: Transmission line loading changes over time

All plots include fault timing indicators and reference lines for easy interpretation.

## Comparison with MATLAB Simulink

This Python implementation provides equivalent functionality to MATLAB Simulink Simscape Power Systems:

| Feature | MATLAB Simulink | This Python Implementation |
|---------|----------------|---------------------------|
| Power Flow Analysis | ✓ | ✓ (Newton-Raphson method) |
| Network Modeling | ✓ | ✓ (Buses, lines, transformers, loads, generators) |
| Transient Simulation | ✓ | ✓ (Time-domain simulation) |
| Fault Analysis | ✓ | ✓ (Configurable fault location and duration) |
| Visualization | ✓ | ✓ (Comprehensive plots) |
| Cost | Commercial License | Free and Open Source |

## Advanced Usage

### Using as a Library

You can import and use the functions in your own scripts:

```python
from ieee9_bus_system import create_ieee9_bus_system, steady_state_analysis, transient_analysis

# Create the network
net = create_ieee9_bus_system()

# Run steady state analysis
ss_results = steady_state_analysis(net)

# Access specific results
bus_voltages = ss_results['bus_results']['vm_pu']
line_loading = ss_results['line_results']['loading_percent']

# Run custom transient analysis
ts_results = transient_analysis(net, duration=5.0, fault_bus=5)
```

### Modifying the Network

You can modify the network parameters to study different scenarios:

```python
# Modify load values
net.load.at[0, 'p_mw'] = 150.0  # Increase load at bus 5

# Modify generator output
net.gen.at[0, 'p_mw'] = 180.0  # Change generator 2 output

# Run analysis with modified network
pp.runpp(net)
```

## Theory and Background

### Steady State Analysis (Power Flow)

The power flow analysis solves the following equations for each bus:

```
P_i = V_i * Σ(V_j * Y_ij * cos(θ_i - θ_j - α_ij))
Q_i = V_i * Σ(V_j * Y_ij * sin(θ_i - θ_j - α_ij))
```

Where:
- P_i, Q_i: Active and reactive power injection at bus i
- V_i, θ_i: Voltage magnitude and angle at bus i
- Y_ij, α_ij: Admittance magnitude and angle between buses i and j

The implementation uses the Newton-Raphson method for fast convergence.

### Transient Analysis

The transient analysis simulates the system's response to disturbances by:
1. Introducing a fault (load increase) at a specified bus
2. Solving power flow at each time step
3. Tracking voltage, power, and loading dynamics
4. Analyzing system stability and recovery

This approach is similar to quasi-steady-state simulation, appropriate for studying electromechanical dynamics.

## References

1. Sauer, P. W., & Pai, M. A. (1998). *Power System Dynamics and Stability*. Prentice Hall.
2. Kundur, P. (1994). *Power System Stability and Control*. McGraw-Hill.
3. Pandapower Documentation: https://pandapower.readthedocs.io/

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License

This project is provided as-is for educational and research purposes.

## Support

For questions or issues, please open an issue in the repository.

---

**Note**: This implementation provides a foundation for power system analysis. For production systems or detailed studies, consider consulting with power system engineers and validating results with commercial software.
