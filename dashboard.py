import streamlit as st
import numpy as np
import scipy.stats as stats
import plotly.graph_objects as go
import matplotlib.pyplot as plt

# Function to calculate confidence intervals


def calculate_confidence_interval(data, confidence_level=0.95):
    mean = np.mean(data)
    std_err = np.std(data, ddof=1) / np.sqrt(len(data))  # Standard error
    confidence_interval = stats.t.interval(
        confidence_level, len(data) - 1, loc=mean, scale=std_err)
    return mean, confidence_interval


# Streamlit user input
st.title("Confidence Interval and Sample Size Analysis")
confidence_level = st.slider(
    "Confidence Level",
    min_value=90,
    max_value=99,
    value=95) / 100
max_sample_size = st.slider(
    "Max Sample Size",
    min_value=10,
    max_value=1000,
    value=500)

# Generate data from a normal distribution (mean=0, std=1)
np.random.seed(42)
full_data = np.random.normal(loc=0, scale=1, size=max_sample_size)

# A. Sample Size vs Mean and Confidence Interval

sample_sizes = np.arange(10, max_sample_size + 1, 10)
means = []
lower_bounds = []
upper_bounds = []

for size in sample_sizes:
    data = np.random.choice(full_data, size=size, replace=False)
    mean, (lower, upper) = calculate_confidence_interval(
        data, confidence_level)
    means.append(mean)
    lower_bounds.append(lower)
    upper_bounds.append(upper)

# Plotting the results for sample size vs mean and confidence interval
fig_A = go.Figure()

# Plot the means
fig_A.add_trace(go.Scatter(
    x=sample_sizes,
    y=means,
    mode='lines+markers',
    name='Mean',
    line=dict(color='blue')
))

# Plot the confidence intervals as shaded areas
fig_A.add_trace(go.Scatter(
    x=np.concatenate([sample_sizes, sample_sizes[::-1]]),
    y=np.concatenate([upper_bounds, lower_bounds[::-1]]),
    fill='toself',
    fillcolor='rgba(0, 100, 80, 0.2)',
    line=dict(color='rgba(255, 255, 255, 0)'),
    name=f'{int(confidence_level * 100)}% Confidence Interval'
))

fig_A.update_layout(
    title="Sample Size vs Mean and Confidence Interval",
    xaxis_title="Sample Size",
    yaxis_title="Mean / Confidence Interval",
    showlegend=True
)

# B. Histogram of the entire sample and a small subset of the sample

subset_size = st.slider(
    "Subset Size for Histogram",
    min_value=10,
    max_value=max_sample_size,
    value=50)

# Plot histograms for full data and a random subset
fig_B, axes = plt.subplots(1, 2, figsize=(12, 6))

# Full data histogram
axes[0].hist(full_data, bins=30, color='lightblue', edgecolor='black')
axes[0].set_title("Histogram of Full Data")
axes[0].set_xlabel("Data Value")
axes[0].set_ylabel("Frequency")

# Subset data histogram
subset_data = np.random.choice(full_data, subset_size, replace=False)
axes[1].hist(subset_data, bins=30, color='lightgreen', edgecolor='black')
axes[1].set_title(f"Histogram of Subset (n={subset_size})")
axes[1].set_xlabel("Data Value")
axes[1].set_ylabel("Frequency")

# Display the histograms as an image
st.pyplot(fig_B)

# Display the interactive plot for Sample Size vs Mean and Confidence Interval
st.plotly_chart(fig_A)
