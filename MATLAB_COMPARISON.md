# IEEE 9 Bus System Analysis - MATLAB Simulink vs Python/Pandapower

## Introduction

This document explains how the Python implementation using pandapower provides equivalent functionality to MATLAB Simulink for power system analysis.

## Key Comparisons

### 1. Network Modeling

#### MATLAB Simulink
In MATLAB Simulink, you would:
- Use Simscape Power Systems (formerly SimPowerSystems)
- Drag and drop blocks (buses, generators, loads, lines, transformers)
- Connect blocks graphically
- Set parameters for each component through dialog boxes

#### Python/Pandapower
In Python with pandapower:
```python
import pandapower as pp

# Create network
net = pp.create_empty_network()

# Create buses
bus1 = pp.create_bus(net, vn_kv=230.0)

# Create generators
pp.create_gen(net, bus=bus1, p_mw=100.0, vm_pu=1.02)

# Create lines
pp.create_line(net, from_bus=bus1, to_bus=bus2, length_km=10, ...)
```

**Advantage**: Programmatic approach allows for:
- Easy parameter sweeps and batch simulations
- Version control of network models
- Automated testing and validation
- Integration with optimization algorithms

### 2. Steady State Analysis (Power Flow)

#### MATLAB Simulink
- Use "Load Flow" or "Power Flow" block
- Or use `runpf` function from command line
- Configure Newton-Raphson or other solver methods
- Results displayed in scopes or saved to workspace

#### Python/Pandapower
```python
import pandapower as pp

# Run power flow
pp.runpp(net, algorithm='nr')

# Access results
bus_voltages = net.res_bus['vm_pu']
line_loading = net.res_line['loading_percent']
```

**Output Comparison**:

| Metric | MATLAB Simulink | Pandapower |
|--------|----------------|-----------|
| Bus Voltages | ✓ | ✓ |
| Voltage Angles | ✓ | ✓ |
| Line Flows | ✓ | ✓ |
| Generator Output | ✓ | ✓ |
| System Losses | ✓ | ✓ |
| Convergence Info | ✓ | ✓ |

### 3. Transient Analysis (Time Domain Simulation)

#### MATLAB Simulink
In Simulink, transient analysis involves:
- Setting simulation time and solver options
- Using continuous-time solvers (ode45, ode23tb, etc.)
- Adding fault blocks and configuring timing
- Running simulation and viewing results in scopes
- Example:
  ```matlab
  % Set simulation parameters
  set_param('model', 'StopTime', '10.0');
  set_param('model', 'Solver', 'ode45');
  
  % Run simulation
  sim('model');
  ```

#### Python/Pandapower
```python
# Configure transient simulation
duration = 10.0      # seconds
time_step = 0.01     # 10ms

# Simulate with fault
for t in time_array:
    if fault_time <= t < fault_time + fault_duration:
        # Apply fault condition
        net.load.at[fault_idx, 'p_mw'] *= 3.0
    
    # Run power flow for this time step
    pp.runpp(net)
    
    # Store results
    voltages[i] = net.res_bus['vm_pu'].values
```

**Capabilities**:

| Feature | MATLAB Simulink | Pandapower |
|---------|----------------|-----------|
| Fault Simulation | ✓ | ✓ |
| Load Variations | ✓ | ✓ |
| Generator Dynamics | ✓ (with detailed models) | ✓ (simplified) |
| Protection Systems | ✓ | Limited |
| Custom Control | ✓ | ✓ |

### 4. Visualization

#### MATLAB Simulink
- Use Scope blocks during simulation
- Plot from workspace after simulation:
  ```matlab
  plot(tout, Vbus1);
  xlabel('Time (s)');
  ylabel('Voltage (pu)');
  ```
- Can create custom GUIs with GUIDE or App Designer

#### Python/Pandapower
```python
import matplotlib.pyplot as plt

# Plot voltage profile
plt.plot(time, voltages)
plt.xlabel('Time (s)')
plt.ylabel('Voltage (pu)')
plt.show()
```

**Advantages**:
- Matplotlib provides publication-quality figures
- Easy to customize with Python
- Can create interactive plots with plotly
- Export to various formats (PNG, PDF, SVG)

## Workflow Comparison

### MATLAB Simulink Workflow

1. Open Simulink
2. Create new model
3. Add blocks from library browser
4. Configure block parameters
5. Connect blocks
6. Set simulation parameters
7. Run simulation
8. View results in scopes
9. Export data to workspace
10. Post-process in MATLAB

### Python/Pandapower Workflow

1. Write Python script
2. Define network programmatically
3. Run analysis functions
4. Results automatically available
5. Create custom visualizations
6. Save results and plots

```python
# Complete workflow in one script
from ieee9_bus_system import create_ieee9_bus_system, steady_state_analysis

net = create_ieee9_bus_system()
results = steady_state_analysis(net)
# Results immediately available for further analysis
```

## Practical Examples

### Example 1: N-1 Contingency Analysis

#### MATLAB Simulink Approach
```matlab
% Manually configure each contingency
% Run simulation for each case
% Collect results
for i = 1:num_lines
    % Disable line i
    % Run power flow
    % Store results
end
```

#### Python/Pandapower Approach
```python
import pandapower as pp

contingency_results = []
for line_idx in range(len(net.line)):
    # Disable line
    net.line.at[line_idx, 'in_service'] = False
    
    # Run power flow
    pp.runpp(net)
    
    # Store results
    contingency_results.append({
        'line': line_idx,
        'min_voltage': net.res_bus['vm_pu'].min(),
        'overloads': (net.res_line['loading_percent'] > 100).sum()
    })
    
    # Re-enable line
    net.line.at[line_idx, 'in_service'] = True

# Analyze results
import pandas as pd
df = pd.DataFrame(contingency_results)
print(df)
```

### Example 2: Optimal Power Flow

While both platforms can do optimization:

#### Python/Pandapower + Optimization
```python
from scipy.optimize import minimize

def objective(gen_powers):
    # Set generator outputs
    net.gen['p_mw'] = gen_powers
    
    # Run power flow
    pp.runpp(net)
    
    # Calculate cost
    cost = sum(gen_powers**2)  # Simplified cost function
    return cost

# Optimize
result = minimize(objective, initial_gen_powers, 
                 constraints=constraints,
                 bounds=gen_bounds)
```

## Performance Comparison

| Aspect | MATLAB Simulink | Python/Pandapower |
|--------|----------------|-------------------|
| Setup Time | Longer (GUI-based) | Shorter (code-based) |
| Large Networks | Good | Excellent |
| Batch Simulations | Moderate | Excellent |
| Automation | Moderate | Excellent |
| Learning Curve | Moderate | Moderate |
| Cost | $$$ (License) | Free (Open Source) |

## When to Use Each Platform

### Use MATLAB Simulink When:
- You need detailed dynamic models (synchronous machines, controls)
- Protection system modeling is required
- You prefer graphical modeling
- You already have MATLAB license
- Working with team familiar with MATLAB

### Use Python/Pandapower When:
- Large-scale studies with many scenarios
- Need for automation and scripting
- Integration with machine learning/optimization
- Open-source requirement
- Cost is a factor
- Need for version control of models

## Conclusion

Both platforms are capable of power system analysis:

- **MATLAB Simulink**: Better for detailed, graphical modeling with extensive component libraries
- **Python/Pandapower**: Better for automated, large-scale studies with programmatic control

The Python implementation in this repository demonstrates that pandapower can effectively replicate the core functionality of MATLAB Simulink for power flow and basic transient analysis, with advantages in automation, scalability, and cost.

## References

1. MATLAB Simscape Power Systems Documentation
2. Pandapower Documentation: https://pandapower.readthedocs.io/
3. IEEE 9-Bus Test System: Anderson, P. M., & Fouad, A. A. (2003). Power system control and stability.
