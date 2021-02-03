import pytest
import pandas as pd
from PySimul8.simulate import make_fr

df = pd.DataFrame(dict(index=['demand','price','sales','cost','expenses','cash'],year1=[0,10,0,0,0,0],year2=[0,10,0,0,0,0],year3=[0,10,0,0,0,0],year4=[0,10,0,0,0,0]))
df.set_index('index',inplace=True)
q = "select demand,price,demand*price as sales, cost ,demand*cost as expenses, (demand*price)-(demand*cost) as cash from df"
fr = make_fr(data=df,
             number_of_simulations= 10000,
             feature_to_simulate= 'cash',
             sql_query= q,
             calculate_NPV_IRR= True,
             Required_Rate= 0.20,
             Initial_investment= -500)

def test_simulations():
    """
    To check the number of simulations
    """
    assert fr.number_of_simulations == 10000
    
def test_feature_to_simulate():
    """
    To check the feature to simulate
    """
    assert fr.feature_to_simulate == 'cash'
    
def test_query():
    """
    To check the query
    """
    assert fr.query == q
    
def test_NPV_IRR():
    """
    To check the NPV and IRR parameter
    """
    assert fr.calculate_NPV_IRR == True
    
def test_req_rate():
    """
    To check the required rate
    """
    assert fr.Required_Rate == 0.20
    
def test_investment():
    """
    To check the initial investement
    """
    assert fr.Initial_investment == -500
