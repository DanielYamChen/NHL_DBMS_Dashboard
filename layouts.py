# Dash components, html, and dash tables
# import dash_core_components as dcc
from dash import dcc
# import dash_html_components as html
from dash import html
# import dash_table
from dash import dash_table

# Import Bootstrap components
import dash_bootstrap_components as dbc
import pandas as pd

# Import custom data.py
# import data

## import backend functions
import backend_functions

# Import data from data.py file
# teams_df = data.teams
# Hardcoded list that contain era names and marks
team_list = pd.read_csv('./data/Team.csv')
team_list = team_list['team_name'].values.tolist()
team_basic_info = {
    "team_abbrev": "MTL",
    "team_name": "Montreal Canadiens",
    "team_city": "Montreal - Quebec",
    "team_arena": "Bell Centre",
}
# era_list = data.era_list
# era_marks = data.era_marks

# team menu
team_menu = html.Div([
    dbc.Row(
        [
            dbc.Col(
                html.H4(
                    style={'text-align': 'center','justify-self': 'right'},
                    children='Select Team:'
                ),
                xs={'size':'auto', 'offset':0}, sm={'size':'auto', 'offset':0},
                md={'size':'auto', 'offset':3}, lg={'size':'auto', 'offset':0},
                xl={'size':'auto', 'offset':1}
            ),
            dbc.Col(
                dcc.Dropdown(
                    style={'text-align': 'center', 'font-size': '18px',
                           'width': '270px'},
                    id='team-dropdown',
                    options=team_list,
                    value=team_list[0],
                    clearable=False
                ),
                xs={'size':'auto', 'offset':0}, sm={'size':'auto', 'offset':0},
                md={'size':'auto', 'offset':0}, lg={'size':'auto', 'offset':0},
                xl={'size':'auto', 'offset':0}
            ),
        ],
        # form=True,
    ),
],className='menu')

# Layout for Team Information page
team_layout = html.Div([
    dbc.Row(dbc.Col(
        html.H1(
            children=html.B(children='Team Information')
        )
    )),
    dbc.Row(dbc.Col(
        html.Hr(),
    )),
    # Display Basic Information
    dbc.Row(dbc.Col(html.H2(children=html.B(children='Basic Information')))),
    dbc.Row(
        [dbc.Col(html.H4(
            id="team_abbrev",
            # children="Team Abbrev.: " + team_basic_info["team_abbrev"],
            children="Team Abbrev.: ",
        )),
        dbc.Col(html.H4(
            id="team_name",
            # children="Team name: " + team_basic_info["team_name"],
            children="Team name: ",
        ))],
        # justify="center",
    ),
    dbc.Row(
        [dbc.Col(html.H4(
            id="team_city",
            # children="Team city: " + team_basic_info["team_city"],
            children="Team city: ",
        )),
        dbc.Col(html.H4(
            id="team_arena",
            # children="Team arena: " + team_basic_info["team_arena"],
            children="Team arena: ",
        ))],
        # justify="center",
    ),
    dbc.Row(dbc.Col(html.Hr())),
    dbc.Row(dbc.Col(html.H2(children=html.B(children='Statistical Information')))),
    # Bar Charts of weight and height histograms
    dbc.Row(dbc.Col(html.H4(children='Weight distribution of team players'))),
    dbc.Row(dbc.Col(
        dcc.Graph(
            id='weight-hist',
            config={'displayModeBar': False}
        ),
        xs={'size': 12, 'offset': 0}, sm={'size': 12, 'offset': 0},
        md={'size': 12, 'offset': 0}, lg={'size': 12, 'offset': 0},
    )),
    dbc.Row(dbc.Col(html.H4(children='Height distribution of team players'))),
    dbc.Row(dbc.Col(
        dcc.Graph(
            id='height-hist',
            config={'displayModeBar': False}
        ),
        xs={'size': 12, 'offset': 0}, sm={'size': 12, 'offset': 0},
        md={'size': 12, 'offset': 0}, lg={'size': 12, 'offset': 0},
    )),
    # Line Charts of game score, penality minute, and ice time
    dbc.Row(dbc.Col(html.H4(children='Game score over years'))),
    dbc.Row(dbc.Col(
        dcc.Graph(
            id='game_score-line',
            config={'displayModeBar': False}
        ),
        xs={'size': 12, 'offset': 0}, sm={'size': 12, 'offset': 0},
        md={'size': 12, 'offset': 0}, lg={'size': 12, 'offset': 0},
    )),
    dbc.Row(dbc.Col(html.H4(children='Penalty minutes over years'))),
    dbc.Row(dbc.Col(
        dcc.Graph(
            id='penalty_minutes-line',
            config={'displayModeBar': False}
        ),
        xs={'size': 12, 'offset': 0}, sm={'size': 12, 'offset': 0},
        md={'size': 12, 'offset': 0}, lg={'size': 12, 'offset': 0},
    )),
    dbc.Row(dbc.Col(html.H4(children='Ice time over years'))),
    dbc.Row(dbc.Col(
        dcc.Graph(
            id='ice_time-line',
            config={'displayModeBar': False}
        ),
        xs={'size':12, 'offset':0}, sm={'size':12, 'offset':0},
        md={'size': 12, 'offset': 0},lg={'size': 12, 'offset': 0},
    )),
],className='app-page')

# Layout for Insert/Delete/Update/Display Player Data page
update_layout = html.Div([
    dbc.Form([
        dbc.Row([
            dbc.Col([dbc.Label("Player ID", html_for="player_id-input"),
                     dbc.Input(type="number", id="player_id-input",
                               placeholder="Enter player_id")],
                    # width=6,
            ),
            dbc.Col([dbc.Label("Season", html_for="season-input"),
                    dbc.Input(type="number", id="season-input",
                              placeholder="Enter season")],
                    # width=6,
            ),
            dbc.Col([dbc.Label("Player name", html_for="player_name-input"),
                    dbc.Input(type="text", id="player_name-input",
                              placeholder="Enter player_name")],
                    # width=6,
            ),
        ]),
        html.Br(),
        dbc.Row([
            dbc.Col([dbc.Label("Position", html_for="position-input"),
                     dbc.Input(type="text", id="position-input",
                               placeholder="Enter position")],
                    # width=6,
            ),
            dbc.Col([dbc.Label("Weight (lb)", html_for="weight-input"),
                    dbc.Input(type="number", id="weight-input",
                              placeholder="Enter weight in pounds")],
                    # width=6,
            ),
            dbc.Col([dbc.Label("Height (in)", html_for="height-input"),
                    dbc.Input(type="number", id="height-input",
                              placeholder="Enter height in inches")],
                    # width=6,
            ),
        ]),
        html.Br(),
        dbc.Row([
            dbc.Col([dbc.Label("Team Abbrev.", html_for="team_abbrev-input"),
                     dbc.Input(type="text", id="team_abbrev-input",
                               placeholder="Enter team_abbrev")],
            width=3,
            ),
        ]),
        
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col([
            dbc.Button("Insert", id="insert-button", color="primary",
                       className="me-1"),
            dbc.Button("Delete", id="delete-button", color="primary",
                       className="me-1"),
            dbc.Button("Update", id="update-button", color="primary",
                       className="me-1"),
            dbc.Button("Display", id="display-button", color="primary",
                       className="me-1"),
        ]),
        dbc.Col(html.P(id="form_state")),
    ]),
    dbc.Row(dbc.Col(
        html.Hr(),
    )),
    dbc.Row(dbc.Col(html.H2(children=html.B(id="update_status")))),
    dbc.Row(dbc.Col([
        html.H4(id="player_id-display"),
        html.H4(id="season-display"),
        html.H4(id="player_name-display"),
        html.H4(id="position-display"),
        html.H4(id="weight-display"),
        html.H4(id="height-display"),
        html.H4(id="team_abbrev-display"),
    ])),
], className='app-page')

# Layout for Basic/Advanced Player Stats page
player_info_layout = html.Div([
    dbc.Row(dbc.Col(
        html.H2(children=html.B(children='Basic or Advanced Player Stats'))
    )),
    dbc.Row(dbc.Col(
        html.Hr(),
    )),
    dbc.Form([
        dbc.Row([
            dbc.Col([dbc.Label("Season", html_for="stats_season-input"),
                     dbc.Input(type="number", id="stats_season-input",
                               placeholder="Enter season")],
            ),
            dbc.Col([dbc.Label("Basic/Advanced", html_for="b_or_a-dropdown"),
                    dcc.Dropdown(
                    style={'text-align': 'center', 'font-size': '18px',
                           'width': '270px'},
                    id='b_or_a-dropdown',
                    options=["Basic", "Advanced"],
                    clearable=False)]
            ),
            dbc.Col(html.P(id="b_or_a_form_state")),
            dbc.Col([dbc.Button("Look up", id="look_up-button", color="primary",
                                className="me-1")
            ])
        ])
    ]),
    html.Br(),
    dbc.Row(dbc.Col(
        dash_table.DataTable(
            id='player_info-table',
            style_as_list_view=True,
            editable=False,
            style_table={'overflowY': 'scroll',
                         'width': '100%', 'minWidth': '100%'},
            style_header={'backgroundColor': '#f8f5f0', 'fontWeight': 'bold'},
            style_cell={'textAlign': 'center', 'padding': '8px'},
        ),
        xs={'size':'auto', 'offset':0}, sm={'size':'auto', 'offset':0},
        md={'size':8, 'offset':0}, lg={'size':'auto', 'offset':0},
        xl={'size':'auto', 'offset':0}
    ), justify="center"),
], className='app-page')
