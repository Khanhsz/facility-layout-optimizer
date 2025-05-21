import streamlit as st
import numpy as np
from itertools import combinations

# --- Page Setup ---
st.set_page_config(page_title="Pairwise Exchange Optimizer", layout="centered")

# --- Title ---
st.title("🔁 Pairwise Exchange Layout Optimizer")
st.markdown("Optimize facility layout by minimizing total cost using pairwise swaps.")

# --- Sample Input ---
sample_flow = """- 10 15 20
0 - 10 5
0 0 - 5
0 0 0 -"""

sample_dist = """- 1 2 3
1 - 1 2
2 1 - 1
3 2 1 -"""

# --- Input Section ---
st.subheader("📥 Input Matrices")
flow_input = st.text_area("FLOW Matrix", sample_flow, height=150)
dist_input = st.text_area("DISTANCE Matrix", sample_dist, height=150)

# --- Helper Functions ---
def parse_matrix(input_str):
    lines = input_str.strip().split("\n")
    matrix = []
    for line in lines:
        row = [int(x) if x != '-' else 0 for x in line.strip().split()]
        matrix.append(row)
    return np.array(matrix)

def calculate_cost(flow, dist, layout):
    n = len(layout)
    cost = 0
    for i in range(n):
        for j in range(n):
            if i != j:
                cost += flow[i][j] * dist[layout[i]][layout[j]]
    return cost

def pairwise_exchange_optimizer(flow, dist):
    n = len(flow)
    layout = list(range(n))  # [0, 1, 2, 3]
    history = []
    iteration = 0

    while True:
        current_cost = calculate_cost(flow, dist, layout)
        best_cost = current_cost
        best_layout = layout[:]
        history.append((iteration, layout[:], current_cost))

        for i, j in combinations(range(n), 2):
            new_layout = layout[:]
            new_layout[i], new_layout[j] = new_layout[j], new_layout[i]
            new_cost = calculate_cost(flow, dist, new_layout)
            if new_cost < best_cost:
                best_cost = new_cost
                best_layout = new_layout[:]

        if best_layout == layout:
            break  # No improvement found
        layout = best_layout
        iteration += 1

    return layout, best_cost, history

# --- Run Optimization ---
if st.button("🚀 Run Optimization"):
    try:
        flow = parse_matrix(flow_input)
        dist = parse_matrix(dist_input)

        if flow.shape != dist.shape or flow.shape[0] != flow.shape[1]:
            st.error("❌ Matrices must be square and of the same dimension.")
            st.stop()

        final_layout, final_cost, history = pairwise_exchange_optimizer(flow, dist)

        # Output final result
        st.success(f"✅ Final Layout (1-based): {[x + 1 for x in final_layout]}")
        st.success(f"💰 Final Total Cost: {final_cost}")

        # Show all iterations
        st.markdown("### 📊 Iteration History")
        for iter_num, layout, cost in history:
            st.write(f"**Iteration {iter_num}:** Layout = {[x + 1 for x in layout]}, Cost = {cost}")

        # Show matrices
        st.markdown("### 📌
