import streamlit as st
import pandas as pd
import base64
from genetic_algorithm import combined_genetic_algorithm

# Initialize session state for progress bar and best ordering
if 'progress_bar' not in st.session_state:
    st.session_state.progress_bar = None

if 'best_ordering_sgg' not in st.session_state:
    st.session_state.best_ordering_sgg = None

if 'best_ordering_plus' not in st.session_state:
    st.session_state.best_ordering_plus = None

if 'fitness_values_sgg' not in st.session_state:
    st.session_state.fitness_values_sgg = None

if 'fitness_values_plus' not in st.session_state:
    st.session_state.fitness_values_plus = None

# Function to run optimization
def run_optimization(rules, constraints, population_size, generations, mutation_rate):
    try:
        st.session_state.progress_bar = st.progress(0)
        best_ordering_sgg, best_ordering_plus = combined_genetic_algorithm(rules, constraints, population_size, generations, mutation_rate, st.session_state.progress_bar)
        st.session_state.best_ordering_sgg = best_ordering_sgg
        st.session_state.best_ordering_plus = best_ordering_plus
    except Exception as e:
        st.error(f"An error occurred during optimization: {e}")
    finally:
        st.experimental_rerun()  # Force rerun to update UI

# Streamlit UI
st.title("Firewall Rules Optimization")

uploaded_file = st.file_uploader("Upload your sample file", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("Uploaded Sample Data:", df)

    # Example columns
    population_size = st.number_input("Population Size", min_value=1, value=100)
    generations = st.number_input("Generations", min_value=1, value=50)
    mutation_rate = st.number_input("Mutation Rate", min_value=0.0, max_value=1.0, step=0.01, value=0.1)

    firewall_rules = df.to_dict('records')  # Convert dataframe to list of dicts
    valid_constraints = [(firewall_rules[i], firewall_rules[i + 1]) for i in range(len(firewall_rules) - 1)]  # Example constraints

    if st.button("Optimize Rules"):
        run_optimization(firewall_rules, valid_constraints, population_size, generations, mutation_rate)

    if st.session_state.best_ordering_sgg is not None and st.session_state.best_ordering_plus is not None:
        optimized_df_sgg = pd.DataFrame([firewall_rules[i] for i in st.session_state.best_ordering_sgg])
        optimized_df_plus = pd.DataFrame([firewall_rules[i] for i in st.session_state.best_ordering_plus])

        # Display and Download buttons
        st.write("Optimized Rules (SGG-GA):", optimized_df_sgg)
        st.write("Optimized Rules (+-GA):", optimized_df_plus)

        def convert_df(df):
            return df.to_csv(index=False).encode('utf-8')

        csv_sgg = convert_df(optimized_df_sgg)
        csv_plus = convert_df(optimized_df_plus)

        st.download_button(
            label="Download Optimized Rules (SGG-GA)",
            data=csv_sgg,
            file_name='optimized_rules_sgg.csv',
            mime='text/csv',
            key='download-csv-sgg'
        )

        st.download_button(
            label="Download Optimized Rules (+-GA)",
            data=csv_plus,
            file_name='optimized_rules_plus.csv',
            mime='text/csv',
            key='download-csv-plus'
        )

else:
    st.write("Please upload a sample file to start optimization.")
