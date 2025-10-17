"""
IEEE 9 Bus System - Steady State and Transient Analysis using Pandapower
This script demonstrates power system analysis similar to MATLAB Simulink
"""

import pandapower as pp
import pandapower.timeseries as ts
import pandapower.control as control
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandapower.plotting import simple_plot


def create_ieee9_bus_system():
    """
    Create the IEEE 9 bus test system in pandapower.
    
    The IEEE 9-bus system (also known as the WSCC 9-bus system) is a standard
    test case used in power system analysis. It consists of:
    - 9 buses
    - 3 generators
    - 3 transformers
    - 6 transmission lines
    - 3 loads
    
    Returns:
        net: pandapower network object
    """
    # Create empty network
    net = pp.create_empty_network(name="IEEE 9 Bus System")
    
    # Create buses
    # Bus 1: Generator bus (slack)
    bus1 = pp.create_bus(net, vn_kv=16.5, name="Bus 1 - Gen 1", type="b")
    
    # Bus 2: Generator bus (PV)
    bus2 = pp.create_bus(net, vn_kv=18.0, name="Bus 2 - Gen 2", type="b")
    
    # Bus 3: Generator bus (PV)
    bus3 = pp.create_bus(net, vn_kv=13.8, name="Bus 3 - Gen 3", type="b")
    
    # Bus 4: Load bus
    bus4 = pp.create_bus(net, vn_kv=230.0, name="Bus 4", type="b")
    
    # Bus 5: Load bus
    bus5 = pp.create_bus(net, vn_kv=230.0, name="Bus 5", type="b")
    
    # Bus 6: Load bus
    bus6 = pp.create_bus(net, vn_kv=230.0, name="Bus 6", type="b")
    
    # Bus 7: Transmission bus
    bus7 = pp.create_bus(net, vn_kv=230.0, name="Bus 7", type="b")
    
    # Bus 8: Transmission bus
    bus8 = pp.create_bus(net, vn_kv=230.0, name="Bus 8", type="b")
    
    # Bus 9: Transmission bus
    bus9 = pp.create_bus(net, vn_kv=230.0, name="Bus 9", type="b")
    
    # Create external grid (slack bus) at Bus 1
    pp.create_ext_grid(net, bus=bus1, vm_pu=1.04, name="Slack Bus", va_degree=0.0)
    
    # Create generators
    # Generator at Bus 2
    pp.create_gen(net, bus=bus2, p_mw=163.0, vm_pu=1.025, name="Gen 2", 
                  controllable=True, max_p_mw=200, min_p_mw=10)
    
    # Generator at Bus 3
    pp.create_gen(net, bus=bus3, p_mw=85.0, vm_pu=1.025, name="Gen 3",
                  controllable=True, max_p_mw=150, min_p_mw=10)
    
    # Create transformers
    # Transformer 1: Bus 1 to Bus 4
    pp.create_transformer_from_parameters(
        net, hv_bus=bus4, lv_bus=bus1, sn_mva=100.0, vn_hv_kv=230.0, vn_lv_kv=16.5,
        vkr_percent=0.0, vk_percent=5.76, pfe_kw=0, i0_percent=0,
        shift_degree=0, name="Trafo 1-4"
    )
    
    # Transformer 2: Bus 2 to Bus 7
    pp.create_transformer_from_parameters(
        net, hv_bus=bus7, lv_bus=bus2, sn_mva=100.0, vn_hv_kv=230.0, vn_lv_kv=18.0,
        vkr_percent=0.0, vk_percent=6.25, pfe_kw=0, i0_percent=0,
        shift_degree=0, name="Trafo 2-7"
    )
    
    # Transformer 3: Bus 3 to Bus 9
    pp.create_transformer_from_parameters(
        net, hv_bus=bus9, lv_bus=bus3, sn_mva=100.0, vn_hv_kv=230.0, vn_lv_kv=13.8,
        vkr_percent=0.0, vk_percent=5.86, pfe_kw=0, i0_percent=0,
        shift_degree=0, name="Trafo 3-9"
    )
    
    # Create transmission lines
    # Line 4-5
    pp.create_line_from_parameters(
        net, from_bus=bus4, to_bus=bus5, length_km=1.0, r_ohm_per_km=1.0,
        x_ohm_per_km=17.0, c_nf_per_km=0, max_i_ka=10, name="Line 4-5"
    )
    
    # Line 4-6
    pp.create_line_from_parameters(
        net, from_bus=bus4, to_bus=bus6, length_km=1.0, r_ohm_per_km=1.7,
        x_ohm_per_km=20.0, c_nf_per_km=0, max_i_ka=10, name="Line 4-6"
    )
    
    # Line 5-7
    pp.create_line_from_parameters(
        net, from_bus=bus5, to_bus=bus7, length_km=1.0, r_ohm_per_km=3.2,
        x_ohm_per_km=16.1, c_nf_per_km=0, max_i_ka=10, name="Line 5-7"
    )
    
    # Line 6-9
    pp.create_line_from_parameters(
        net, from_bus=bus6, to_bus=bus9, length_km=1.0, r_ohm_per_km=3.9,
        x_ohm_per_km=17.0, c_nf_per_km=0, max_i_ka=10, name="Line 6-9"
    )
    
    # Line 7-8
    pp.create_line_from_parameters(
        net, from_bus=bus7, to_bus=bus8, length_km=1.0, r_ohm_per_km=0.85,
        x_ohm_per_km=7.2, c_nf_per_km=0, max_i_ka=10, name="Line 7-8"
    )
    
    # Line 8-9
    pp.create_line_from_parameters(
        net, from_bus=bus8, to_bus=bus9, length_km=1.0, r_ohm_per_km=1.19,
        x_ohm_per_km=10.08, c_nf_per_km=0, max_i_ka=10, name="Line 8-9"
    )
    
    # Create loads
    # Load at Bus 5
    pp.create_load(net, bus=bus5, p_mw=125.0, q_mvar=50.0, name="Load 5")
    
    # Load at Bus 6
    pp.create_load(net, bus=bus6, p_mw=90.0, q_mvar=30.0, name="Load 6")
    
    # Load at Bus 8
    pp.create_load(net, bus=bus8, p_mw=100.0, q_mvar=35.0, name="Load 8")
    
    return net


def steady_state_analysis(net):
    """
    Perform steady state analysis (power flow) on the network.
    
    This is equivalent to running a power flow analysis in MATLAB Simulink.
    It calculates the steady state operating point of the system.
    
    Args:
        net: pandapower network object
        
    Returns:
        results: dictionary containing analysis results
    """
    print("\n" + "="*70)
    print("STEADY STATE ANALYSIS - POWER FLOW")
    print("="*70)
    
    # Run power flow calculation
    pp.runpp(net, algorithm='nr', calculate_voltage_angles=True)
    
    # Extract results
    results = {
        'bus_results': net.res_bus.copy(),
        'line_results': net.res_line.copy(),
        'trafo_results': net.res_trafo.copy(),
        'gen_results': net.res_gen.copy(),
        'load_results': net.res_load.copy(),
        'ext_grid_results': net.res_ext_grid.copy()
    }
    
    # Display results
    print("\n*** Bus Voltage Results ***")
    print(net.res_bus[['vm_pu', 'va_degree', 'p_mw', 'q_mvar']])
    
    print("\n*** Generator Results ***")
    print(net.res_gen[['p_mw', 'q_mvar', 'vm_pu']])
    
    print("\n*** External Grid Results ***")
    print(net.res_ext_grid[['p_mw', 'q_mvar']])
    
    print("\n*** Line Loading Results ***")
    print(net.res_line[['p_from_mw', 'q_from_mvar', 'p_to_mw', 'q_to_mvar', 'pl_mw', 'loading_percent']])
    
    print("\n*** Transformer Loading Results ***")
    print(net.res_trafo[['p_hv_mw', 'q_hv_mvar', 'p_lv_mw', 'q_lv_mvar', 'pl_mw', 'loading_percent']])
    
    print("\n*** Load Results ***")
    print(net.res_load[['p_mw', 'q_mvar']])
    
    # Calculate total system losses
    total_line_losses = net.res_line['pl_mw'].sum()
    total_trafo_losses = net.res_trafo['pl_mw'].sum()
    total_losses = total_line_losses + total_trafo_losses
    
    print("\n*** System Losses ***")
    print(f"Line Losses: {total_line_losses:.4f} MW")
    print(f"Transformer Losses: {total_trafo_losses:.4f} MW")
    print(f"Total System Losses: {total_losses:.4f} MW")
    
    return results


def transient_analysis(net, duration=10.0, time_step=0.01, fault_time=1.0, 
                       fault_duration=0.1, fault_bus=4):
    """
    Perform transient analysis (dynamic simulation) on the network.
    
    This simulates a disturbance (fault) in the system and analyzes the dynamic response,
    similar to time-domain simulation in MATLAB Simulink.
    
    Args:
        net: pandapower network object
        duration: simulation duration in seconds
        time_step: time step for simulation in seconds
        fault_time: time when fault occurs in seconds
        fault_duration: duration of fault in seconds
        fault_bus: bus number where fault occurs
        
    Returns:
        time_series_results: dictionary with time series data
    """
    print("\n" + "="*70)
    print("TRANSIENT ANALYSIS - DYNAMIC SIMULATION")
    print("="*70)
    print(f"Simulating fault at Bus {fault_bus} at t={fault_time}s for {fault_duration}s")
    print(f"Total simulation time: {duration}s, Time step: {time_step}s")
    
    # Initialize arrays to store results
    num_steps = int(duration / time_step)
    time_array = np.linspace(0, duration, num_steps)
    
    # Arrays to store results
    bus_voltages = np.zeros((num_steps, len(net.bus)))
    bus_angles = np.zeros((num_steps, len(net.bus)))
    gen_powers = np.zeros((num_steps, len(net.gen)))
    line_loadings = np.zeros((num_steps, len(net.line)))
    
    # Store original load values
    original_loads = net.load['p_mw'].copy()
    
    # Simulate time series
    for i, t in enumerate(time_array):
        # Apply fault condition
        if fault_time <= t < fault_time + fault_duration:
            # Simulate fault by increasing load at fault bus significantly
            fault_load_idx = net.load[net.load['bus'] == fault_bus].index
            if len(fault_load_idx) > 0:
                net.load.at[fault_load_idx[0], 'p_mw'] = original_loads[fault_load_idx[0]] * 3.0
        else:
            # Normal operation - restore original loads
            net.load['p_mw'] = original_loads.copy()
        
        # Add small load variations to simulate dynamics
        load_variation = 1.0 + 0.05 * np.sin(2 * np.pi * 0.5 * t)  # 0.5 Hz oscillation
        net.load['p_mw'] = original_loads * load_variation
        
        try:
            # Run power flow for this time step
            pp.runpp(net, algorithm='nr', calculate_voltage_angles=True)
            
            # Store results
            bus_voltages[i, :] = net.res_bus['vm_pu'].values
            bus_angles[i, :] = net.res_bus['va_degree'].values
            gen_powers[i, :] = net.res_gen['p_mw'].values
            line_loadings[i, :] = net.res_line['loading_percent'].values
            
        except Exception as e:
            print(f"Warning: Power flow did not converge at t={t:.2f}s: {e}")
            # Use previous values if convergence fails
            if i > 0:
                bus_voltages[i, :] = bus_voltages[i-1, :]
                bus_angles[i, :] = bus_angles[i-1, :]
                gen_powers[i, :] = gen_powers[i-1, :]
                line_loadings[i, :] = line_loadings[i-1, :]
    
    # Restore original loads
    net.load['p_mw'] = original_loads
    
    # Prepare results
    time_series_results = {
        'time': time_array,
        'bus_voltages': bus_voltages,
        'bus_angles': bus_angles,
        'gen_powers': gen_powers,
        'line_loadings': line_loadings,
        'fault_time': fault_time,
        'fault_duration': fault_duration,
        'fault_bus': fault_bus
    }
    
    print("\nTransient simulation completed successfully!")
    
    return time_series_results


def plot_steady_state_results(net, results):
    """
    Plot steady state analysis results.
    
    Args:
        net: pandapower network object
        results: results dictionary from steady_state_analysis
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('IEEE 9 Bus System - Steady State Analysis Results', fontsize=16)
    
    # Plot 1: Bus Voltages
    ax1 = axes[0, 0]
    bus_numbers = range(len(net.bus))
    voltages = results['bus_results']['vm_pu'].values
    ax1.bar(bus_numbers, voltages, color='steelblue', alpha=0.7)
    ax1.axhline(y=1.0, color='r', linestyle='--', label='Nominal (1.0 pu)')
    ax1.axhline(y=0.95, color='orange', linestyle='--', label='Lower Limit (0.95 pu)')
    ax1.axhline(y=1.05, color='orange', linestyle='--', label='Upper Limit (1.05 pu)')
    ax1.set_xlabel('Bus Number')
    ax1.set_ylabel('Voltage (pu)')
    ax1.set_title('Bus Voltage Profile')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Bus Voltage Angles
    ax2 = axes[0, 1]
    angles = results['bus_results']['va_degree'].values
    ax2.bar(bus_numbers, angles, color='green', alpha=0.7)
    ax2.set_xlabel('Bus Number')
    ax2.set_ylabel('Voltage Angle (degrees)')
    ax2.set_title('Bus Voltage Angles')
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Line Loadings
    ax3 = axes[1, 0]
    line_numbers = range(len(net.line))
    loadings = results['line_results']['loading_percent'].values
    ax3.bar(line_numbers, loadings, color='coral', alpha=0.7)
    ax3.axhline(y=100, color='r', linestyle='--', label='100% Loading')
    ax3.set_xlabel('Line Number')
    ax3.set_ylabel('Loading (%)')
    ax3.set_title('Transmission Line Loading')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Power Generation and Load
    ax4 = axes[1, 1]
    
    # Calculate total generation
    total_gen_p = results['ext_grid_results']['p_mw'].sum() + results['gen_results']['p_mw'].sum()
    total_gen_q = results['ext_grid_results']['q_mvar'].sum() + results['gen_results']['q_mvar'].sum()
    
    # Total load
    total_load_p = results['load_results']['p_mw'].sum()
    total_load_q = results['load_results']['q_mvar'].sum()
    
    # Total losses
    total_losses = results['line_results']['pl_mw'].sum() + results['trafo_results']['pl_mw'].sum()
    
    categories = ['Active Power\n(MW)', 'Reactive Power\n(MVAr)']
    generation = [total_gen_p, total_gen_q]
    load = [total_load_p, total_load_q]
    
    x = np.arange(len(categories))
    width = 0.35
    
    ax4.bar(x - width/2, generation, width, label='Generation', color='lightgreen', alpha=0.7)
    ax4.bar(x + width/2, load, width, label='Load', color='lightcoral', alpha=0.7)
    ax4.set_ylabel('Power (MW/MVAr)')
    ax4.set_title('System Generation vs Load')
    ax4.set_xticks(x)
    ax4.set_xticklabels(categories)
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    # Add text for losses
    ax4.text(0.5, 0.95, f'Total Losses: {total_losses:.2f} MW', 
             transform=ax4.transAxes, ha='center', va='top',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig('/home/runner/work/Kaggle1/Kaggle1/steady_state_results.png', dpi=300, bbox_inches='tight')
    print("\nSteady state results plot saved as 'steady_state_results.png'")
    plt.show()


def plot_transient_results(net, time_series_results):
    """
    Plot transient analysis results.
    
    Args:
        net: pandapower network object
        time_series_results: results dictionary from transient_analysis
    """
    time = time_series_results['time']
    fault_time = time_series_results['fault_time']
    fault_duration = time_series_results['fault_duration']
    
    fig, axes = plt.subplots(3, 1, figsize=(14, 12))
    fig.suptitle('IEEE 9 Bus System - Transient Analysis Results', fontsize=16)
    
    # Plot 1: Bus Voltages Over Time
    ax1 = axes[0]
    for i in range(len(net.bus)):
        ax1.plot(time, time_series_results['bus_voltages'][:, i], 
                label=f'Bus {i}', linewidth=1.5)
    ax1.axvline(x=fault_time, color='r', linestyle='--', label='Fault Start', linewidth=2)
    ax1.axvline(x=fault_time + fault_duration, color='g', linestyle='--', 
                label='Fault Clear', linewidth=2)
    ax1.axhline(y=1.0, color='gray', linestyle=':', alpha=0.5)
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Voltage (pu)')
    ax1.set_title('Bus Voltage Dynamics')
    ax1.legend(loc='upper right', ncol=3, fontsize=8)
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim([0.85, 1.15])
    
    # Add shaded region for fault period
    ax1.axvspan(fault_time, fault_time + fault_duration, alpha=0.2, color='red')
    
    # Plot 2: Generator Power Output Over Time
    ax2 = axes[1]
    for i in range(len(net.gen)):
        ax2.plot(time, time_series_results['gen_powers'][:, i], 
                label=f'Gen {i+2}', linewidth=2)
    ax2.axvline(x=fault_time, color='r', linestyle='--', linewidth=2)
    ax2.axvline(x=fault_time + fault_duration, color='g', linestyle='--', linewidth=2)
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Active Power (MW)')
    ax2.set_title('Generator Power Output Dynamics')
    ax2.legend(loc='best')
    ax2.grid(True, alpha=0.3)
    ax2.axvspan(fault_time, fault_time + fault_duration, alpha=0.2, color='red')
    
    # Plot 3: Line Loading Over Time (selected lines)
    ax3 = axes[2]
    # Plot first 3 lines for clarity
    for i in range(min(3, len(net.line))):
        ax3.plot(time, time_series_results['line_loadings'][:, i], 
                label=f'Line {i}', linewidth=2)
    ax3.axvline(x=fault_time, color='r', linestyle='--', label='Fault Start', linewidth=2)
    ax3.axvline(x=fault_time + fault_duration, color='g', linestyle='--', 
                label='Fault Clear', linewidth=2)
    ax3.axhline(y=100, color='orange', linestyle='--', alpha=0.5, label='100% Loading')
    ax3.set_xlabel('Time (s)')
    ax3.set_ylabel('Loading (%)')
    ax3.set_title('Transmission Line Loading Dynamics')
    ax3.legend(loc='best')
    ax3.grid(True, alpha=0.3)
    ax3.axvspan(fault_time, fault_time + fault_duration, alpha=0.2, color='red')
    
    plt.tight_layout()
    plt.savefig('/home/runner/work/Kaggle1/Kaggle1/transient_results.png', dpi=300, bbox_inches='tight')
    print("\nTransient analysis results plot saved as 'transient_results.png'")
    plt.show()


def plot_network_topology(net):
    """
    Plot the network topology diagram.
    
    Args:
        net: pandapower network object
    """
    try:
        plt.figure(figsize=(12, 8))
        simple_plot(net, plot_loads=True, plot_gens=True, plot_line_switches=True,
                   load_size=1.0, gen_size=1.0, trafo_size=1.0, bus_size=1.0)
        plt.title('IEEE 9 Bus System Topology', fontsize=16)
        plt.savefig('/home/runner/work/Kaggle1/Kaggle1/network_topology.png', dpi=300, bbox_inches='tight')
        print("\nNetwork topology plot saved as 'network_topology.png'")
        plt.show()
    except Exception as e:
        print(f"\nNote: Network topology plotting requires additional setup: {e}")
        print("Network structure can be examined through the data tables above.")


def main():
    """
    Main function to run the complete analysis.
    """
    print("IEEE 9 Bus System Analysis using Pandapower")
    print("Similar to MATLAB Simulink Power System Analysis")
    print("="*70)
    
    # Create the IEEE 9 bus system
    print("\nCreating IEEE 9 Bus System model...")
    net = create_ieee9_bus_system()
    print(f"System created successfully!")
    print(f"- Total buses: {len(net.bus)}")
    print(f"- Total generators: {len(net.gen) + len(net.ext_grid)}")
    print(f"- Total lines: {len(net.line)}")
    print(f"- Total transformers: {len(net.trafo)}")
    print(f"- Total loads: {len(net.load)}")
    
    # Perform steady state analysis
    steady_state_results = steady_state_analysis(net)
    
    # Plot steady state results
    plot_steady_state_results(net, steady_state_results)
    
    # Perform transient analysis
    transient_results = transient_analysis(
        net, 
        duration=10.0,      # 10 second simulation
        time_step=0.01,     # 10 ms time step
        fault_time=1.0,     # Fault at 1 second
        fault_duration=0.1, # Fault duration 100 ms
        fault_bus=4         # Fault at bus 4
    )
    
    # Plot transient results
    plot_transient_results(net, transient_results)
    
    # Try to plot network topology
    plot_network_topology(net)
    
    print("\n" + "="*70)
    print("Analysis complete! Results have been saved as PNG files.")
    print("="*70)
    
    return net, steady_state_results, transient_results


if __name__ == "__main__":
    # Run the analysis
    network, ss_results, ts_results = main()
