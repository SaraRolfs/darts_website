import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

def plot_winning_averages(selected_tournaments, add_regression=False, add_std=False, apply_to_all=False):
    
    def custom_index_order(n):
        sequence = [0, 5, 2, 3, 6, 10, 8, 4, 7]
        return (sequence * ((n // len(sequence)) + 1))[:n]
    
    major_tournaments_all = [
        "World Championship", "World Matchplay", "World Grand Prix", "Grand Slam",
        "Players Championship Finals", "World Series of Darts Finals",
    ]
    extra_tournaments_all = ["European Tour", "Players Championship"]
    
    major_tournaments = [t for t in selected_tournaments if t in major_tournaments_all]
    extra_tournaments = [t for t in selected_tournaments if t in extra_tournaments_all]
    only_one = len(selected_tournaments) == 1
    
    file = 'Data/question 2/question2.csv'
    df = pd.read_csv(file)
    df.columns = df.columns.str.strip()
    df_cleaned = df.dropna(subset=['Average'])
    df_cleaned = df_cleaned[df_cleaned['Average'] >= 10]
    
    df_all = df_cleaned[
        df_cleaned['Tournament'].isin(major_tournaments_all) | 
        df_cleaned['Tournament'].str.startswith(tuple(extra_tournaments_all), na=False) & 
        ~df_cleaned['Tournament'].str.contains("Qualifier", na=False)
    ]
    
    if apply_to_all:
        df_selected = df_all
    elif only_one:
        df_selected = df_cleaned[df_cleaned['Tournament'] == selected_tournaments[0]]
    elif extra_tournaments:
        df_selected = df_cleaned[
            df_cleaned['Tournament'].isin(major_tournaments) |
            df_cleaned['Tournament'].str.startswith(tuple(extra_tournaments), na=False) & 
            ~df_cleaned['Tournament'].str.contains("Qualifier", na=False)
        ]
    else:
        df_selected = df_cleaned[
            df_cleaned['Tournament'].isin(major_tournaments) | 
            ~df_cleaned['Tournament'].str.contains("Qualifier", na=False)
        ]
    
    def normalize_tournament_name(name):
        return name.translate(str.maketrans('', '', '0123456789')).strip()
    
    df_selected['Tournament'] = df_selected['Tournament'].apply(normalize_tournament_name)
    df_all['Tournament'] = df_all['Tournament'].apply(normalize_tournament_name)
    
    df_selected['Date'] = pd.to_datetime(df_selected['Date'], errors='coerce')
    df_all['Date'] = pd.to_datetime(df_all['Date'], errors='coerce')
    
    df_selected['Year'] = df_selected['Date'].dt.year
    df_all['Year'] = df_all['Date'].dt.year
    
    df_selected = df_selected[df_selected['Year'] >= 2000]
    df_all = df_all[df_all['Year'] >= 2000]
    
    df_grouped = df_selected.groupby(['Year', 'Tournament'])['Average'].mean().reset_index()
    
    tournaments = df_grouped['Tournament'].unique()
    prism_colors = px.colors.qualitative.Prism
    index_order = custom_index_order(len(tournaments))
    color_map = {tournaments[i]: prism_colors[index_order[i] % len(prism_colors)] for i in range(len(tournaments))}
    
    fig = go.Figure()
    
    for tournament in selected_tournaments:
        df_tournament = df_grouped[df_grouped['Tournament'] == tournament]
        fig.add_trace(go.Scatter(
            x=df_tournament['Year'],
            y=df_tournament['Average'],
            mode='lines',
            name=tournament,
            line=dict(color=color_map.get(tournament, "gray"))
        ))
    
    avg_selected = df_selected.groupby('Year')['Average'].mean()
    
    if not avg_selected.empty:
        fig.add_trace(go.Scatter(
            x=avg_selected.index,
            y=avg_selected.values,
            mode='lines',
            line=dict(width=3, dash='dot', color="black"),
            name="Average of selected tournaments",
        ))
    
    if add_regression and len(avg_selected) > 1:
        x_years = avg_selected.index.to_numpy()
        y_avg = avg_selected.values
        coeffs = np.polyfit(x_years, y_avg, deg=1)
        regression_line = np.poly1d(coeffs)
        
        fig.add_trace(go.Scatter(
            x=x_years,
            y=regression_line(x_years),
            mode="lines",
            line=dict(color="magenta", width=2, dash="dash"),
            name="Regression Line"
        ))
    
    if add_std and len(avg_selected) > 1:
        min_year = avg_selected.index.min()
        std_per_year = df_selected[df_selected['Year'] >= min_year].groupby('Year')['Average'].std()
        
        if not std_per_year.empty:
            fig.add_trace(go.Scatter(
                x=std_per_year.index.tolist() + std_per_year.index[::-1].tolist(),
                y=(avg_selected + std_per_year).tolist() + (avg_selected - std_per_year).tolist()[::-1],
                fill="toself",
                fillcolor="rgba(0, 0, 255, 0.2)",
                line=dict(color="rgba(255,255,255,0)"),
                name="Standard Deviation"
            ))
    
    fig.update_layout(
        title="Development of Average Scores Over the Years",
        xaxis_title="Year",
        yaxis_title="Average Score",
        legend_title="Tournaments",
        hovermode="x unified"
    )
    
    return fig
