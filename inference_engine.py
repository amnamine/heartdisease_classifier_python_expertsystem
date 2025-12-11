import pandas as pd

def load_rules(filename="heart_rules.csv"):
    return pd.read_csv(filename)

def check_condition(user_val, operator, rule_val):
    """Helper to handle >, <, == logic"""
    if str(rule_val) == "None": return True # Condition ignored
    
    # Convert numbers if possible
    try:
        user_val = float(user_val)
        rule_val = float(rule_val)
    except:
        pass # Keep as strings

    if operator == ">": return user_val > rule_val
    if operator == "<": return user_val < rule_val
    if operator == "<=": return user_val <= rule_val
    if operator == ">=": return user_val >= rule_val
    if operator == "==": return user_val == rule_val
    return False

def run_expert_system(inputs, rules_df):
    """
    inputs: Dict (e.g., {'age': 60, 'chol': 250})
    rules_df: The loaded pandas dataframe
    """
    facts = inputs.copy()
    trace = [] # Log of what happened
    
    loop = True
    while loop:
        loop = False # Stop if no new facts are learned
        for idx, rule in rules_df.iterrows():
            # Check Condition 1
            cond1 = check_condition(facts.get(rule['Cond1']), rule['Op1'], rule['Val1'])
            
            # Check Condition 2
            cond2 = True
            if str(rule['Cond2']) != "None":
                cond2 = check_condition(facts.get(rule['Cond2']), rule['Op2'], rule['Val2'])
            
            # If both True, Fire Rule
            if cond1 and cond2:
                res_attr = rule['Result_Attr']
                res_val = rule['Result_Val']
                
                # If we learned a NEW fact, add it and repeat loop
                if res_attr not in facts:
                    facts[res_attr] = res_val
                    trace.append(f"Rule {rule['RuleID']} fired: {res_attr} = {res_val}")
                    loop = True 
                    
    return facts, trace