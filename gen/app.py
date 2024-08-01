import streamlit as st
import pandas as pd
import base64
from genetic_algorithm import combined_genetic_algorithm

# Initialize session state for progress bar and best ordering
if 'progress_bar' not in st.session_state:
    st.session_state.progress_bar = None

if 'best_ordering' not in st.session_state:
    st.session_state.best_ordering = None

if 'fitness_values' not in st.session_state:
    st.session_state.fitness_values = None

# Function to run optimization
def run_optimization(rules, constraints, population_size, generations, mutation_rate):
    try:
        st.session_state.progress_bar = st.progress(0)
        best_ordering, population = combined_genetic_algorithm(rules, constraints, population_size, generations, mutation_rate, st.session_state.progress_bar)
        st.session_state.best_ordering = best_ordering
        st.session_state.fitness_values = [ind.fitness.values[0] for ind in population]
    except Exception as e:
        st.error(f"An error occurred during optimization: {e}")

# Function to create a download link for a dataframe
def get_table_download_link(df, filename, link_text):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="{filename}">{link_text}</a>'

# Streamlit UI
st.title("Firewall Rules Optimization")

uploaded_file = st.file_uploader("Upload your sample file", type=["csv"])
if uploaded_file is not None:
    try:
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

        if st.session_state.best_ordering is not None:
            optimized_df = pd.DataFrame([firewall_rules[i] for i in st.session_state.best_ordering])
            fitness_values = st.session_state.fitness_values

            # Enhanced Download button
            st.markdown(
                """
                <style>
                .download-btn {
                    background-color: #4CAF50;
                    color: white;
                    padding: 10px 20px;
                    text-align: center;
                    text-decoration: none;
                    display: inline-block;
                    font-size: 16px;
                    margin: 4px 2px;
                    cursor: pointer;
                    border-radius: 12px;
                    transition-duration: 0.4s;
                }
                .download-btn:hover {
                    background-color: white;
                    color: black;
                    border: 2px solid #4CAF50;
                }
                </style>
                """, unsafe_allow_html=True
            )

            download_link = get_table_download_link(optimized_df, 'optimized_rules.csv', 'Download Optimized Rules')
            st.markdown(download_link, unsafe_allow_html=True)

            st.write("Optimized Rules:", optimized_df)
            st.write("Fitness Values:", fitness_values)
    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")
else:
    st.write("Please upload a sample file to start optimization.")
