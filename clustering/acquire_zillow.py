from env import host, password, user, get_connection
import pandas as pd

# Open a connection to a mySQL database. The name of the database should be the input to this function. 
# Make sure your database credentials are not included in this file.
def zillow_connection(database_name='zillow'):
    """Grabs zillow data from MySQL. Input is db name, output is db connection."""
    return get_connection(database_name)


# Query the zillow database and return a several dataframes:
    # the properties data from 2016 and 2017
        # information to include: all fields related to the properties that are available; 
        # however, for those id variables that have a reference table that holds the description, 
        # such as airconditioningtypeid and the table aircondintiontype, 
        # include the descriptions of those fields but do not include the id column in your output. 
        # That is, you would include airconditioningtypedesc and not airconditioningtypeid. 
        # (You will end up using all the tables in the database). Be sure to do the correct join. 
        # We do not want to eliminate properties purely because they may have a null value for airconditioningtypeid
def grab_zillow_data():
    """Returns two DataFrames for 2016 and 2017 properties. The DataFrames will include logerror and related descriptions \
    for id fields."""
    dbc = zillow_connection('zillow')
    prop_sixteen = pd.read_sql('SELECT * FROM properties_2016 psix \
                                RIGHT JOIN predictions_2016 preds ON psix.parcelid = preds.parcelid\
                                LEFT JOIN airconditioningtype ac ON psix.airconditioningtypeid = ac.airconditioningtypeid \
                                LEFT JOIN architecturalstyletype ast ON psix.architecturalstyletypeid = ast.architecturalstyletypeid \
                                LEFT JOIN buildingclasstype bct ON psix.buildingclasstypeid = bct.buildingclasstypeid \
                                LEFT JOIN heatingorsystemtype hst ON psix.heatingorsystemtypeid = hst.heatingorsystemtypeid \
                                LEFT JOIN propertylandusetype plut ON psix.propertylandusetypeid = plut.propertylandusetypeid \
                                LEFT JOIN storytype st ON psix.storytypeid = st.storytypeid \
                                LEFT JOIN typeconstructiontype tct ON psix.typeconstructiontypeid = tct.typeconstructiontypeid',dbc)
    prop_seventeen = pd.read_sql('SELECT * FROM properties_2017 psev \
                                RIGHT JOIN predictions_2017 preds ON psev.parcelid = preds.parcelid\
                                LEFT JOIN airconditioningtype ac ON psev.airconditioningtypeid = ac.airconditioningtypeid \
                                LEFT JOIN architecturalstyletype ast ON psev.architecturalstyletypeid = ast.architecturalstyletypeid \
                                LEFT JOIN buildingclasstype bct ON psev.buildingclasstypeid = bct.buildingclasstypeid \
                                LEFT JOIN heatingorsystemtype hst ON psev.heatingorsystemtypeid = hst.heatingorsystemtypeid \
                                LEFT JOIN propertylandusetype plut ON psev.propertylandusetypeid = plut.propertylandusetypeid \
                                LEFT JOIN storytype st ON psev.storytypeid = st.storytypeid \
                                LEFT JOIN typeconstructiontype tct ON psev.typeconstructiontypeid = tct.typeconstructiontypeid',dbc)
    # logerror_sixteen = pd.read_sql('SELECT * FROM predictions_2016', dbc)
    # logerror_seventeen = pd.read_sql('SELECT * FROM predictions_2017', dbc)
    # prop_sixteen.drop(['airconditioningtypeid', 'architecturalstyletypeid', 'buildingclasstypeid', 'heatingorsystemtypeid', 'propertylandusetypeid', 'storytypeid', 'typeconstructiontypeid', 'Unnamed: 0', 'id', 'id.1', 'parcelid.1', 'parcelid.2'], axis=1, inplace=True)
    # prop_seventeen.drop(['airconditioningtypeid', 'architecturalstyletypeid', 'buildingclasstypeid', 'heatingorsystemtypeid', 'propertylandusetypeid', 'storytypeid', 'typeconstructiontypeid', 'Unnamed: 0', 'id', 'id.1', 'parcelid.1', 'parcelid.2'], axis=1, inplace=True)
    properties = pd.concat([prop_sixteen, prop_seventeen])
    properties.drop(['airconditioningtypeid', 'architecturalstyletypeid', 'buildingclasstypeid', 'heatingorsystemtypeid', 'propertylandusetypeid', 'storytypeid', 'typeconstructiontypeid', 'id'], axis=1, inplace=True)
    return properties

    # the logerror for the properties from 2016 and 2017




# Saves the dataframes as csv files locally
def make_csv(df, file_name):
    """Creates local csv of inputted DataFrames."""
    df.to_csv(file_name, sep='\t')

