import pandas as pd, numpy as np
DEFAULT_WEIGHTS={"Cost":25.0,"Quality":25.0,"Lead Time":15.0,"On-Time Delivery":15.0,"Defect Rate":10.0,"Sustainability":10.0}
CRITERIA={"Cost":("Unit_Cost","lower"),"Quality":("Quality_Score","higher"),"Lead Time":("Lead_Time_Days","lower"),"On-Time Delivery":("On_Time_Delivery_Percentage","higher"),"Defect Rate":("Defect_Rate","lower"),"Sustainability":("Sustainability_Score","higher")}
def validate_weights(w): return abs(sum(w.values())-100)<1e-9,sum(w.values())
def normalize(s,d):
 s=pd.to_numeric(s,errors="coerce"); lo,hi=s.min(),s.max()
 if hi==lo:return pd.Series(1.0,index=s.index)
 return ((s-lo)/(hi-lo)) if d=="higher" else ((hi-s)/(hi-lo))
def score_vendors(df,weights=None):
 w=weights or DEFAULT_WEIGHTS; ok,total=validate_weights(w)
 if not ok: raise ValueError(f"Weights must sum to 100%. Current total: {total:.2f}%")
 o=df.copy(); total_s=pd.Series(0.0,index=o.index)
 for k,(col,d) in CRITERIA.items():
  n=normalize(o[col],d); o[f"{k}_Score"]=n*100; o[f"{k}_Contribution"]=n*w[k]; total_s+=o[f"{k}_Contribution"]
 o["Overall_Score"]=total_s.round(2); o=o.sort_values(["Overall_Score","Quality_Score"],ascending=[False,False]).reset_index(drop=True); o["Rank"]=range(1,len(o)+1)
 o["Recommendation"]=pd.cut(o["Overall_Score"],[-np.inf,50,65,80,np.inf],labels=["Not Recommended","Conditional","Recommended","Highly Recommended"],right=False)
 r=(100-o["Financial_Risk_Score"])*.3+(100-o["Supply_Risk_Score"])*.3+(100-o["Geopolitical_Risk_Score"])*.2+(100-o["Business_Continuity_Score"])*.2
 o["Risk_Score"]=r.round(2); o["Risk_Level"]=pd.cut(o["Risk_Score"],[-np.inf,25,50,np.inf],labels=["Low","Medium","High"],right=False)
 return o
def scenario_weights(n):
 return {"Cost Optimization":{"Cost":45,"Quality":15,"Lead Time":10,"On-Time Delivery":10,"Defect Rate":10,"Sustainability":10},"Quality First":{"Cost":10,"Quality":45,"Lead Time":10,"On-Time Delivery":10,"Defect Rate":15,"Sustainability":10},"Speed First":{"Cost":10,"Quality":15,"Lead Time":30,"On-Time Delivery":25,"Defect Rate":10,"Sustainability":10},"Risk Reduction":{"Cost":10,"Quality":25,"Lead Time":10,"On-Time Delivery":25,"Defect Rate":20,"Sustainability":10},"Sustainability First":{"Cost":15,"Quality":20,"Lead Time":10,"On-Time Delivery":10,"Defect Rate":10,"Sustainability":35},"Balanced Procurement":DEFAULT_WEIGHTS.copy()}[n]
