#!/usr/bin/env python3
"""
Automated Real Estate Underwriting Dashboard
===========================================
Comprehensive dashboard integrating underwriting engine and property sourcing.
"""

import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from dash.dependencies import Input, Output

from src.property_sourcer import PropertySourcer, ClientScenario

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Initialize engine
property_sourcer = PropertySourcer()

# Button ID constants
SARAH_BTN = "sarah-btn"
RISAHL_BTN = "risahl-btn"

# Define client scenarios
SCENARIOS = {
    SARAH_BTN: ClientScenario(
        name="Sarah & Husband",
        max_oop=375000,
        max_purchase_price=375000,
        min_coc_return=0.09,
        location="Houston, TX",
        requirements=["Minimum 9% CoC return", "Max $375K OOP"]
    ),
    RISAHL_BTN: ClientScenario(
        name="Risahl",
        max_oop=175000,
        max_purchase_price=500000,
        min_coc_return=0.05,
        location="Houston, TX",
        requirements=["Minimum 5% CoC return", "Max $175K OOP"]
    ),
}

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
                dbc.Button("Sarah & Husband", id=SARAH_BTN, color="primary", n_clicks=0),
                dbc.Button("Risahl", id=RISAHL_BTN, color="secondary", n_clicks=0)
            ], className="mb-3")
        ])
    ]),

    # Results Display
    dbc.Row([dbc.Col([html.Div(id="scenario-results")])]),

    # Property Analysis
    dbc.Row([dbc.Col([html.H3("Property Analysis"), html.Div(id="property-analysis")])]),

    # Charts
    dbc.Row([
        dbc.Col([dcc.Graph(id="coc-comparison-chart")], width=6),
        dbc.Col([dcc.Graph(id="cash-flow-chart")], width=6)
    ]),

    # Optimization Opportunities
    dbc.Row([dbc.Col([html.H3("Optimization Opportunities"), html.Div(id="optimization-opportunities")])]),

    # Risk Assessment
    dbc.Row([dbc.Col([html.H3("Risk Assessment"), html.Div(id="risk-assessment")])])
], fluid=True)


def _get_scenario_from_context():
    """Return the scenario matching the clicked button, or None."""
    ctx = dash.callback_context
    if not ctx.triggered:
        return None
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    return SCENARIOS.get(button_id)


@app.callback(
    [Output("scenario-results", "children"),
     Output("property-analysis", "children"),
     Output("coc-comparison-chart", "figure"),
     Output("cash-flow-chart", "figure"),
     Output("optimization-opportunities", "children"),
     Output("risk-assessment", "children")],
    [Input(SARAH_BTN, "n_clicks"),
     Input(RISAHL_BTN, "n_clicks")]
)
def update_all(sarah_clicks, risahl_clicks):
    """Single callback that runs analysis once and updates all outputs."""
    scenario = _get_scenario_from_context()
    if scenario is None:
        return (
            html.P("Select a scenario to analyze"),
            html.P("Select a scenario to view property analysis"),
            go.Figure(),
            go.Figure(),
            html.P("Select a scenario to view optimization opportunities"),
            html.P("Select a scenario to view risk assessment"),
        )

    # Run analysis ONCE
    results = property_sourcer.analyze_scenario(scenario)

    # 1. Scenario results cards
    if results['properties_found'] == 0:
        scenario_results = dbc.Alert(
            f"No properties found meeting requirements for {scenario.name}",
            color="warning"
        )
        return (scenario_results, html.P("No properties found"), go.Figure(),
                go.Figure(), html.P("No properties found"), html.P("No properties found"))

    recs = results['recommendations']

    # --- Scenario Results ---
    cards = []
    for i, rec in enumerate(recs):
        cards.append(dbc.Card([
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
        ], className="mb-3"))

    # --- Property Analysis (top property) ---
    top = recs[0]
    scenario_cards = []
    for stype, data in top['scenarios'].items():
        scenario_cards.append(dbc.Card([
            dbc.CardHeader(stype.title() + " Scenario"),
            dbc.CardBody([
                html.P(f"Rent: ${data['rent']:,.0f}/month"),
                html.P(f"Expenses: ${data['expenses']:,.0f}/month"),
                html.P(f"CoC Return: {data['coc_return']:.1%}")
            ])
        ], className="mb-2"))

    property_analysis = dbc.Card([
        dbc.CardHeader("Detailed Property Analysis"),
        dbc.CardBody([
            html.H4(top['address']),
            html.Hr(),
            html.H5("Financial Summary"),
            dbc.Row([
                dbc.Col([
                    html.P(f"Purchase Price: ${top['purchase_price']:,.0f}"),
                    html.P(f"Down Payment: ${top['down_payment']:,.0f}"),
                    html.P(f"Total OOP: ${top['total_oop']:,.0f}")
                ], width=6),
                dbc.Col([
                    html.P(f"CoC Return: {top['coc_return']:.1%}"),
                    html.P(f"Monthly Cash Flow: ${top['monthly_cash_flow']:,.0f}"),
                    html.P(f"Risk Level: {top['risk_level']}")
                ], width=6)
            ]),
            html.Hr(),
            html.H5("Scenario Analysis"),
            dbc.Row([dbc.Col(card, width=4) for card in scenario_cards])
        ])
    ])

    # --- CoC Chart ---
    addresses = [rec['address'][:20] + "..." for rec in recs]
    coc_returns = [rec['coc_return'] * 100 for rec in recs]
    coc_fig = go.Figure(data=[go.Bar(
        x=addresses, y=coc_returns,
        text=[f"{coc:.1f}%" for coc in coc_returns], textposition='auto',
    )])
    coc_fig.update_layout(title="Cash-on-Cash Return Comparison",
                          xaxis_title="Properties", yaxis_title="CoC Return (%)", height=400)

    # --- Cash Flow Chart ---
    cash_flows = [rec['monthly_cash_flow'] for rec in recs]
    cf_fig = go.Figure(data=[go.Bar(
        x=addresses, y=cash_flows,
        text=[f"${cf:,.0f}" for cf in cash_flows], textposition='auto',
    )])
    cf_fig.update_layout(title="Monthly Cash Flow Comparison",
                         xaxis_title="Properties", yaxis_title="Monthly Cash Flow ($)", height=400)

    # --- Optimization & Risk (from already-computed underwriting result) ---
    uw_result = top['underwriting_result']
    opt_cards = []
    for opp in uw_result.optimization_opportunities:
        roi_text = f"ROI: {opp['roi']:.1%}" if opp['roi'] != float('inf') else "ROI: Infinite"
        opt_cards.append(dbc.Card([
            dbc.CardHeader(f"{opp['title']} ({opp['category']})"),
            dbc.CardBody([
                html.P(opp['description']),
                html.P(f"Investment: ${opp['investment']:,.0f}"),
                html.P(f"Annual Benefit: ${opp['annual_benefit']:,.0f}"),
                html.P(roi_text),
                html.P(f"Implementation Time: {opp['implementation_time']}"),
                html.P(f"Priority: {opp['priority']}"),
                html.P(f"Risk Level: {opp['risk_level']}")
            ])
        ], className="mb-2"))

    risk_card = dbc.Card([
        dbc.CardHeader("Risk Assessment"),
        dbc.CardBody([
            html.H5(f"Risk Level: {uw_result.risk_assessment['risk_level']}"),
            html.P(f"Risk Score: {uw_result.risk_assessment['risk_score']}"),
            html.Hr(),
            html.H6("Risk Factors:"),
            html.Ul([html.Li(f) for f in uw_result.risk_assessment['risk_factors']]),
            html.Hr(),
            html.H6("Mitigation Strategies:"),
            html.Ul([html.Li(s) for s in uw_result.risk_assessment['mitigation_strategies']])
        ])
    ])

    return cards, property_analysis, coc_fig, cf_fig, opt_cards, risk_card


if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0', port=8050)
