import matplotlib.pyplot as plt
import seaborn as sns

def plot_dual_axis_trends(future_data):
    """
    Plots predicted deaths trends with two y-axes: 
    one for nationwide deaths, another for state-level deaths.
    """
    # Ensure Year column is sorted
    future_data = future_data.sort_values(by=['Year'])

    # Standardize state names for filtering
    future_data['State'] = future_data['State'].str.strip().str.lower()

    # Separate nationwide and state-level data
    us_data = future_data[future_data['State'] == "united states"]
    state_data = future_data[future_data['State'] != "united states"]

    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Plot nationwide deaths on primary y-axis
    ax1.plot(us_data['Year'], us_data['Predicted Deaths'], color='red', marker='o', linewidth=2, label="United States")
    ax1.set_ylabel("Nationwide Predicted Deaths", color='red')
    ax1.tick_params(axis='y', labelcolor='red')

    # Create secondary y-axis for states
    ax2 = ax1.twinx()

    # Plot state-level deaths
    for state in state_data['State'].unique():
        state_subset = state_data[state_data['State'] == state]
        ax2.plot(state_subset['Year'], state_subset['Predicted Deaths'], linestyle='dashed', alpha=0.7, label=state.title())

    ax2.set_ylabel("State-Level Predicted Deaths", color='blue')
    ax2.tick_params(axis='y', labelcolor='blue')

    # Titles and legend
    ax1.set_xlabel("Year")
    plt.title("Predicted Death Trends: Nationwide vs. State-Level (Next 10 Years)")
    fig.legend(loc="upper left", bbox_to_anchor=(1,1))

    plt.show()
    
def plot_log_scale_trends(future_data):
    """
    Plots the trend of predicted deaths using a logarithmic scale to balance nationwide vs. state values.
    """
    # Ensure Year column is sorted
    future_data = future_data.sort_values(by=['Year'])

    # Standardize state names
    future_data['State'] = future_data['State'].str.strip().str.lower()

    # Create the plot
    plt.figure(figsize=(12, 6))

    # Plot each state's data
    for state in future_data['State'].unique():
        state_data = future_data[future_data['State'] == state]
        plt.plot(state_data['Year'], state_data['Predicted Deaths'], marker='o', linestyle='dashed', label=state.title())

    # Use log scale for y-axis
    plt.yscale("log")
    plt.xlabel("Year")
    plt.ylabel("Predicted Death Count (Log Scale)")
    plt.title("Predicted Death Trends (Logarithmic Scale)")
    plt.legend(title="State", loc="upper left", bbox_to_anchor=(1,1))
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)

    plt.show()

