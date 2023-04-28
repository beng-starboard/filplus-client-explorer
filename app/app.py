from dash import Dash, html, dash_table, dcc, callback, Output, Input
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

# Name mapping
metric_map = {
    'c_owner_verified_deal_concentration': 'Concentration of verified deals (%)',
    'c_notary_datacap_alloc_concentration': 'Concentration of notary allocation (%)',
    'c_total_datacap_received': 'Total datacap received (TiB)',
    'c_total_datacap_used': 'Total datacap used (TiB)',
    'c_datacap_utilization_rate': 'Datacap used (%)',
    'c_max_single_provider_datacap_spent': 'Max datacap spend on an SP',
    'c_max_single_notary_datacap_received': 'Max datacap received from notary',
    'c_top3_provider_datacap_spent': 'Datacap spent on top 3 SPs',
    'c_top3_notary_datacap_received': 'Datacap received from top 3 notaries',
    'c_top3_provider_concentration_verified': 'Concentration of verified in top 3 SPs (%)',
    'c_top3_notary_concentration': 'Concentration of datacap from top 3 notaries (%)',
    'c_top5_provider_concentration_verified': 'Concentration of verified in top 5 SPs (%)',
    'c_top5_notary_concentration': 'Concentration of datacap from top 5 notaries (%)',
    'c_verified_deal_duration_avg': 'Avg. duration of verified deals (days)',
    'c_verified_deal_duration_std': 'Stdev. duration of verified deals (days)',
    'c_avg_price_per_epoch_per_unit_verified': 'Price per epoch per verified',
    'c_frac_paid_verified_deals': 'Proportion of verified deals paid (%)',
    'c_verified_deal_frequency': 'Verified deal frequency',
    'c_datacap_to_deal_timelapse_min': 'Min. time from allocation to deal',
    'c_datacap_to_deal_timelapse_avg': 'Avg. time from allocation to deal',    
}

# Pull data
df = pd.read_csv('assets/filplus_data.csv', index_col=[0])
df_full = df.copy()
selected_columns = [dfc for dfc in df.columns if dfc[0:2] == 'c_']
selected_columns.insert(0, 'stat_date')
selected_columns.insert(1, 'client_id')

selected_columns_percentile = [dfc for dfc in df.columns if dfc[0:2] == 'p_']
selected_columns_percentile.insert(0, 'stat_date')
selected_columns_percentile.insert(1, 'client_id')

# Format the data
dfp = df[selected_columns_percentile]
df = df[selected_columns]
selected_features = selected_columns[2:]
df.style.format("{:.4f}")

df['c_owner_verified_deal_concentration'] = np.round(df['c_owner_verified_deal_concentration']*100, 1)
df['c_notary_datacap_alloc_concentration'] = np.round(df['c_notary_datacap_alloc_concentration']*100,1)
df['c_top3_provider_concentration_verified'] = np.round(df['c_top3_provider_concentration_verified']*100,1)
df['c_top3_notary_concentration'] = np.round(df['c_top3_notary_concentration']*100,1)
df['c_top5_provider_concentration_verified'] = np.round(df['c_top5_provider_concentration_verified']*100,1)
df['c_top5_notary_concentration'] = np.round(df['c_top5_notary_concentration']*100,1)
df['c_frac_paid_verified_deals'] = np.round(df['c_frac_paid_verified_deals']*100,1)
df['c_datacap_utilization_rate'] = np.round(df['c_datacap_utilization_rate']*100,1)
df['c_verified_deal_duration_avg'] = np.round(df['c_verified_deal_duration_avg']/2880,1)
df['c_verified_deal_duration_std'] = np.round(df['c_verified_deal_duration_std']/2880,1)
df[['c_total_datacap_received', 'c_total_datacap_used', 'c_max_single_provider_datacap_spent', 'c_max_single_notary_datacap_received', 'c_top3_provider_datacap_spent', 'c_top3_notary_datacap_received']] = np.round(df[['c_total_datacap_received', 'c_total_datacap_used', 'c_max_single_provider_datacap_spent', 'c_max_single_notary_datacap_received', 'c_top3_provider_datacap_spent', 'c_top3_notary_datacap_received']]/2**40,1)

external_stylesheets = [dbc.themes.CERULEAN, dbc_css]
app = Dash(__name__, external_stylesheets=external_stylesheets, title='Fil+ Client Metric Explorer')
app.title = 'Fil+ Client Metric Explorer'
server = app.server

app.layout = dbc.Container([

    dbc.Row([
        html.Div('FIL+ Client Metric Explorer', className="text-primary text-center fs-3", style={'paddingBottom':'10px'})
    ]),

    dbc.Row([
        dbc.Col([
            html.Div('Client')
        ]),

        dbc.Col([
            html.Div('Metric')
        ])
    ]),

    dbc.Row([

        dbc.Col([
            dcc.Dropdown(
                df.client_id.unique(),
                value=df.client_id.iloc[0],
                id = 'client-search'
            )
        ]),

        dbc.Col([
            dcc.Dropdown(
                selected_features,
                value='c_owner_verified_deal_concentration',
                id = 'controls-and-radio-item'
            )
        ])

    ]),

    dbc.Row([
        html.Div(style={'padding-top':'10px'})
    ]),

    dbc.Row([
        dbc.Col([
            html.Div(
                dash_table.DataTable(
                    id = 'client_view',
                    data=df.to_dict('records'),
                    cell_selectable = False,
                    style_cell={
                        "fontFamily": '-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,"Noto Sans",sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji"',
                        'fontWeight': '400',
                        'lineHeight': '1.1',
                        'fontSize': '0.75em',
                        'color': '#212529',
                        'textAlign': 'left',
                        'whiteSpace': 'normal',
                        'height': 'auto',
                        'padding':'0.3rem',
                        'border': '0 px',
                        'verticalAlign': 'top',
                    },
                    style_header = {
                        'fontWeight': 'bold'
                    },
                    style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': '#f8f9fa',
                    }],

                ),
                className="dbc dbc-row-selectable"
            )
        ]),

        dbc.Col([
            html.Div(
                dcc.Graph(
                    figure = {},
                    id = 'controls-and-graph'
                ),
                # className="col-8"
            )
        ]),

    ]),

    dbc.Row([
        html.Div('Last updated %s' % (df.stat_date.max()), style={'paddingTop':'10px', 'fontSize':'0.6em'})
    ])

    # dbc.Row([
    #     html.Div(style={'padding-top':'20px'})
    # ]),


    # dbc.Row([
    #     html.Div('Full data table', className="text-primary text-center fs-3")
    # ]),

    # dbc.Row([
    #     html.Div(style={'padding-top':'10px'})
    # ]),


    # dbc.Row([
    #     dash_table.DataTable(
    #         data=df_full.to_dict('records'), 
    #         style_table={'overflowX': 'auto'},
    #         page_size=10,
    #         cell_selectable = False,
    #         style_cell={
    #             "fontFamily": '-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,"Noto Sans",sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji"',
    #             'fontWeight': '400',
    #             'lineHeight': '1.1',
    #             'fontSize': '0.75em',
    #             'color': '#212529',
    #             'textAlign': 'left',
    #             'whiteSpace': 'normal',
    #             'height': 'auto',
    #             'padding':'0.3rem',
    #             'border': '0 px',
    #             'verticalAlign': 'top',
    #         },
    #         style_data_conditional=[
    #         {
    #             'if': {'row_index': 'odd'},
    #             'backgroundColor': '#f8f9fa'
    #         }],

    #     ),
    # ])

])


@callback(
    Output(component_id='controls-and-graph', component_property='figure'),
    Input(component_id='controls-and-radio-item', component_property='value'),
    Input(component_id='client-search', component_property='value')
)
def update_histogram(selected_col, selected_client):
    fig = px.histogram(df, x=selected_col, height=500, width=600)

    current_value = df[df.client_id==selected_client][selected_col].iloc[0]

    fig.add_trace(
        go.Scatter(
            x = [current_value, current_value], 
            y = [1, len(df)],
        )        
    )

    fig.data[-1].name = '%s: %s' %(selected_col, current_value)
    fig.update_layout(showlegend=False)

    return fig

@callback(
    Output(component_id='client_view', component_property='data'),
    Input(component_id='client-search', component_property='value')        
)
def update_client_table(selected_client):
    df_selected = df[df.client_id == selected_client]
    df_selected_percentile = dfp[df.client_id == selected_client]
    df_selected = df_selected.T.reset_index().iloc[2:]
    df_selected_percentile = df_selected_percentile.T.reset_index()
    df_selected.columns = ['Metric', 'Value']
    df_selected['Percentile'] = df_selected_percentile[df_selected_percentile.columns[-1]]

    # Give the columns readable names
    df_selected['Metric'] = df_selected.Metric.replace(metric_map)
    df_selected['Value'].iloc[-1] = str(df_selected['Value'].iloc[-1])[0:5]
    df_selected['Value'].iloc[-2] = str(df_selected['Value'].iloc[-2])[0:5]
    df_selected['Value'].iloc[-3] = str(df_selected['Value'].iloc[-3])[0:5]    

    return df_selected.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)
