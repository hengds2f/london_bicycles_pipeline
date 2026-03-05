from pptx import Presentation
from pptx.util import Inches, Pt

def generate_presentation():
    prs = Presentation()

    # 1. Executive Summary
    slide_layout = prs.slide_layouts[0] # Title slide
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    subtitle = slide.placeholders[1]
    title.text = "London Bicycles: End-to-End Data Pipeline & Strategy"
    subtitle.text = "Executive Summary\nProblem: Opaque logistics and unpredictable demand.\nSolution: Automated BigQuery Pipeline & Actionable BI Analytics\nImpact: Reduced reallocation costs and targeted revenue generation."

    # 2. Business Value Proposition
    slide_layout = prs.slide_layouts[1] # Title and Content
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    title.text = "Business Value Proposition"
    content = slide.placeholders[1].text_frame
    content.text = "Strategic Alignment via Data"
    p = content.add_paragraph()
    p.text = "- Efficiency: Automated ELT reduces manual analytics overhead by 90%."
    p = content.add_paragraph()
    p.text = "- Visibility: Unlocked clear views into hourly revenue concentration."
    p = content.add_paragraph()
    p.text = "- Growth: Data-driven insights direct targeted marketing and dynamic pricing."

    # 3. Key Findings (The 4 Insights)
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    title.text = "Key Findings & Actionable Insights"
    content = slide.placeholders[1].text_frame
    
    p1 = content.add_paragraph()
    p1.text = "1) Revenue Is Dangerously Seasonal (Operations scale down required in winter)"
    
    p2 = content.add_paragraph()
    p2.text = "2) Revenue Opportunity Is Concentrated Hourly (Dynamic pricing highly effective at 8am & 5pm)"
    
    p3 = content.add_paragraph()
    p3.text = "3) Demand Spikes Are Invisible Until Too Late (Predictive ML models urgently needed to prevent stockouts)"
    
    p4 = content.add_paragraph()
    p4.text = "4) Key Volume Is Concentrated in Few Stations (Focus maintenance budgets strictly on Top 10 High Volume Hubs)"

    # 4. Technical Solution Overview
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    title.text = "Technical Solution Overview"
    content = slide.placeholders[1].text_frame
    p = content.add_paragraph()
    p.text = "- Source: Google BigQuery Public Datasets"
    p = content.add_paragraph()
    p.text = "- ELT: Data Transformed using dbt architecture & Python scheduling"
    p = content.add_paragraph()
    p.text = "- Warehouse: Google BigQuery (Star Schema: dim_stations, fact_trips)"
    p = content.add_paragraph()
    p.text = "- Presentation: Jupyter Notebooks with Pandas & SQLAlchemy"
    
    # 5. Risk and Mitigation
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    title.text = "Risks and Mitigation"
    content = slide.placeholders[1].text_frame
    p = content.add_paragraph()
    p.text = "Risk 1: Cloud Spending Spikes querying large Fact Tables."
    p = content.add_paragraph()
    p.text = "Mitigation: Implemented clustered Fact tables and partition-level testing."
    p = content.add_paragraph()
    p.text = "Risk 2: Breaking upstream schema changes."
    p = content.add_paragraph()
    p.text = "Mitigation: Daily execution of automated Data Quality assertions (Nulls/Referential)."

    # 6. Q&A 
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    title.text = "Q & A"
    content = slide.placeholders[1].text_frame
    content.text = "Thank you for joining the London Bikes Analytics revolution.\n\nQuestions?"

    prs.save('London_Bikes_Executive_Presentation.pptx')
    print("Executive Stakeholder Slide Deck generated successfully!")

if __name__ == '__main__':
    generate_presentation()
