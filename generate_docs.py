from fpdf import FPDF
import os

class BusinessReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'London Bicycles Data Pipeline & Analysis Report', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def generate_pdf():
    pdf = BusinessReport()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Section 1: Introduction
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, '1. Executive Summary', 0, 1)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, "This report details the end-to-end data pipeline built for the London Bicycles dataset. The objective was to ingest raw data, transform it into a star schema data warehouse, ensure high data quality, perform exploratory data analysis, and orchestrate the pipeline for regular execution.")
    pdf.ln(5)

    # Section 2: Technical Architecture
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, '2. Pipeline Architecture & Tooling Justifications', 0, 1)
    pdf.set_font("Arial", size=12)
    arch_text = (
        "1. Source: Google BigQuery Public Data (london_bicycles dataset).\n"
        "2. Ingestion: Python extracts the data to a local environment ensuring no network payload bottlenecks.\n"
        "3. Data Warehouse: DuckDB is used as the analytical database. It is much faster than SQLite for OLAP workloads and integrates natively with Python and Pandas.\n"
        "4. ELT & Data Quality: Python-native SQL performs Data Cleaning, derivations, and tests for exact duplicates, null checks, and referential integrity.\n"
        "5. Orchestration: Prefect orchestrates the entire pipeline, creating a resilient, visible, and easily schedulable DAG.\n"
        "6. Lineage: BigQuery -> raw_cycle_stations / raw_cycle_hire -> dim_stations / fact_trips -> Python Analysis."
    )
    pdf.multi_cell(0, 10, arch_text)
    pdf.ln(5)

    # Section 3: Data Analysis & Insights
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, '3. Data Analysis & Findings', 0, 1)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, "Our exploratory analysis yielded key insights regarding usage patterns over time and space.")
    pdf.ln(5)

    try:
        pdf.image('analysis_output/trips_by_hour.png', w=170)
        pdf.ln(5)
        pdf.multi_cell(0, 10, "Insight 1: Busiest Hours. The peak hours are clearly reflecting morning (typically 8 AM) and evening (typically 5 PM) commuter peaks, indicating usage is heavily tailored around workforce transit.")
    except Exception as e:
        pdf.multi_cell(0, 10, "(Image missing - analysis output not found)")
        
    pdf.add_page()
    try:
        pdf.image('analysis_output/top_10_start_stations.png', w=170)
        pdf.ln(5)
        pdf.multi_cell(0, 10, "Insight 2: Busiest Stations. The top starting stations concentrate heavily around major transit hubs and business centers, providing key supply-chain locations for bicycle reallocation.")
    except Exception as e:
        pdf.multi_cell(0, 10, "(Image missing - analysis output not found)")

    # Section 4: Business Recommendations
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, '4. Business Recommendations for Executives', 0, 1)
    pdf.set_font("Arial", size=12)
    recommendations = (
        "- Supply Chain Operations (VP Engineering): Automate the reallocation of bicycles to top-performing stations during non-peak hours (10 AM - 3 PM and midnight) to prepare for the morning/evening rush.\n"
        "- Targeted Marketing (CMO): Launch targeted campaigns or partnerships with businesses near the busiest stations. Introduce commuter membership plans tailored to 8 AM and 5 PM users.\n"
        "- Strategic Expansion (CEO): The pipeline is scalable. Consider extending infrastructure by adding more stations near the top 5 areas, as they currently operate near maximum demand capacity during peak hours."
    )
    pdf.multi_cell(0, 10, recommendations)

    pdf.output('london_bicycles_report.pdf')
    print("PDF Report Generated successfully.")

if __name__ == '__main__':
    generate_pdf()
