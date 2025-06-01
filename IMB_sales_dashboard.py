#!/usr/bin/env python3
"""
Automobile Sales Dashboard

This project served as part of the Final Project for the "Data Visualization with Python" 
course in the IBM Data Analyst Professional Certificate. This dashboard visualizes car 
sales data using Plotly and Dash in Python.

Author: Dr. Pooja (original), enhanced with modern styling
"""

# Import required packages
import dash
import pandas as pd
import plotly.express as px
from dash import dcc, html
from dash.dependencies import Input, Output

# Set CSS Style Preferences for the dashboard
external_stylesheets = ['https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap']

# Initialize the Dash app with external stylesheets
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Set the title of the dashboard
app.title = "Automobile Statistics Dashboard"

# Modern color scheme
colors = {
    'background': '#f8fafc',
    'surface': '#ffffff',
    'primary': '#2563eb',
    'primary_light': '#3b82f6', 
    'text': '#1f2937',
    'text_light': '#6b7280',
    'accent': '#10b981',
    'border': '#e5e7eb'
}

# Load the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Clean up vehicle type names globally -- for better visualization display
vehicle_name_mapping = {
    'Executivecar': 'Executive Car',
    'Mediumfamilycar': 'Medium Family Car', 
    'Smallfamiliycar': 'Small Family Car',
    'Sports': 'Sports Car',
    'Supperminicar': 'Supermini Car'
}

data['Vehicle_Type'] = data['Vehicle_Type'].replace(vehicle_name_mapping)

# Create the dropdown menu options
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]

# List of years (for convenience)
year_list = [i for i in range(1980, 2024, 1)]

# Create the layout with modern styling
app.layout = html.Div([
    # Main container
    html.Div([
        # Header section
        html.Div([
            html.H1("Automobile Sales Analytics", # title
                style={
                    'textAlign': 'center',
                    'color': '#ffffff',
                    'fontSize': '2.5rem',
                    'fontWeight': '700',
                    'fontFamily': 'Inter, -apple-system, BlinkMacSystemFont, sans-serif',
                    'marginBottom': '0.5rem',
                    'letterSpacing': '-0.025em'
                }),
            html.P("Interactive dashboard for automobile sales statistics and trends", # subtitle
                style={
                    'textAlign': 'center',
                    'color': '#e5e7eb',
                    'fontSize': '1.1rem',
                    'fontFamily': 'Inter, sans-serif',
                    'marginBottom': '3rem',
                    'fontWeight': '400'
                })
        ], style={
            'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            'padding': '4rem 2rem',
            'marginBottom': '2rem',
            'borderRadius': '0 0 24px 24px',
            'boxShadow': '0 10px 25px rgba(0,0,0,0.1)'
        }),
        
        # Controls section
        html.Div([
            html.Div([
                html.Div([
                    html.Label('Report Type', 
                        style={
                            'fontSize': '1rem',
                            'fontWeight': '600',
                            'color': colors['text'],
                            'fontFamily': 'Inter, sans-serif',
                            'marginBottom': '0.5rem',
                            'display': 'block'
                        }),
                    dcc.Dropdown(
                        id='dropdown-statistics',
                        options=dropdown_options,
                        value=None,
                        placeholder='Select a report type',
                        style={
                            'fontFamily': 'Inter, sans-serif',
                            'fontSize': '1rem'
                        }
                    )
                ], style={
                    'background': colors['surface'],
                    'padding': '1.5rem',
                    'borderRadius': '12px',
                    'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.05)',
                    'border': f'1px solid {colors["border"]}',
                    'width': '48%'
                }),
                
                html.Div([
                    html.Label('Select Year', 
                        style={
                            'fontSize': '1rem',
                            'fontWeight': '600',
                            'color': colors['text'],
                            'fontFamily': 'Inter, sans-serif',
                            'marginBottom': '0.5rem',
                            'display': 'block'
                        }),
                    dcc.Dropdown(
                        id='select-year',
                        options=[{'label': i, 'value': i} for i in year_list],
                        value=None,
                        placeholder='Select year',
                        style={
                            'fontFamily': 'Inter, sans-serif',
                            'fontSize': '1rem'
                        }
                    )
                ], style={
                    'background': colors['surface'],
                    'padding': '1.5rem',
                    'borderRadius': '12px',
                    'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.05)',
                    'border': f'1px solid {colors["border"]}',
                    'width': '48%'
                })
            ], style={
                'display': 'flex',
                'justifyContent': 'space-between',
                'gap': '1rem',
                'marginBottom': '2rem'
            })
        ], style={
            'maxWidth': '1200px',
            'margin': '0 auto',
            'padding': '0 2rem'
        }),
        
        # Charts container
        html.Div(id='output-container', style={
            'maxWidth': '1200px',
            'margin': '0 auto',
            'padding': '0 2rem'
        })
        
    ], style={
        'backgroundColor': colors['background'],
        'minHeight': '100vh',
        'fontFamily': 'Inter, -apple-system, BlinkMacSystemFont, sans-serif'
    })
])

# Callback 1: Enable or Disable Year Selection and Reset Value
@app.callback(
    [Output(component_id='select-year', component_property='disabled'),
     Output(component_id='select-year', component_property='value')], 
    Input(component_id='dropdown-statistics', component_property='value'))

def update_input_container(selected_statistics):
    """
    This callback enables or disables the year selection dropdown based on the 
    user's choice of report type and resets the year value when report type changes.
    """
    if selected_statistics == 'Yearly Statistics': 
        return False, None  # Enable dropdown, reset value
    else: 
        return True, None   # Disable dropdown, reset value

# Callback 2: Generate Charts Based on User Selections
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='dropdown-statistics', component_property='value'), 
     Input(component_id='select-year', component_property='value')])

def update_output_container(selected_statistics, input_year):
    """
    This callback filters the data based on the report type selected and generates
    appropriate visualizations.
    """
    # Chart configuration - clean up options
    chart_config = {
        'displayModeBar': True,
        'displaylogo': False,
        'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'select2d'],
    }
    
    # Set a layout template for the visualizations
    chart_layout_template = {
        'font': {'family': 'Inter, sans-serif', 'size': 14, 'color': colors['text']},
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'title': {
            'font': {'size': 18, 'family': 'Inter, sans-serif', 'color': colors['text']},
            'x': 0.5,
            'xanchor': 'center'
        },
        'xaxis': {
            'gridcolor': colors['border'],
            'linecolor': colors['border'],
            'tickfont': {'family': 'Inter, sans-serif', 'color': colors['text_light']}
        },
        'yaxis': {
            'gridcolor': colors['border'],
            'linecolor': colors['border'],
            'tickfont': {'family': 'Inter, sans-serif', 'color': colors['text_light']}
        }
    }
    
    if selected_statistics == 'Recession Period Statistics':
        recession_data = data[data['Recession'] == 1]
        
        # Plot 1: Automobile sales fluctuate over Recession Period (year wise)
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        fig1 = px.line(yearly_rec, x='Year', y='Automobile_Sales',
                       title="Average Automobile Sales During Recession Period")
        fig1.update_layout(chart_layout_template)
        fig1.update_traces(line=dict(color=colors['primary'], width=3))
        fig1.update_xaxes(title_text="Year")
        fig1.update_yaxes(title_text="Automobile Sales")
        
        R_chart1 = dcc.Graph(figure=fig1, config=chart_config)
        
        # Plot 2: Calculate the average number of vehicles sold by vehicle type       
        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        fig2 = px.bar(average_sales, x='Vehicle_Type', y='Automobile_Sales', color='Vehicle_Type',
                      title="Average Sales by Vehicle Type During Recession")
        fig2.update_layout(chart_layout_template)
        fig2.update_layout(legend_title_text='Vehicle Type')
        fig2.update_xaxes(title_text="Vehicle Type")
        fig2.update_yaxes(title_text="Automobile Sales")
        
        R_chart2 = dcc.Graph(figure=fig2, config=chart_config)
        
        # Plot 3: Pie chart for total expenditure share by vehicle type during recessions
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        fig3 = px.pie(exp_rec, values='Advertising_Expenditure', names='Vehicle_Type',
                      title="Advertising Expenditure Share by Vehicle Type")
        fig3.update_layout(chart_layout_template)
        fig3.update_layout(legend_title_text='Vehicle Type')
        fig3.update_traces(textfont=dict(family='Inter, sans-serif'))
        
        R_chart3 = dcc.Graph(figure=fig3, config=chart_config)
        
        # Plot 4: Bar chart for the effect of unemployment rate on vehicle type and sales
        unemp_data = recession_data.groupby(['unemployment_rate', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        fig4 = px.bar(unemp_data, x='unemployment_rate', y='Automobile_Sales', color='Vehicle_Type',
                      title='Effect of Unemployment Rate on Vehicle Sales')
        fig4.update_layout(chart_layout_template)
        fig4.update_layout(legend_title_text='Vehicle Type')
        fig4.update_xaxes(title_text="Unemployment Rate")
        fig4.update_yaxes(title_text="Automobile Sales")
        
        R_chart4 = dcc.Graph(figure=fig4, config=chart_config)
        
        return [
            html.Div([
                html.Div(R_chart1, style={'width': '50%', 'padding': '0.5rem'}),
                html.Div(R_chart2, style={'width': '50%', 'padding': '0.5rem'})
            ], style={'display': 'flex', 'marginBottom': '1rem'}),
            html.Div([
                html.Div(R_chart3, style={'width': '50%', 'padding': '0.5rem'}),
                html.Div(R_chart4, style={'width': '50%', 'padding': '0.5rem'})
            ], style={'display': 'flex'})
        ]
        
    elif selected_statistics == 'Yearly Statistics' and input_year:
        yearly_data = data[data['Year'] == int(input_year)]
        
        # Plot 5: Yearly Automobile sales using line chart for the whole period
        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        fig5 = px.line(yas, x='Year', y='Automobile_Sales', title='Yearly Automobile Sales')
        fig5.update_layout(chart_layout_template)
        fig5.update_traces(line=dict(color=colors['accent'], width=3))
        fig5.update_xaxes(title_text="Year")
        fig5.update_yaxes(title_text="Automobile Sales")
        
        Y_chart1 = dcc.Graph(figure=fig5, config=chart_config)
        
        # Plot 6: Total Monthly Automobile sales using line chart
        mas = data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        fig6 = px.line(mas, x='Month', y='Automobile_Sales', title='Monthly Automobile Sales')
        fig6.update_layout(chart_layout_template)
        fig6.update_traces(line=dict(color=colors['primary'], width=3))
        fig6.update_xaxes(title_text="Month")
        fig6.update_yaxes(title_text="Automobile Sales")
        
        Y_chart2 = dcc.Graph(figure=fig6, config=chart_config)
        
        # Plot 7: Bar chart for average number of vehicles sold during the given year
        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        fig7 = px.bar(avr_vdata, x='Vehicle_Type', y='Automobile_Sales', color='Vehicle_Type',
                      title=f'Average Vehicle Sales in {input_year}')
        fig7.update_layout(chart_layout_template)
        fig7.update_layout(legend_title_text='Vehicle Type')
        fig7.update_xaxes(title_text="Vehicle Type")
        fig7.update_yaxes(title_text="Automobile Sales")
        
        Y_chart3 = dcc.Graph(figure=fig7, config=chart_config)
        
        # Plot 8: Total Advertisement Expenditure for each vehicle using pie chart
        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        fig8 = px.pie(exp_data, values='Advertising_Expenditure', names='Vehicle_Type',
                title='Advertisement Expenditure by Vehicle Type')
        fig8.update_layout(chart_layout_template)
        fig8.update_layout(legend_title_text='Vehicle Type')
        
        Y_chart4 = dcc.Graph(figure=fig8, config=chart_config)
        
        return [
            html.Div([
                html.Div(Y_chart1, style={'width': '50%', 'padding': '0.5rem'}),
                html.Div(Y_chart2, style={'width': '50%', 'padding': '0.5rem'})
            ], style={'display': 'flex', 'marginBottom': '1rem'}),
            html.Div([
                html.Div(Y_chart3, style={'width': '50%', 'padding': '0.5rem'}),
                html.Div(Y_chart4, style={'width': '50%', 'padding': '0.5rem'})
            ], style={'display': 'flex'})
        ]
     
    # Display homepage message if nothing is selected    
    else:
        return html.Div([
            html.Div([
                html.H3("Welcome to the Automobile Sales Dashboard", 
                    style={
                        'textAlign': 'center',
                        'color': colors['text'],
                        'fontFamily': 'Inter, sans-serif',
                        'marginBottom': '1rem'
                    }),
                html.P("Please select a report type to begin exploring the data.",
                    style={
                        'textAlign': 'center',
                        'color': colors['text_light'],
                        'fontFamily': 'Inter, sans-serif'
                    })
            ], style={
                'background': colors['surface'],
                'padding': '3rem',
                'borderRadius': '12px',
                'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.05)',
                'border': f'1px solid {colors["border"]}',
                'textAlign': 'center'
            })
        ])

# Run the Dash app
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8051)