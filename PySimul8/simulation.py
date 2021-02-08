# Module: Financial Data Simulation
# Authors: Abhimanyu Anand <abhimanyu7296@gmail.com>, Fahad Akbar <m.akbar@queensu.ca>
# License: MIT


##################################################################################################################################################################################

#importing libraries
import numpy as np
import pandas as pd
import pandasql as ps
import numpy_financial as npf
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# _______________________________________________________________________________________________________________________


class simulator():

   '''
    - This will try to simulate the values of different metrics/feature financial data, like cash, NPV (Net Present Value), IRR (Internal Rate of Return) values etc..
    - This can also create simulations for data belonging to different distributions like unifrom, normal, lognormal etc..
  '''

  def __init__(self,data,number_of_simulations,feature_to_simulate,sql_query,calculate_NPV_IRR=False,Required_Rate=None,Initial_investment=None):
    '''
    User to define the feature to simulate variable
      args:
                         data: pandas dataframe, pass in the dataframe with columns to simulate upon
        number_of_simulations: integer, the number of itreations to run simulations for a specific feature
          feature_to_simulate: string, name of feature column to generate simulation for.
                    sql_query: string, provide a sql query to create calculate fields like sales from demand and price values,
            calculate_NPV_IRR: boolean, provide a boolean value, for deciding whether to create NPR or IRR values, default False, when False NPV and IRR values will not be calculated
                Required_Rate: integer, provide the required rate value for calculating NPV and IRR values, default None, when None NPV and IRR values will not be calculated
           Initial_investment: integer, provide initial investment value to be added to cah values for simulation, default None, when None 0 will be added to cash simulation values.
  '''
    
    self.data = data.transpose()
    self.pd = data.shape[1]
    self.number_of_simulations = number_of_simulations
    self.query = sql_query
    self.feature_to_simulate = feature_to_simulate
    self.all_random_numbers = {}
    self.calculate_NPV_IRR = calculate_NPV_IRR
    self.Required_Rate = Required_Rate

    if Initial_investment < 0:
      self.Initial_investment = Initial_investment
    else:
      self.Initial_investment = Initial_investment * -1.0

    return(None)

  # normal distribution
  def NDist(self,**details):
    """
    To calculate the simulation of norammlly distributed variable
    Args: 
      Provide variable name , mean & std
      e.g.:
        demand = [50,5]
        temperature = [20,2]
    Returns:
        list 
    """
    self.n_details = details
    self.ND = {}

    for d in details:
      col = np.random.normal(details[d][0],details[d][1],(self.number_of_simulations,self.pd)) # self.pd is numbers of years (columns)
      self.ND.update({d:col})

    # update the global dict
    self.all_random_numbers.update(self.ND)
    return(self.ND)

  # log normal distribution
  def LnDist(self,**details):
    """
    To calculate the simulation of log norammlly distributed variable
    Args: 
      Provide variable name , mean & std
      e.g.:
        share price = [50,5]
        rainfall = [20,2]
    Returns:
        list 
    """
    self.n_details = details
    self.LnD = {}

    for d in details:
      col = np.random.lognormal(details[d][0],details[d][1],(self.number_of_simulations,self.pd)) 
      self.LnD.update({d:col})

    # update the global dict
    self.all_random_numbers.update(self.LnD)
    return(self.LnD)

  #triangle distribution
  def TriDist(self,**details):
    """
    To calculate the simulation of a variable following triangle distribution
    Args: 
      Provide variable name , lowest value, most likely value & maximum value
      e.g.:
        demand = [10,100,250]
        temp = [-10,18,40]
    Returns:
        list 
    """
    self.t_details = details
    self.TD = {}
    for d in details:
      col = np.random.triangular(details[d][0],details[d][1],details[d][2],(self.number_of_simulations,self.pd))
      self.TD.update({d:col})
    
    # update the global dict
    self.all_random_numbers.update(self.TD)
    return(self.TD)
  
  # poisson distribution
  def PDist(self,**details):
    """
    To calculate the simulation of a variable following poisson distribution
    Args: 
      Provide variable name , lambda
      e.g.:
        Daily portfolio loss below 5% = [50]
        Number of births per hour during a given day = [20]
    Returns:
        list 
    """
    self.n_details = details
    self.PD = {}

    for d in details:
      col = np.random.poisson(details[d][0],(self.number_of_simulations,self.pd))
      self.PD.update({d:col})

    # update the global dict
    self.all_random_numbers.update(self.PD)
    return(self.PD)

  # exponential distribution
  def EDist(self,**details):
    """
    To calculate the simulation of a variable following exponential distribution
    Args:
      Provide variable name , lambda
      e.g.:
        amount of time until an earthquake occurs = [50]
        length business telephone calls = [20]
    Returns:
        list 
    """
    self.n_details = details
    self.ED = {}

    for d in details:
      col = np.random.exponential(details[d][0],(self.number_of_simulations,self.pd))
      self.ED.update({d:col})

    # update the global dict
    self.all_random_numbers.update(self.ED)
    return(self.ED)

  # binomial distribution
  def BDist(self,**details):
    """
    To calculate the simulation of a variable following binomial distribution
    Args:
      Provide variable name , number of trials, probability of success
      e.g.:
        druug works or not = [50, 0.4]
        win a lottery or not = [20, 0.3]
    Returns:
        list 
    """
    self.n_details = details
    self.BD = {}

    for d in details:
      col = np.random.binomial(details[d][0],details[d][1],(self.number_of_simulations,self.pd))
      self.BD.update({d:col})

    # update the global dict
    self.all_random_numbers.update(self.BD)
    return(self.BD)

  # unifrom distribution
  def UDist(self,**details):
    """
    To calculate the simulation of a variable following unifrom distribution
    Args:
      Provide variable name , low, high
      e.g.:
        coin toss = [0, 1]
        deck of cards = [0, 13]
    Returns:
        list 
    """
    self.n_details = details
    self.UD = {}

    for d in details:
      col = np.random.uniform(details[d][0],details[d][1],(self.number_of_simulations,self.pd))
      self.UD.update({d:col})

    # update the global dict
    self.all_random_numbers.update(self.UD)
    return(self.UD)


  def simulate(self):
   """
    To generate the simulated data for the target feature
    To calculate the NPV/IRR value if calculate_NPV_IRR is set to True
    Returns:
        list 
    """
  
    copy_data = self.data.copy()
 
    self.full_data = []
    self.feature_only_sum = []
    self.NPV = []
    self.IRR =[]

   
    for i in range(self.number_of_simulations):

      # get the random number for the current i
      for k,v in zip(self.all_random_numbers.keys(),self.all_random_numbers.values()):
        #print(k,v[i])
        copy_data[k] = v[i]
        copy_data_updated = copy_data.copy()

      # once we have all the random numbers in place, we need to apply the sql formulas
      data_index  = self.data.index
      df = copy_data_updated.reset_index(drop=True)
      df_refreshed = ps.sqldf(self.query,locals())

      # now check if we need to calculate NPV/IRR or a simple sum 
      if (self.Required_Rate is not None) & (self.calculate_NPV_IRR == True) & (self.Initial_investment is not None):
        # add initial investment to the cash
        c = list(df_refreshed[self.feature_to_simulate])
        c.insert(0,self.Initial_investment)

        #calculate npv
        npv = npf.npv(self.Required_Rate,c)
        self.NPV.append(npv)

        #calculate irr
        irr = npf.mirr(c,self.Required_Rate,self.Required_Rate)
        self.IRR.append(irr)
      
      # now calculate the sum of all the cash
      if self.Initial_investment is None:
        cash = np.sum(df_refreshed[self.feature_to_simulate])
      else:
        cash = self.Initial_investment + np.sum(df_refreshed[self.feature_to_simulate])
      # add to list
      self.feature_only_sum.append(cash)

      # now save the full data frame
      self.full_data.append(df_refreshed)

    min_irr = np.min([i for i in self.IRR if i is not np.nan])
    self.IRR = [min_irr if np.isnan(x) else x for x in self.IRR]
    return(self.full_data)
   
  
  def visualize(self, visualize_on = 'feature_only_sum'):
     """
    To visualize the simulated data
    Displays the cumulative probability of the values via a histogram
    Args:
      visualize_on: string, name of the feature/column to display
    Returns:
      None
    """
    
    # selecting which value to visualize
    x_val = ""
    if visualize_on.upper() == 'IRR':
      x_val = self.IRR
      visualize_on = "IRR for "
    elif visualize_on.upper() == 'NPV':
      x_val = self.NPV
      visualize_on = "NPV for "
    else:
      x_val = self.feature_only_sum
      visualize_on = ""

    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(
      go.Histogram(name='%s%s count' % (visualize_on,self.feature_to_simulate), x= x_val 
      ),
      secondary_y=False,
    )
    fig.add_trace(
      go.Histogram(name = 'Cumulative probability of %s %s' % (visualize_on,self.feature_to_simulate), x = x_val,histnorm='probability',
                   cumulative={'enabled':True, 'direction': 'increasing','currentbin':'include'}, opacity= 0.5,
                   hoverlabel = dict(namelength = -1), marker=dict(color='mediumseagreen')
                   ),
                   secondary_y=True,)

    # updating layout
    fig.update_layout(
      title_text="<b>Distribution of %s%s values</b>" % (visualize_on,self.feature_to_simulate),
      title_x=0.43,
      template = 'simple_white',
      yaxis = {'showspikes' : True}
    )

    # Set x-axis title
    fig.update_xaxes(title_text="<b>%s%s values</b>" % (visualize_on,self.feature_to_simulate))

    # Set y-axes titles
    fig.update_yaxes(title_text="<b>Count of %s%s values </b>" % (visualize_on,self.feature_to_simulate), secondary_y=False)
    fig.update_yaxes(title_text= "<b>Cumulative probability of %s%s values</b>" % (visualize_on,self.feature_to_simulate), secondary_y=True)
    fig.show()
