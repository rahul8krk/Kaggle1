# Quick Start Guide - IEEE 9 Bus System Analysis

## Installation (5 minutes)

1. **Clone the repository** (if not already done):
   ```bash
   git clone https://github.com/rahul8krk/Kaggle1.git
   cd Kaggle1
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Analysis (2 minutes)

### Option 1: Complete Analysis with Plots

Run the main script to perform both steady state and transient analysis:

```bash
python ieee9_bus_system.py
```

**Output:**
- Console output with detailed results
- `steady_state_results.png` - 4 plots showing steady state analysis
- `transient_results.png` - 3 plots showing transient response

### Option 2: Examples and Tutorials

Run the examples script to see different use cases:

```bash
python examples.py
```

This demonstrates:
- Basic power flow analysis
- Custom transient analysis with different parameters
- Load variation studies
- Generator dispatch optimization

## Understanding the Results

### Steady State Analysis Output

The steady state analysis shows:

1. **Bus Voltages**: All should be within 0.95-1.05 pu (per unit)
   - Below 0.95: Under-voltage condition
   - Above 1.05: Over-voltage condition

2. **Line Loading**: Percentage of line capacity used
   - Below 100%: Safe operation
   - Above 100%: Overload condition

3. **System Losses**: Power lost in transmission
   - Typical range: 2-5% of total generation

4. **Generation vs Load**: Should balance (with losses)
   - Generation = Load + Losses

### Transient Analysis Output

The transient analysis shows:

1. **Voltage Dynamics**: How voltages change during fault
   - Fault causes voltage dip
   - System should recover after fault clears
   - Recovery time indicates system stability

2. **Generator Response**: How generators adjust output
   - Generators increase/decrease to maintain stability
   - Oscillations should dampen over time

3. **Line Loading Dynamics**: How line flows change
   - Sudden changes during fault
   - Redistribution of power flow

## Customizing the Analysis

### Change Fault Parameters

Edit the `main()` function in `ieee9_bus_system.py`:

```python
transient_results = transient_analysis(
    net, 
    duration=10.0,      # Change simulation time (seconds)
    time_step=0.01,     # Change time resolution (seconds)
    fault_time=1.0,     # Change when fault occurs (seconds)
    fault_duration=0.1, # Change fault duration (seconds)
    fault_bus=4         # Change fault location (bus number)
)
```

### Modify Network Parameters

```python
# Change load values
net.load.at[0, 'p_mw'] = 150.0  # Change Bus 5 load from 125 to 150 MW

# Change generator output
net.gen.at[0, 'p_mw'] = 180.0  # Change Gen 2 output from 163 to 180 MW

# Re-run analysis
pp.runpp(net)
```

### Study Different Scenarios

```python
# Scenario 1: High load condition
net.load['p_mw'] = net.load['p_mw'] * 1.5  # 150% load

# Scenario 2: Line outage
net.line.at[0, 'in_service'] = False  # Disconnect line 0

# Scenario 3: Generator outage
net.gen.at[0, 'in_service'] = False  # Disconnect Gen 2
```

## Common Issues and Solutions

### Issue 1: Power Flow Does Not Converge

**Symptoms:**
```
PowerFlowNotConverged: Power flow did not converge after X iterations
```

**Solutions:**
- Check if loads are too high for available generation
- Verify bus voltage specifications are reasonable
- Check line parameters are correct
- Try different algorithm: `pp.runpp(net, algorithm='bfsw')`

### Issue 2: Plots Not Displayed

**Symptoms:**
- Script runs but no plot windows appear

**Solutions:**
- Plots are saved as PNG files by default
- Check for `steady_state_results.png` and `transient_results.png`
- To view interactively, remove `matplotlib.use('Agg')` line

### Issue 3: Installation Errors

**Symptoms:**
```
ModuleNotFoundError: No module named 'pandapower'
```

**Solutions:**
- Ensure pip is up to date: `pip install --upgrade pip`
- Install dependencies: `pip install -r requirements.txt`
- Try with virtual environment:
  ```bash
  python -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate
  pip install -r requirements.txt
  ```

## Next Steps

### For Beginners
1. Run the examples script: `python examples.py`
2. Read through `README.md` for detailed documentation
3. Modify parameters in examples and observe changes

### For Advanced Users
1. Study `MATLAB_COMPARISON.md` for workflow comparison
2. Implement N-1 contingency analysis
3. Add optimization (OPF) capabilities
4. Integrate with real-time data sources

### For Researchers
1. Modify the network to study different topologies
2. Implement advanced control strategies
3. Add renewable energy sources (wind, solar)
4. Study stability margins and critical clearing times

## Additional Resources

- **Pandapower Documentation**: https://pandapower.readthedocs.io/
- **IEEE Test Systems**: https://labs.ece.uw.edu/pstca/
- **Power System Analysis Book**: Grainger & Stevenson, "Power System Analysis"

## Getting Help

- Check the `README.md` for detailed documentation
- Review code comments in `ieee9_bus_system.py`
- Consult pandapower documentation
- Open an issue on GitHub for bugs or questions

---

**Quick Commands Reference:**

```bash
# Full analysis
python ieee9_bus_system.py

# Examples
python examples.py

# Install dependencies
pip install -r requirements.txt

# Check installation
python -c "import pandapower; print(pandapower.__version__)"
```

**Happy Analyzing! ⚡**
