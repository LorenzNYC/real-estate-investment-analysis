#!/usr/bin/env python3
"""
Automated Real Estate Underwriting Dashboard
===========================================
Comprehensive dashboard integrating underwriting engine and property sourcing.
"""

import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.express as px
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
from typing import Dict, List
import json

from src.underwriting_engine import UnderwritingEngine, PropertyData
from src.property_sourcer import PropertySourcer, ClientScenario

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Initialize engines
underwriting_engine = UnderwritingEngine()
property_sourcer = PropertySourcer()

# Define client scenarios
SARAH_HUSBAND = ClientScenario(
    name="Sarah & Husband",
    max_oop=375000,
    max_purchase_price=375000,
    min_coc_return=0.09,
    location="Houston, TX",
    requirements=["Minimum 9% CoC return", "Max $375K OOP"]
)

RISAHL = ClientScenario(
    name="Risahl",
    max_oop=175000,
    max_purchase_price=500000,
    min_coc_return=0.05,
    location="Houston, TX",
    requirements=["Minimum 5% CoC return", "Max $175K OOP"]
)

# App layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Real Estate Underwriting Dashboard", className="text-center mb-4"),
            html.Hr()
        ])
    ]),
    
    # Scenario Selection
    dbc.Row([
        dbc.Col([
            html.H3("Client Scenario Analysis"),
            dbc.ButtonGroup([
                dbc.Button("Sarah & Husband", id="sarah-btn", color="primary", n_clicks=0),
                dbc.Button("Risahl", id="risahl-btn", color="secondary", n_clicks=0)
            ], className="mb-3")
        ])
    ]),
    
    # Results Display
    dbc.Row([
        dbc.Col([
            html.Div(id="scenario-results")
        ])
    ]),
    
    # Property Analysis
    dbc.Row([
        dbc.Col([
            html.H3("Property Analysis"),
            html.Div(id="property-analysis")
        ])
    ]),
    
    # Charts
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="coc-comparison-chart")
        ], width=6),
        dbc.Col([
            dcc.Graph(id="cash-flow-chart")
        ], width=6)
    ]),
    
    # Optimization Opportunities
    dbc.Row([
        dbc.Col([
            html.H3("Optimization Opportunities"),
            html.Div(id="optimization-opportunities")
        ])
    ]),
    
    # Risk Assessment
    dbc.Row([
        dbc.Col([
            html.H3("Risk Assessment"),
            html.Div(id="risk-assessment")
        ])
    ])
], fluid=True)

@app.callback(
    Output("scenario-results", "children"),
    [Input("sarah-btn", "n_clicks"),
     Input("risahl-btn", "n_clicks")]
)
def update_scenario_results(sarah_clicks, risahl_clicks):
    """Update scenario results based on button clicks"""
    ctx = dash.callback_context
    if not ctx.triggered:
        return html.P("Select a scenario to analyze")
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if button_id == "sarah-btn":
        scenario = SARAH_HUSBAND
    elif button_id == "risahl-btn":
        scenario = RISAHL
    else:
        return html.P("Select a scenario to analyze")
    
    # Analyze scenario
    results = property_sourcer.analyze_scenario(scenario)
    
    if results['properties_found'] == 0:
        return dbc.Alert(
            f"No properties found meeting requirements for {scenario.name}",
            color="warning"
        )
    
    # Create results cards
    cards = []
    for i, rec in enumerate(results['recommendations']):
        card = dbc.Card([
            dbc.CardHeader(f"Property {i+1}: {rec['address']}"),
            dbc.CardBody([
                html.H5(f"Purchase Price: ${rec['purchase_price']:,.0f}"),
                html.P(f"Down Payment: ${rec['down_payment']:,.0f}"),
                html.P(f"Total OOP: ${rec['total_oop']:,.0f}"),
                html.P(f"CoC Return: {rec['coc_return']:.1%}"),
                html.P(f"Monthly Cash Flow: ${rec['monthly_cash_flow']:,.0f}"),
                html.P(f"Risk Level: {rec['risk_level']}"),
                html.P(f"Recommendation: {rec['recommendation']}"),
                html.P(f"Optimization Opportunities: {rec['optimization_opportunities']}")
            ])
        ], className="mb-3")
        cards.append(card)
    
    return cards

@app.callback(
    Output("property-analysis", "children"),
    [Input("sarah-btn", "n_clicks"),
     Input("risahl-btn", "n_clicks")]
)
def update_property_analysis(sarah_clicks, risahl_clicks):
    """Update detailed property analysis"""
    ctx = dash.callback_context
    if not ctx.triggered:
        return html.P("Select a scenario to view property analysis")
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if button_id == "sarah-btn":
        scenario = SARAH_HUSBAND
    elif button_id == "risahl-btn":
        scenario = RISAHL
    else:
        return html.P("Select a scenario to view property analysis")
    
    # Get top property for detailed analysis
    results = property_sourcer.analyze_scenario(scenario)
    if not results['recommendations']:
        return html.P("No properties found for detailed analysis")
    
    top_property = results['recommendations'][0]
    
    # Build scenario cards before constructing the layout
    scenarios = top_property['scenarios']
    scenario_cards = []
    for scenario_type, data in scenarios.items():
        card = dbc.Card([
            dbc.CardHeader(scenario_type.title() + " Scenario"),
            dbc.CardBody([
                html.P(f"Rent: ${data['rent']:,.0f}/month"),
                html.P(f"Expenses: ${data['expenses']:,.0f}/month"),
                html.P(f"CoC Return: {data['coc_return']:.1%}")
            ])
        ], className="mb-2")
        scenario_cards.append(card)

    # Create detailed analysis
    analysis = dbc.Card([
        dbc.CardHeader("Detailed Property Analysis"),
        dbc.CardBody([
            html.H4(top_property['address']),
            html.Hr(),

            # Financial Summary
            html.H5("Financial Summary"),
            dbc.Row([
                dbc.Col([
                    html.P(f"Purchase Price: ${top_property['purchase_price']:,.0f}"),
                    html.P(f"Down Payment: ${top_property['down_payment']:,.0f}"),
                    html.P(f"Total OOP: ${top_property['total_oop']:,.0f}")
                ], width=6),
                dbc.Col([
                    html.P(f"CoC Return: {top_property['coc_return']:.1%}"),
                    html.P(f"Monthly Cash Flow: ${top_property['monthly_cash_flow']:,.0f}"),
                    html.P(f"Risk Level: {top_property['risk_level']}")
                ], width=6)
            ]),

            html.Hr(),

            # Scenario Analysis
            html.H5("Scenario Analysis"),
            dbc.Row([
                dbc.Col(card, width=4) for card in scenario_cards
            ])
        ])
    ])
    
    return analysis

@app.callback(
    Output("coc-comparison-chart", "figure"),
    [Input("sarah-btn", "n_clicks"),
     Input("risahl-btn", "n_clicks")]
)
def update_coc_chart(sarah_clicks, risahl_clicks):
    """Update CoC comparison chart"""
    ctx = dash.callback_context
    if not ctx.triggered:
        return go.Figure()
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if button_id == "sarah-btn":
        scenario = SARAH_HUSBAND
    elif button_id == "risahl-btn":
        scenario = RISAHL
    else:
        return go.Figure()
    
    results = property_sourcer.analyze_scenario(scenario)
    if not results['recommendations']:
        return go.Figure()
    
    # Create CoC comparison chart
    addresses = [rec['address'][:20] + "..." for rec in results['recommendations']]
    coc_returns = [rec['coc_return'] * 100 for rec in results['recommendations']]
    
    fig = go.Figure(data=[
        go.Bar(
            x=addresses,
            y=coc_returns,
            text=[f"{coc:.1f}%" for coc in coc_returns],
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title="Cash-on-Cash Return Comparison",
        xaxis_title="Properties",
        yaxis_title="CoC Return (%)",
        height=400
    )
    
    return fig

@app.callback(
    Output("cash-flow-chart", "figure"),
    [Input("sarah-btn", "n_clicks"),
     Input("risahl-btn", "n_clicks")]
)
def update_cash_flow_chart(sarah_clicks, risahl_clicks):
    """Update cash flow chart"""
    ctx = dash.callback_context
    if not ctx.triggered:
        return go.Figure()
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if button_id == "sarah-btn":
        scenario = SARAH_HUSBAND
    elif button_id == "risahl-btn":
        scenario = RISAHL
    else:
        return go.Figure()
    
    results = property_sourcer.analyze_scenario(scenario)
    if not results['recommendations']:
        return go.Figure()
    
    # Create cash flow chart
    addresses = [rec['address'][:20] + "..." for rec in results['recommendations']]
    cash_flows = [rec['monthly_cash_flow'] for rec in results['recommendations']]
    
    fig = go.Figure(data=[
        go.Bar(
            x=addresses,
            y=cash_flows,
            text=[f"${cf:,.0f}" for cf in cash_flows],
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title="Monthly Cash Flow Comparison",
        xaxis_title="Properties",
        yaxis_title="Monthly Cash Flow ($)",
        height=400
    )
    
    return fig

@app.callback(
    Output("optimization-opportunities", "children"),
    [Input("sarah-btn", "n_clicks"),
     Input("risahl-btn", "n_clicks")]
)
def update_optimization_opportunities(sarah_clicks, risahl_clicks):
    """Update optimization opportunities"""
    ctx = dash.callback_context
    if not ctx.triggered:
        return html.P("Select a scenario to view optimization opportunities")
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if button_id == "sarah-btn":
        scenario = SARAH_HUSBAND
    elif button_id == "risahl-btn":
        scenario = RISAHL
    else:
        return html.P("Select a scenario to view optimization opportunities")
    
    results = property_sourcer.analyze_scenario(scenario)
    if not results['recommendations']:
        return html.P("No properties found for optimization analysis")
    
    # Get optimization opportunities for top property
    top_property_data = None
    for prop in property_sourcer.generate_houston_properties(scenario.max_purchase_price, scenario.min_coc_return):
        if prop.address == results['recommendations'][0]['address']:
            top_property_data = prop
            break
    
    if not top_property_data:
        return html.P("Property data not found")
    
    # Perform underwriting analysis to get optimization opportunities
    underwriting_result = underwriting_engine.underwrite_property(top_property_data)
    
    # Create optimization opportunities cards
    cards = []
    for opp in underwriting_result.optimization_opportunities:
        card = dbc.Card([
            dbc.CardHeader(f"{opp['title']} ({opp['category']})"),
            dbc.CardBody([
                html.P(opp['description']),
                html.P(f"Investment: ${opp['investment']:,.0f}"),
                html.P(f"Annual Benefit: ${opp['annual_benefit']:,.0f}"),
                html.P(f"ROI: {opp['roi']:.1%}" if opp['roi'] != float('inf') else "ROI: Infinite"),
                html.P(f"Implementation Time: {opp['implementation_time']}"),
                html.P(f"Priority: {opp['priority']}"),
                html.P(f"Risk Level: {opp['risk_level']}")
            ])
        ], className="mb-2")
        cards.append(card)
    
    return cards

@app.callback(
    Output("risk-assessment", "children"),
    [Input("sarah-btn", "n_clicks"),
     Input("risahl-btn", "n_clicks")]
)
def update_risk_assessment(sarah_clicks, risahl_clicks):
    """Update risk assessment"""
    ctx = dash.callback_context
    if not ctx.triggered:
        return html.P("Select a scenario to view risk assessment")
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if button_id == "sarah-btn":
        scenario = SARAH_HUSBAND
    elif button_id == "risahl-btn":
        scenario = RISAHL
    else:
        return html.P("Select a scenario to view risk assessment")
    
    results = property_sourcer.analyze_scenario(scenario)
    if not results['recommendations']:
        return html.P("No properties found for risk assessment")
    
    # Get risk assessment for top property
    top_property_data = None
    for prop in property_sourcer.generate_houston_properties(scenario.max_purchase_price, scenario.min_coc_return):
        if prop.address == results['recommendations'][0]['address']:
            top_property_data = prop
            break
    
    if not top_property_data:
        return html.P("Property data not found")
    
    # Perform underwriting analysis to get risk assessment
    underwriting_result = underwriting_engine.underwrite_property(top_property_data)
    
    # Create risk assessment card
    risk_card = dbc.Card([
        dbc.CardHeader("Risk Assessment"),
        dbc.CardBody([
            html.H5(f"Risk Level: {underwriting_result.risk_assessment['risk_level']}"),
            html.P(f"Risk Score: {underwriting_result.risk_assessment['risk_score']}"),
            html.Hr(),
            html.H6("Risk Factors:"),
            html.Ul([html.Li(factor) for factor in underwriting_result.risk_assessment['risk_factors']]),
            html.Hr(),
            html.H6("Mitigation Strategies:"),
            html.Ul([html.Li(strategy) for strategy in underwriting_result.risk_assessment['mitigation_strategies']])
        ])
    ])
    
    return risk_card

if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0', port=8050)
