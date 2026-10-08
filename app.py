from pathlib import Path
import os,pandas as pd,streamlit as st,plotly.express as px
from utils.scoring import score_vendors,DEFAULT_WEIGHTS,CRITERIA,scenario_weights
from utils.validation import validate_dataframe
from utils.scenarios import run_scenario
from utils.ai_analysis import get_gemini_response
st.set_page_config(page_title="ProcureAI",page_icon="🧭",layout="wide")
ROOT=Path(__file__).parent
st.markdown("<style>.hero{padding:22px;border-radius:16px;background:#111827;color:white}.block-container{padding-top:1.5rem}</style>",unsafe_allow_html=True)
@st.cache_data
def load(n): return pd.read_csv(ROOT/n)
st.sidebar.header("ProcureAI")
source=st.sidebar.selectbox("Dataset",["10-vendor demo","250-vendor scale","Upload CSV"])
if source=="10-vendor demo": df=load("sample_vendors_10.csv")
elif source=="250-vendor scale": df=load("sample_vendors_250.csv")
else:
 f=st.sidebar.file_uploader("Upload CSV",type="csv"); df=pd.read_csv(f) if f else load("sample_vendors_10.csv")
st.sidebar.subheader("Decision weights")
weights={k:st.sidebar.number_input(k,0.,100.,float(v),1.) for k,v in DEFAULT_WEIGHTS.items()}
total=sum(weights.values()); st.sidebar.write(f"Total: **{total:.1f}%**")
validation=validate_dataframe(df)
pages=["Home","Executive Dashboard","Vendor Ranking","Vendor Analysis","Vendor Profile","Strategy Simulator","What-If Analysis","AI Assistant","Data Validation"]
page=st.sidebar.radio("Navigate",pages)
scored=score_vendors(df,weights) if validation["valid"] and abs(total-100)<1e-9 else None
def guard():
 if not validation["valid"]: st.error("Fix data validation errors before scoring."); return True
 if abs(total-100)>1e-9: st.error("Weights must total 100%."); return True
 return False
if page=="Home":
 st.markdown('<div class="hero"><h1>PROCUREAI</h1><p>AI-Powered Vendor Selection & Procurement Intelligence Platform</p><p>Smarter supplier decisions. Transparent recommendations. AI-powered procurement intelligence.</p></div>',unsafe_allow_html=True)
 st.subheader("Business Problem"); st.write("ProcureAI converts multi-criteria supplier comparison into a transparent, adjustable and explainable decision-support workflow.")
 a,b,c=st.columns(3); a.metric("Use Case","Vendor Selection"); b.metric("Criteria",6); c.metric("Demo Vendors",10)
 st.subheader("Workflow"); st.write("Data → validation → deterministic scoring → ranking → what-if analysis → analytics → Gemini explanation.")
 st.info("Responsible AI: this prototype supports procurement decisions; it does not independently approve, contract with, or purchase from vendors.")
elif page=="Executive Dashboard":
 st.title("Executive Dashboard")
 if not guard():
  v=scored.iloc[0]; cols=st.columns(5)
  for col,label,val in zip(cols,["Vendors","Best Vendor","Best Score","Highly Recommended","High Risk"],[len(scored),v.Vendor_Name,f"{v.Overall_Score:.1f}",int((scored.Recommendation=="Highly Recommended").sum()),int((scored.Risk_Level=="High").sum())]): col.metric(label,val)
  st.plotly_chart(px.bar(scored.sort_values("Overall_Score"),x="Overall_Score",y="Vendor_Name",orientation="h",title="Vendor Ranking"),use_container_width=True)
  st.write(f"**Insight:** {v.Vendor_Name} ranks first at {v.Overall_Score:.1f}; the result reflects the selected weights.")
elif page=="Vendor Ranking":
 st.title("Vendor Ranking")
 if not guard():
  filt=st.multiselect("Category",sorted(scored.Category.unique())); view=scored[scored.Category.isin(filt)] if filt else scored
  st.dataframe(view[["Rank","Vendor_Name","Category","Country","Overall_Score","Recommendation","Risk_Level","Cost_Score","Quality_Score","Lead Time_Score","On-Time Delivery_Score","Defect Rate_Score","Sustainability_Score"]],use_container_width=True,hide_index=True)
elif page=="Vendor Analysis":
 st.title("Vendor Analysis")
 if not guard():
  a,b=st.columns(2); a.plotly_chart(px.scatter(scored,x="Unit_Cost",y="Quality_Score",color="Risk_Level",hover_name="Vendor_Name",title="Cost vs Quality"),use_container_width=True); b.plotly_chart(px.scatter(scored,x="Lead_Time_Days",y="On_Time_Delivery_Percentage",color="Risk_Level",hover_name="Vendor_Name",title="Lead Time vs Delivery"),use_container_width=True)
  a,b=st.columns(2); a.plotly_chart(px.scatter(scored,x="Risk_Score",y="Overall_Score",color="Recommendation",hover_name="Vendor_Name",title="Risk vs Overall Score"),use_container_width=True)
  m=scored.head(3).melt(id_vars="Vendor_Name",value_vars=[f"{x}_Score" for x in CRITERIA],var_name="Criterion",value_name="Score"); b.plotly_chart(px.bar(m,x="Criterion",y="Score",color="Vendor_Name",barmode="group",title="Top 3 Comparison"),use_container_width=True)
elif page=="Vendor Profile":
 st.title("Vendor Profile")
 if not guard():
  name=st.selectbox("Vendor",scored.Vendor_Name); v=scored[scored.Vendor_Name==name].iloc[0]; a,b,c,d=st.columns(4)
  a.metric("Rank",int(v.Rank)); b.metric("Score",f"{v.Overall_Score:.1f}"); c.metric("Recommendation",str(v.Recommendation)); d.metric("Risk",str(v.Risk_Level))
  st.write(f"**Country:** {v.Country}  |  **Category:** {v.Category}  |  **Unit cost:** {v.Unit_Cost:.2f}  |  **Quality:** {v.Quality_Score:.1f}  |  **Lead time:** {v.Lead_Time_Days:.1f} days  |  **On-time:** {v.On_Time_Delivery_Percentage:.1f}%")
  x=pd.DataFrame({"Criterion":list(CRITERIA),"Score":[v[f"{k}_Score"] for k in CRITERIA]}); st.plotly_chart(px.bar(x,x="Criterion",y="Score",title="Criterion Score Profile"),use_container_width=True)
  st.write("Top weighted contributions:",sorted([(k,float(v[f"{k}_Contribution"])) for k in CRITERIA],key=lambda z:z[1],reverse=True)[:3])
elif page=="Strategy Simulator":
 st.title("Procurement Strategy Simulator")
 if not guard():
  n=st.selectbox("Strategy",list(["Cost Optimization","Quality First","Speed First","Risk Reduction","Sustainability First","Balanced Procurement"])); alt=score_vendors(df,scenario_weights(n)); m=scored[["Vendor_ID","Vendor_Name","Rank","Overall_Score"]].merge(alt[["Vendor_ID","Rank","Overall_Score"]],on=["Vendor_ID","Vendor_Name"],suffixes=("_Baseline","_Strategy")); m["Rank_Change"]=m.Rank_Baseline-m.Rank_Strategy; st.write("Weights:",scenario_weights(n)); st.dataframe(m.sort_values("Rank_Strategy"),use_container_width=True,hide_index=True)
elif page=="What-If Analysis":
 st.title("What-If Analysis")
 if not guard():
  n=st.selectbox("Scenario",["Cost Optimization","Quality First","Speed First","Risk Reduction","Sustainability First","Balanced Procurement"]); r=run_scenario(df,n); st.dataframe(r,use_container_width=True,hide_index=True)
elif page=="AI Assistant":
 st.title("AI Procurement Assistant")
 if not guard():
  name=st.selectbox("Focus vendor",scored.Vendor_Name); q=st.text_area("Question",f"Why is {name} ranked where it is and what should procurement consider?"); v=scored[scored.Vendor_Name==name].iloc[0]
  if st.button("Analyze with Gemini",type="primary"): ans,err=get_gemini_response({"selected_vendor":v.to_dict(),"top_vendors":scored.head(3).to_dict("records"),"weights":weights},q); _ = st.warning(err) if err else st.markdown(ans)
  st.caption("Gemini explains structured analytics; it cannot change the deterministic ranking.")
else:
 st.title("Data Validation"); st.metric("Status","PASS" if validation["valid"] else "FAIL")
 if validation["errors"]: st.dataframe(pd.DataFrame(validation["errors"]),use_container_width=True,hide_index=True)
 if validation["warnings"]: st.warning("Warnings detected."); st.dataframe(pd.DataFrame(validation["warnings"]),use_container_width=True,hide_index=True)
 if st.button("Validate invalid test dataset"):
  r=validate_dataframe(pd.read_csv(ROOT/"test_vendors_invalid.csv")); st.write(f"Errors: {len(r['errors'])}, Warnings: {len(r['warnings'])}"); st.dataframe(pd.DataFrame(r["errors"]),use_container_width=True,hide_index=True)
