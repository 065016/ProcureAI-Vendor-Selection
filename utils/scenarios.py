from .scoring import score_vendors,scenario_weights,DEFAULT_WEIGHTS
def run_scenario(df,name):
 a=score_vendors(df,DEFAULT_WEIGHTS); b=score_vendors(df,scenario_weights(name))
 m=a[["Vendor_ID","Vendor_Name","Rank","Overall_Score"]].merge(b[["Vendor_ID","Rank","Overall_Score"]],on=["Vendor_ID","Vendor_Name"],suffixes=("_Original","_Scenario"))
 m["Rank_Change"]=m.Rank_Original-m.Rank_Scenario; m["Score_Change"]=(m.Overall_Score_Scenario-m.Overall_Score_Original).round(2); return m.sort_values("Rank_Scenario")
