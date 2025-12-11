import tkinter as tk
from tkinter import messagebox
from inference_engine import load_rules, run_expert_system

def diagnose():
    try:
        # 1. Get Inputs from GUI
        user_data = {
            "age": float(entry_age.get()),
            "chol": float(entry_chol.get()),
            "trestbps": float(entry_bp.get()),
            "cp": float(entry_cp.get()),
            "exang": float(entry_exang.get()),
            "oldpeak": float(entry_oldpeak.get()),
            "ca": float(entry_ca.get())
        }
        
        # 2. Run Engine
        rules = load_rules("heart_rules.csv")
        final_facts, log = run_expert_system(user_data, rules)
        
        # 3. Show Result
        result_text = "--- Reasoning Steps ---\n" + "\n".join(log) + "\n\n"
        
        if "target" in final_facts:
            outcome = "HEART DISEASE DETECTED" if final_facts['target'] == 1 else "HEALTHY / NO DISEASE"
            color = "red" if final_facts['target'] == 1 else "green"
            result_text += f"FINAL DIAGNOSIS: {outcome}"
            lbl_result.config(fg=color)
        else:
            result_text += "Result: Inconclusive (No rule matched)"
            lbl_result.config(fg="black")
            
        lbl_result.config(text=result_text)
        
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers.")

# --- GUI SETUP ---
root = tk.Tk()
root.title("Heart Expert System")
root.geometry("450x600")

tk.Label(root, text="Cardiology Diagnosis Tool", font=("Arial", 14, "bold")).pack(pady=10)

# Input Fields
tk.Label(root, text="Age:").pack()
entry_age = tk.Entry(root)
entry_age.pack()

tk.Label(root, text="Cholesterol (chol):").pack()
entry_chol = tk.Entry(root)
entry_chol.pack()

tk.Label(root, text="Resting BP (trestbps):").pack()
entry_bp = tk.Entry(root)
entry_bp.pack()

tk.Label(root, text="Chest Pain Type (cp) [0-3]:").pack()
entry_cp = tk.Entry(root)
entry_cp.pack()

tk.Label(root, text="Exercise Induced Angina (exang) [0/1]:").pack()
entry_exang = tk.Entry(root)
entry_exang.pack()

tk.Label(root, text="ST Depression (oldpeak):").pack()
entry_oldpeak = tk.Entry(root)
entry_oldpeak.pack()

tk.Label(root, text="Major Vessels (ca) [0-4]:").pack()
entry_ca = tk.Entry(root)
entry_ca.pack()

# Button
tk.Button(root, text="Analyze Patient", command=diagnose, bg="lightblue").pack(pady=20)

# Output
lbl_result = tk.Label(root, text="Waiting for input...", justify="left", wraplength=400)
lbl_result.pack()

root.mainloop()