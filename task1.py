

import base64
import pickle
import pandas as pd
import webbrowser
import dash
import dash_html_components as html
import dash_core_components as dcc
import numpy as np
from dash.dependencies import State
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output 
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
import plotly.graph_objects as go
from pandas_datareader import data as web

import plotly 
import plotly.express as px
import plotly.io as pio
import dash_extensions as de
import plotly.graph_objects as go


# Declaring Global variables
# A variable declared outside a function is a global variable by default.



app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app = dash.Dash('project_name',external_stylesheets=[dbc.themes.SLATE])
url = "https://assets3.lottiefiles.com/packages/lf20_ss10xmcn.json"
url2 = "https://assets9.lottiefiles.com/packages/lf20_CYBIbn.json"
options = dict(loop=True, autoplay=True, rendererSettings=dict(preserveAspectRatio='xMidYMid slice'))
colors_g = {'background': '#DEC19B'}

#color identification
colors = {'background': '#ffffff',
          'bg_home': '#666666',
          'text': '#ffa500',
          'background_plot': '#cccccc',
          'text_plot': '#000000'}





#read balanced_reviews csv file by pandas framework
df = pd.read_csv('D:/Competitions_2020_2021/Apscript/task/data/balanced_reviews.csv')
(df.columns.tolist())

df['overall'].value_counts()

df.isnull().any(axis = 0)

df.isnull().any(axis = 1)

df[df.isnull().any(axis = 1)].tail()


#handling the missing data
df.dropna(inplace = True)


df['Positivity'] = np.where(df['overall'] > 3, 1, 0)

#defining labels and values for pie chart variables
labels = ['Positive', 'Negative']
values = [len(df[df.Positivity == 1]), len(df[df.Positivity == 0])]

#read generated csv file from etsy page by pandas framework
df1 = pd.read_csv('D:/Competitions_2020_2021/Apscript/task/data/Review_data.csv')
(df1.columns.tolist())

df1['Ratings'].value_counts()

df1.isnull().any(axis = 0)

df1.isnull().any(axis = 1)

df1[df1.isnull().any(axis = 1)].tail()


#handling the missing data
df1.dropna(inplace = True)


df1['Positivity'] = np.where(df1['Ratings'] > 3, 1, 0)

dff = df1  
box_style = dict(border='1px solid', margin='15px', padding='10px')
project_name = None


#loading the model function
def load_model():
    global df
    df = pd.read_csv('D:/Competitions_2020_2021/Apscript/task/data/balanced_reviews.csv')
  
    global pickle_model
    file = open("pickle_model.pkl", 'rb') 
    pickle_model = pickle.load(file)

    global vocab
    file = open("feature.pkl", 'rb') 
    vocab = pickle.load(file)
    
    print(df.sample(5))
    
    
#defining the funtion which holds the host address for platform
def open_browser():
    # Open the default web browser
    webbrowser.open_new('http://127.0.0.1:8050/')

def check_review(reviewText):

    #reviewText has to be vectorised, that vectorizer is not saved yet
    #load the vectorize and call transform and then pass that to model preidctor
    #load it later

    transformer = TfidfTransformer()
    loaded_vec = CountVectorizer(decode_error="replace",vocabulary=vocab)
    reviewText = transformer.fit_transform(loaded_vec.fit_transform([reviewText]))


    # Add code to test the sentiment of using both the model
    # [0] == negative   [1] == positive
    return pickle_model.predict(reviewText)

   


image_filename = 'D:/Competitions_2020_2021/Apscript/task/assets/computer.jpeg'

#defining the quality support sector

card_main = dbc.Card(
    [

        dbc.CardBody(
            [
                html.Div(de.Lottie(options=options, width="50%", height="50%", url=url)),
                html.H4("Check the customer review by our service with free of charge", className="card-title"),
                html.H6("Response", className="card-subtitle"),
                html.P(
                    "Give your reaction to our service if you don't mind!",
                    className="card-text",
                ),
                dcc.Dropdown(id='user_choice', options=[{'label': i, 'value': i} for i in df.overall.unique()],
                             value=5, clearable=False, style={"color": "#000000"}),
              
            ]
        ),
    ],
    color="success", 
    inverse=True,   # change color of text (black or white)
    outline=False,  # True = remove the block colors from the background and header
    className="mt-3"
)

#defining the app layout

def create_app_ui():
    # Create the UI of the Webpage here
    main_layout = html.Div(
             [
                 
                 
                dbc.Container([ html.Img(src=b64_image(image_filename),style={
                'height': '50%',
                'width': '50%'
            })],style={'textAlign': 'center'}),
           
            
            html.H1('Welcome!', style={'color': 'black','text-align': 'center' ,'background-image': 'url(https://s3.amazonaws.com/blog4.0/blog/wp-content/uploads/2018/04/customer-sentiment-analysis-tools.png)'})
                ,
        
        
        html.H1(children='Sentiment analyzing wizard', id='Main_title',style={'color': 'blue','text-align': 'center' }),
       
        dbc.Row(
            [
            html.H3('Random sentiment analysis summary vizualisation')
            ], justify="center", align="center"
            ),
        
        dbc.Row(
            [
            html.H5('Below results obtained by our model reviews.')
            ], justify="center", align="center"
            ),
                    

        
        dbc.Row(
            [
            html.H3('Check the service quality with your sample input ')
            ], justify="center", align="center"
            ),
        
        dbc.InputGroup(
            [
                dbc.InputGroupAddon("Look how good your review is!", addon_type="prepend"),
                dbc.Textarea(
                     id='textarea_review',
            placeholder='Enter the review here...',
            value='Enter review',
            style={'width': '100%', 'height': 100}
            ),
            ],
            className="mb-3",
        ),
         dbc.Row(
            [
            html.H3('Check the service quality with our sample input ')
            ], justify="center", align="center"
            ),
        dbc.Container([
                        dcc.Dropdown(
                    id='dropdown',
                    placeholder = 'Select a Review',
                    options=[{'label': i, 'value': i} for i in dff.Reviews.sample(81)],className='select_box',
                        
                        # {'label': 'New York City', 'value': 'NYC'},
                        # {'label': 'Montreal', 'value': 'MTL'},
                        # {'label': 'San Francisco', 'value': 'SF'}
                    value = dff.Reviews[0],
                    style = {'margin-bottom': '30px'}
                    
                )
                       ],
                        style = {'padding-left': '50px', 'padding-right': '50px'}
                        ),
       
    #butten
    dbc.Row(
        [
       dbc.Col(html.Div(
            dbc.Button(children='Show Review',id = 'show_review', n_clicks=0,style={
        'textAlign': 'center', 'color': colors['text']})),align="center"),
       
         ],style={'margin-bottom': '10px',
              'textAlign':'center',
              'width': '220px',
              'margin':'auto'}
        ),
           
       #text for review
    dbc.Row(
            [
            html.H3(children=None,id='result'),html.Br(),
            ], justify="center", align="center",style={'textAlign':'center','backgroundColor':'	#FA8072','margin-left':20,'margin-right':20}
            ),
    html.Br(),
    
    dbc.Row(
            [
            html.H3(children=None,id='result1'),html.Br(),
            ], justify="center", align="center",style={'textAlign':'center','backgroundColor':'	#87CEEB','margin-left':20,'margin-right':20}
            ),
    html.Div(
    [
        dbc.Button("Click me to see who is behind all this", id="alert-toggle-auto", className="mr-1"),
        html.Hr(),
        dbc.Alert(
            "Hello! We are MLgeeks,AI enthusiastic from little country called SriLanka!",
            id="alert-auto",
            is_open=True,
            duration=4000,
        ),
    ],style={'margin-bottom': '10px',
              'textAlign':'center',
              'width': '220px',
              'margin':'auto'}
),
    dbc.Row([dbc.Col(card_main, width=3)], justify="around"),
    html.Div(
    [dbc.Button("Submit", type='submit', outline=True, color="info", className="mr-1"),

     ],
    style={'margin-bottom': '10px',
              'textAlign':'center',
              'width': '220px',
              'margin':'auto'}
        )
    
    
    
        ])
        
        
    return main_layout

#defining the image function

def b64_image(image_filename):
    with open(image_filename, 'rb') as f: 
        image = f.read()
        return 'data:image/png;base64,' + base64.b64encode(image).decode('utf-8')
 
@app.callback(
    Output("alert-auto", "is_open"),
    [Input("alert-toggle-auto", "n_clicks")],
    [State("alert-auto", "is_open")],
)
def toggle_alert(n, is_open):
    if n:
        return not is_open
    return is_open
@app.callback(
    Output('result', 'children'),
    [
    Input('show_review', 'n_clicks')
    ],
    state=[State('textarea_review', 'value')]
    )



def update_app_ui(n_clicks,textarea_value):
    
    print("Data Type  = ", str(type(textarea_value)))
    print("Value      = ", str(textarea_value))

    
    result_list = check_review(textarea_value)
    
    if (result_list[0] == 0 and n_clicks > 0):
        result = 'user_input review : Negative'
    elif (result_list[0] == 1 and n_clicks > 0):
        result = 'user_input review : Positive'
    else:
        result = 'user_input review : Unknown'
    
    return result


@app.callback(
    Output('result1', 'children'),
    [
    Input('show_review', 'n_clicks')
    ],
    
    state=[ State('dropdown', 'value') ]
    )




def update_dropdown(n_clicks, value):
    result_list = check_review(value)
    
    if (result_list[0] == 0 and n_clicks > 0):
        result = 'dropdown result : Negative'
    elif (result_list[0] == 1 and n_clicks > 0):
        result = 'dropdown result : Positive'
    else:
        result = 'dropdown result : Unknown'
    
    
    return result

# Main Function to control the Flow of your Project
def main():
    load_model()    
    open_browser()


    global project_name
    project_name = "Sentiments Analysis with Insights" 
      
    global app
    app.layout = create_app_ui()
    app.title = project_name
 
    app.run_server() # debug=True
  
    print("This would be executed only after the script is closed")
    app = None
    project_name = None

if __name__ == '__main__':
    main()
