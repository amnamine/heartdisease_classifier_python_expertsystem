import pandas as pd
from inference_engine import load_rules, run_expert_system

def calculate_metrics(y_true, y_pred):
    tp = 0 # True Positive
    tn = 0 # True Negative
    fp = 0 # False Positive
    fn = 0 # False Negative
    unclassified = 0

    for true, pred in zip(y_true, y_pred):
        if pred == -1: # No Rule Matched
            unclassified += 1
            continue
            
        if true == 1 and pred == 1: tp += 1
        elif true == 0 and pred == 0: tn += 1
        elif true == 0 and pred == 1: fp += 1
        elif true == 1 and pred == 0: fn += 1

    # Metrics Math
    total = tp + tn + fp + fn
    accuracy = (tp + tn) / total if total > 0 else 0
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    return {
        "TP": tp, "TN": tn, "FP": fp, "FN": fn, "Unclassified": unclassified,
        "Accuracy": accuracy, "Precision": precision, "Recall": recall, "F1_Score": f1
    }

def main():
    print("Loading data...")
    df = pd.read_csv("heart.csv")
    rules = load_rules("heart_rules.csv")
    
    y_true = []
    y_pred = []
    
    print(f"Running Expert System on {len(df)} patients...")
    
    for index, row in df.iterrows():
        # Prepare input data
        patient_data = row.to_dict()
        
        # Run System
        facts, _ = run_expert_system(patient_data, rules)
        
        # Get Truth and Prediction
        y_true.append(int(row['target']))
        
        if 'target' in facts:
            y_pred.append(int(facts['target']))
        else:
            y_pred.append(-1) # Inconclusive

    m = calculate_metrics(y_true, y_pred)

    print("\n" + "="*40)
    print("   HEART DISEASE SYSTEM REPORT")
    print("="*40)
    print(f"Total Processed: {len(df)}")
    print(f"Unclassified:    {m['Unclassified']}")
    print("-" * 40)
    print(f"TP (Sick->Sick):      {m['TP']}")
    print(f"TN (Healthy->Healthy):{m['TN']}")
    print(f"FP (Healthy->Sick):   {m['FP']}")
    print(f"FN (Sick->Healthy):   {m['FN']}")
    print("-" * 40)
    print(f"ACCURACY:  {m['Accuracy']:.2%}")
    print(f"PRECISION: {m['Precision']:.2%}")
    print(f"RECALL:    {m['Recall']:.2%}")
    print(f"F1 SCORE:  {m['F1_Score']:.4f}")
    print("="*40)

if __name__ == "__main__":
    main()