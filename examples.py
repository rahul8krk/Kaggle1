"""
Example: Quick Start Guide for IEEE 9 Bus System Analysis

This script demonstrates basic usage of the IEEE 9 bus system analysis.
"""

from ieee9_bus_system import (
    create_ieee9_bus_system, 
    steady_state_analysis, 
    transient_analysis,
    plot_steady_state_results,
    plot_transient_results
)
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend


def example_1_basic_power_flow():
    """
    Example 1: Basic power flow analysis (steady state)
    This is the simplest use case - just run power flow and see results.
    """
    print("\n" + "="*70)
    print("EXAMPLE 1: Basic Power Flow Analysis")
    print("="*70)
    
    # Create the network
    net = create_ieee9_bus_system()
    
    # Run steady state analysis
    results = steady_state_analysis(net)
    
    # Access specific results
    print("\nKey Results:")
    print(f"Minimum Bus Voltage: {results['bus_results']['vm_pu'].min():.4f} pu")
    print(f"Maximum Bus Voltage: {results['bus_results']['vm_pu'].max():.4f} pu")
    print(f"Total Generation: {results['ext_grid_results']['p_mw'].sum() + results['gen_results']['p_mw'].sum():.2f} MW")
    print(f"Total Load: {results['load_results']['p_mw'].sum():.2f} MW")
    
    return net, results


def example_2_custom_transient_analysis():
    """
    Example 2: Transient analysis with custom parameters
    Shows how to modify simulation parameters.
    """
    print("\n" + "="*70)
    print("EXAMPLE 2: Custom Transient Analysis")
    print("="*70)
    
    # Create the network
    net = create_ieee9_bus_system()
    
    # Run transient analysis with custom parameters
    # Simulate a fault at bus 5 for 150ms starting at 2 seconds
    transient_results = transient_analysis(
        net,
        duration=8.0,         # 8 second simulation
        time_step=0.02,       # 20ms time step (faster simulation)
        fault_time=2.0,       # Fault at 2 seconds
        fault_duration=0.15,  # 150ms fault duration
        fault_bus=5           # Fault at bus 5 (load bus)
    )
    
    print("\nTransient analysis completed!")
    print(f"Simulated {len(transient_results['time'])} time steps")
    
    return net, transient_results


def example_3_load_variation_study():
    """
    Example 3: Study the effect of load changes
    Shows how to modify network parameters and re-run analysis.
    """
    print("\n" + "="*70)
    print("EXAMPLE 3: Load Variation Study")
    print("="*70)
    
    import pandapower as pp
    
    # Create the network
    net = create_ieee9_bus_system()
    
    # Store original load
    original_load = net.load.at[0, 'p_mw']
    
    # Test different load levels
    load_levels = [0.8, 1.0, 1.2, 1.5]  # 80%, 100%, 120%, 150%
    
    print("\nLoad Variation Study Results:")
    print("-" * 50)
    print(f"{'Load Level':<15} {'Min Voltage (pu)':<20} {'Max Voltage (pu)'}")
    print("-" * 50)
    
    for level in load_levels:
        # Modify all loads
        net.load['p_mw'] = net.load['p_mw'] * level / (net.load['p_mw'].sum() / (125 + 90 + 100))
        
        # Run power flow
        pp.runpp(net, numba=False)
        
        # Get results
        min_voltage = net.res_bus['vm_pu'].min()
        max_voltage = net.res_bus['vm_pu'].max()
        
        print(f"{level*100:>6.0f}%         {min_voltage:>8.4f}           {max_voltage:>8.4f}")
    
    return net


def example_4_generator_dispatch():
    """
    Example 4: Study generator dispatch changes
    Shows how to modify generator outputs.
    """
    print("\n" + "="*70)
    print("EXAMPLE 4: Generator Dispatch Study")
    print("="*70)
    
    import pandapower as pp
    
    # Create the network
    net = create_ieee9_bus_system()
    
    # Increase generator 2 output
    net.gen.at[0, 'p_mw'] = 180.0  # Increase from 163 MW to 180 MW
    net.gen.at[1, 'p_mw'] = 70.0   # Decrease from 85 MW to 70 MW
    
    print("\nModified Generator Dispatch:")
    print(f"Generator 2: 180.0 MW")
    print(f"Generator 3: 70.0 MW")
    
    # Run power flow
    pp.runpp(net, numba=False)
    
    print("\nResults after dispatch change:")
    print(f"Generator 2 Output: {net.res_gen.at[0, 'p_mw']:.2f} MW, {net.res_gen.at[0, 'q_mvar']:.2f} MVAr")
    print(f"Generator 3 Output: {net.res_gen.at[1, 'p_mw']:.2f} MW, {net.res_gen.at[1, 'q_mvar']:.2f} MVAr")
    print(f"Slack Bus Power: {net.res_ext_grid.at[0, 'p_mw']:.2f} MW, {net.res_ext_grid.at[0, 'q_mvar']:.2f} MVAr")
    
    return net


def main():
    """Run all examples"""
    print("\n" + "="*70)
    print("IEEE 9 BUS SYSTEM - USAGE EXAMPLES")
    print("="*70)
    
    # Run examples
    net1, results1 = example_1_basic_power_flow()
    
    net2, transient_results = example_2_custom_transient_analysis()
    
    net3 = example_3_load_variation_study()
    
    net4 = example_4_generator_dispatch()
    
    print("\n" + "="*70)
    print("All examples completed successfully!")
    print("="*70)
    print("\nTips:")
    print("1. Run 'python ieee9_bus_system.py' for full analysis with plots")
    print("2. Import functions from ieee9_bus_system.py for custom analysis")
    print("3. Modify network parameters (loads, generators) to study different scenarios")
    print("4. Use pandapower's runpp() function to run power flow after modifications")


if __name__ == "__main__":
    main()
