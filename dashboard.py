import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF
import tempfile

# Set page configuration
st.set_page_config(page_title="E-commerce Business Dashboard", page_icon="📊", layout="wide")

# Display Creator Information
st.markdown("""
    <h1 style='text-align: center; color: #4CAF50;'>📊 A tool to visualize and analyze business metrics.</h1>
    <h3 style='text-align: center; color: #888;'>Made by MD H. Rahman</h3>
    <h4 style='text-align: center;'><a href='https://www.linkedin.com/in/habib-rahmann/' target='_blank'>LinkedIn Profile</a></h4>
""", unsafe_allow_html=True)

# Function to clean text (remove unsupported characters for PDF)
def clean_text(text):
    return text.encode("ascii", "ignore").decode()

# Enter Business Name
business_name = st.text_input("Enter Your Business Name (Ex: ABC Retail)", "My Business")

# Manually Enter Data
st.subheader("📋 Enter Business Data ")

col1, col2, col3 = st.columns(3)
total_revenue = col1.number_input("Total Revenue ($)", min_value=0.0, format="%.2f")
marketing_spend = col2.number_input("Marketing Spend ($)", min_value=0.0, format="%.2f")
cost_of_goods_sold = col3.number_input("Cost of Goods Sold ($)", min_value=0.0, format="%.2f")

col4, col5, col6 = st.columns(3)
operating_expenses = col4.number_input("Operating Expenses ($)", min_value=0.0, format="%.2f")
customer_acquisition_cost = col5.number_input("Customer Acquisition Cost ($)", min_value=0.0, format="%.2f")
conversion_rate = col6.number_input("Conversion Rate (%)", min_value=0.0, max_value=100.0, format="%.2f")

col7, col8 = st.columns(2)
new_customers = col7.number_input("New Customers", min_value=0, format="%d")
visitors = col8.number_input("Total Visitors", min_value=0, format="%d")
initial_investment = st.number_input("Initial Investment ($)", min_value=0.0, format="%.2f")

# Calculations
gross_profit = total_revenue - cost_of_goods_sold
net_profit = gross_profit - operating_expenses
cash_flow = net_profit - initial_investment
roi = ((net_profit - initial_investment) / initial_investment) * 100 if initial_investment > 0 else 0
predicted_growth_rate = (new_customers / visitors) * 100 if visitors > 0 else 0
future_revenue = total_revenue * (1 + predicted_growth_rate / 100)

# Display Key Metrics
st.subheader("📊 Business Metrics Overview")
st.metric(label="Total Revenue", value=f"${total_revenue:,.2f}")
st.metric(label="Gross Profit", value=f"${gross_profit:,.2f}")
st.metric(label="Net Profit", value=f"${net_profit:,.2f}")
st.metric(label="Cash Flow", value=f"${cash_flow:,.2f}")
st.metric(label="Return on Investment (ROI)", value=f"{roi:.2f}%")
st.metric(label="Predicted Revenue (Next Quarter)", value=f"${future_revenue:,.2f}")
st.caption(f"🔍 Predicted based on new customer growth rate of {predicted_growth_rate:.2f}%, assuming similar trends continue.")

# Revenue Breakdown & Marketing Efficiency
st.subheader("📈 Revenue Breakdown & Marketing Efficiency")
chart_data = pd.DataFrame({
    "Category": ["Total Revenue", "Marketing Spend", "Customer Acquisition Cost"],
    "Value": [total_revenue, marketing_spend, customer_acquisition_cost]
})
revenue_fig = px.bar(chart_data, x="Category", y="Value", title="Revenue and Marketing Overview")
st.plotly_chart(revenue_fig, use_container_width=True)

# Dynamic Recommendations
recommendations = []
if total_revenue == 0:
    recommendations.append("💡 Enter more data for recommendations.")
else:
    if roi < 0:
        recommendations.append("Your ROI is negative. Consider reducing costs or increasing revenue streams to improve profitability.")
    if cash_flow < 0:
        recommendations.append("Your cash flow is negative. You may need to adjust pricing or expenses to improve liquidity.")
    if conversion_rate < 5:
        recommendations.append("Your conversion rate is low. Optimize your website and marketing strategy to increase conversions.")
    if total_revenue > 0 and marketing_spend / total_revenue > 0.3:
        recommendations.append("Marketing spend is high relative to revenue. Optimize your ad spend for better efficiency.")

st.subheader("📌 Business Recommendations")

# Generate overall feedback based on data
if total_revenue > 0 and roi > 0 and cash_flow > 0 and conversion_rate >= 5:
    recommendations.insert(0, "✅ Your business is performing well! Keep up the great work and continue optimizing for sustained growth.")
else:
    if roi > 0:
        recommendations.insert(0, "✅ Your ROI is positive, indicating a good return on your investment!")
    if cash_flow > 0:
        recommendations.insert(0, "✅ Your cash flow is positive, which means your business is generating more cash than it's spending!")
    if conversion_rate >= 5:
        recommendations.insert(0, "✅ Your conversion rate is healthy, showing effective customer engagement!")
for rec in recommendations:
    st.write(f"- {rec}")

# Function to generate PDF report
def generate_pdf():
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", style='B', size=16)
    pdf.cell(200, 10, clean_text(f"{business_name} - Business Report"), ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, clean_text(f"Total Revenue: ${total_revenue:,.2f}"), ln=True)
    pdf.cell(200, 10, clean_text(f"Gross Profit: ${gross_profit:,.2f}"), ln=True)
    pdf.cell(200, 10, clean_text(f"Net Profit: ${net_profit:,.2f}"), ln=True)
    pdf.cell(200, 10, clean_text(f"Cash Flow: ${cash_flow:,.2f}"), ln=True)
    pdf.cell(200, 10, clean_text(f"ROI: {roi:.2f}%"), ln=True)
    pdf.cell(200, 10, clean_text(f"Predicted Revenue: ${future_revenue:,.2f}"), ln=True)
    pdf.cell(200, 10, "Recommendations:", ln=True)
    for rec in recommendations:
        pdf.cell(200, 10, clean_text(f"- {rec}"), ln=True)
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        pdf.output(tmp_file.name, "F")
        tmp_file_path = tmp_file.name
    
    return tmp_file_path  # Return file path instead of bytes

# Download Report Button
st.subheader("📄 Download Business Report")
pdf_path = generate_pdf()
st.download_button(label="Download PDF Report", data=open(pdf_path, "rb"), file_name="business_report.pdf", mime="application/pdf")

