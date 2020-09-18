# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 21:45:24 2020

@author: Daniel Tan
"""


from src.utils import AttributeDict
from src.awbw import findUnitsInRangeOf

def main():
    client_obj = AttributeDict.from_json_file('clientObj.json')        
    base_damage_values= AttributeDict.from_json_file('assets/baseDamageValues.json')
    
    print(f"Unit ids present: {client_obj.units.keys}")
    
    # Arbitrarily pick a unit
    unit = client_obj.units[77164577]
    x = unit.units_x
    y = unit.units_y
    
    
    #print(client_obj.buildings.keys)
    #print(6 in client_obj.buildings)
    units_in_range = findUnitsInRangeOf(x,y,unit,client_obj, base_damage_values)
    print(units_in_range)
    
if __name__ == "__main__":
    main()