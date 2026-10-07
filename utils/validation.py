import pandas as pd
REQUIRED=["Vendor_ID","Vendor_Name","Category","Sub_Category","Location","Country","Vendor_Size","Years_in_Business","Unit_Cost","Annual_Contract_Value","Payment_Terms_Days","Minimum_Order_Quantity","Price_Volatility_Percentage","Quality_Score","Defect_Rate","Return_Rate","Quality_Complaints","Lead_Time_Days","On_Time_Delivery_Percentage","Average_Delay_Days","Delivery_Failure_Rate","Annual_Capacity","Capacity_Utilization_Percentage","Scalability_Score","Financial_Risk_Score","Supply_Risk_Score","Geopolitical_Risk_Score","Business_Continuity_Score","Sustainability_Score","Carbon_Footprint_Score","ESG_Compliance_Score","Vendor_Response_Score","Service_Score","Contract_Compliance_Score"]
RANGES=["Price_Volatility_Percentage","Defect_Rate","Return_Rate","On_Time_Delivery_Percentage","Average_Delay_Days","Delivery_Failure_Rate","Capacity_Utilization_Percentage","Quality_Score","Scalability_Score","Financial_Risk_Score","Supply_Risk_Score","Geopolitical_Risk_Score","Business_Continuity_Score","Sustainability_Score","ESG_Compliance_Score","Vendor_Response_Score","Service_Score","Contract_Compliance_Score"]
def validate_dataframe(df):
 e=[]; w=[]; miss=[c for c in REQUIRED if c not in df.columns]
 for c in miss:e.append({"row":"-","field":c,"issue":"Missing required column","fix":"Add field"})
 if miss:return {"valid":False,"errors":e,"warnings":w}
 for c in ["Vendor_ID","Vendor_Name","Category"]:
  for i in df.index[df[c].isna() | (df[c].astype(str).str.strip()=="")]:e.append({"row":int(i)+2,"field":c,"issue":"Missing required value","fix":"Populate value"})
 for i in df.index[df["Vendor_ID"].duplicated(keep=False)]:e.append({"row":int(i)+2,"field":"Vendor_ID","issue":"Duplicate Vendor_ID","fix":"Use unique ID"})
 numeric=["Unit_Cost","Annual_Contract_Value","Payment_Terms_Days","Minimum_Order_Quantity","Years_in_Business","Lead_Time_Days","Annual_Capacity"]+RANGES
 for c in numeric:
  s=pd.to_numeric(df[c],errors="coerce")
  for i in df.index[s.isna() & df[c].notna()]:e.append({"row":int(i)+2,"field":c,"issue":"Invalid numeric type","fix":"Use numeric value"})
 for c in ["Unit_Cost","Annual_Contract_Value","Payment_Terms_Days","Minimum_Order_Quantity","Years_in_Business","Lead_Time_Days","Annual_Capacity"]:
  s=pd.to_numeric(df[c],errors="coerce")
  for i in df.index[s<0]:e.append({"row":int(i)+2,"field":c,"issue":"Negative value","fix":"Use non-negative value"})
 for c in RANGES:
  s=pd.to_numeric(df[c],errors="coerce")
  for i in df.index[(s<0)|(s>100)]:e.append({"row":int(i)+2,"field":c,"issue":"Outside 0–100 range","fix":"Correct value"})
 for i in df.index[df.duplicated(keep=False)]:w.append({"row":int(i)+2,"field":"record","issue":"Duplicate record","fix":"Review duplicate"})
 return {"valid":len(e)==0,"errors":e,"warnings":w}
