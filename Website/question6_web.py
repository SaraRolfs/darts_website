import streamlit as st
from .question6_text import *
from .footer import add_footer
from Visualizations.question_6 import (
    plot_ranking_age,
    plot_ranking_nationality,
    plot_ranking_handedness
)

def question6_web():    
    st.title("Rankings vs. Properties")
    st.markdown("---")
    # Erstelle einen Slider von 0 bis 50
    selected_ranking_position= st.slider("Choose the number of ranking positions", min_value=1, max_value=50, value= 5)
    variant = st.radio("Choose an Option", ("absolute values", "relative values"))
    st.markdown("---")
    st.subheader("How does age, nationality and handiness effects the rankings?")
    
    with st.expander("Explanation"):
        st.write("Explanation")
    
    if variant == "absolute values":
        variant = 1
    else:
        variant = 0
    
    
    fig, _ = plot_ranking_age(selected_ranking_position, variant)
    st.plotly_chart(fig)
    st.write("Hier kommt eine kurze Beschreibung der Ergebnisse hin.")
    with st.expander("Interpretation and critical evaluation"):
        st.write(first_graph_6)
    
  
    fig, _ = plot_ranking_nationality(selected_ranking_position, variant)
    st.plotly_chart(fig)
    st.write("Hier kommt eine kurze Beschreibung der Ergebnisse hin.")
    with st.expander("Interpretation and critical evaluation"):
        st.write(second_graph_6)
    

    fig, _ = plot_ranking_handedness(selected_ranking_position, variant)
    st.plotly_chart(fig)
    st.write("Hier kommt eine kurze Beschreibung der Ergebnisse hin.")
    with st.expander("Interpretation and critical evaluation"):
        st.write(third_graph_6)

    # Call function to add footer
    add_footer()