import os
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib import colors
from reportlab.lib.units import inch

EXCEL_PATH = "Old FINAL Data_MIS.xlsx"
OUTPUT_DIR = "reports"
LOGO_PATH = "logo.png"
SIGN1_PATH = "sign1.png"
SIGN2_PATH = "sign2.png"

TEST_GROUPS = {
    "Lipid Profile Test ~ Clinical Chemistry ~ Blood (Serum)-Red": {
        "S.TOTAL CHOLESTEROL": "<200 mg/dL",
        "S.TRIGLYCERIDES": "40 to 160 mg/dL",
        "Direct HDL": "35 to 60 mg/dL",
        "LDL": "75 to 130 mg/dL",
        "VLDL": "10 to 32 mg/dL",
        "TOTAL CHOLESTEROL/HDL RATIO": "3 to 5",
        "LDL/HDL RATIO": "1.5 to 3.5",
        "NON HDL CHOLESTEROL*": ""
    },
    "LFT (Liver Function Test) ~ Clinical Chemistry ~ Blood (Serum)-Red": {
        "Total Bilirubin": "<2 mg/dL",
        "Direct Bilirubin": "0.1 to 0.4 mg/dL",
        "Indirect Bilirubin": "<0.8 mg/dL",
        "SGOT": "<31 U/L",
        "SGPT": "<34 U/L",
        "SGOT/SGPTRatio": "",
        "Alkaline Phosphatase": "42 to 98 U/L",
        "S.GGT": "<30 U/L",
        "Total Proteins": "6 to 8.5 gm/dL",
        "Albumin": "3.5 to 5.5 gm/dL",
        "Globulin": "2.5 to 3.5 gm/dL",
        "A/G Ratio": "1 to 1.8"
    },
    "TFT (Thyroid Function Test) ~ Clinical Chemistry ~ Blood (Serum)-Red": {
        "T3 (Triiodothyronine)": "0.87 to 1.78 ng/ml",
        "T4 (Thyroxine)": "3.2 to 12.6 ug/dl",
        "TSH-Thyrotropin Stimulating Hormon": "0.35 to 5.5 uIU/ml"
    },
    "CBC / Platelets": {
        "Platelet Count": "1.50 – 4.00 Lakh/comm."
    }
}

INTERPRETATIONS = {
    "Lipid Profile": "The results of your lipid panel are reported for each type of cholesterol and triglycerides...",
    "LFT": "These tests help detect liver disease, differentiate liver disorders, assess liver damage, and monitor treatment...",
    "TFT": "TSH reference ranges vary by age. Assay results should be interpreted only in context of clinical status...",
    "CBC / Platelets": "Method: PLT-Electrical impedance. Low platelets - risk of bleeding. High platelets - risk of thrombosis."
}

FOOTER = "CORE Diagnostics (Central Reference Lab) - Gurugram<br/>406, Udyog Vihar, Phase III, Gurugram, Haryana - 122016"

def generate_page(doc, story, data_row, title, tests, interpretation):
    styles = getSampleStyleSheet()
    centered = ParagraphStyle(name='Centered', parent=styles['Normal'], alignment=TA_CENTER)
    lefted = ParagraphStyle(name='Lefted', parent=styles['Normal'], alignment=TA_LEFT)

    if os.path.exists(LOGO_PATH):
        story.append(Image(LOGO_PATH, width=6.5*inch, height=1*inch))
    story.append(Paragraph(f"<b>{title}</b>", centered))
    story.append(Spacer(1, 12))

    info = [["Name", data_row['Name'], "Age", str(data_row['Age'])],
            ["Gender", data_row['GENDER'], "Location", data_row['Location']]]
    table = Table(info, colWidths=[100, 150, 100, 150])
    table.setStyle(TableStyle([("GRID", (0,0), (-1,-1), 0.5, colors.black)]))
    story.append(table)
    story.append(Spacer(1, 16))

    story.append(Table([["Parameter", "Result", "Reference"]], colWidths=[220, 120, 140],
                       style=[("BACKGROUND", (0,0), (-1,0), colors.grey), ("TEXTCOLOR", (0,0), (-1,0), colors.white)]))

    for test, ref in tests.items():
        val = str(data_row.get(test, "")).strip()
        if val and val.lower() != "nan":
            story.append(Table([[test, val, ref]], colWidths=[220, 120, 140],
                               style=[("GRID", (0,0), (-1,-1), 0.25, colors.grey)]))

    story.append(Spacer(1, 20))
    story.append(Paragraph("<b>Interpretation:</b>", styles["Heading5"]))
    story.append(Paragraph(interpretation, lefted))
    story.append(Spacer(1, 30))

    sig_table = Table([[Image(SIGN1_PATH, width=1.5*inch, height=0.5*inch), Image(SIGN2_PATH, width=1.5*inch, height=0.5*inch)],
                       [Paragraph("<b>Dr. Bhavna Jaiswal</b><br/>MBBS, MD, DPB<br/>Consultant Pathologist", centered),
                        Paragraph("<b>Dr. Rahul Sharma</b><br/>PhD Microbiologist", centered)]],
                      colWidths=[3*inch, 3*inch])
    story.append(sig_table)
    story.append(Spacer(1, 20))
    story.append(Paragraph(FOOTER, centered))
    story.append(PageBreak())

def generate_report(data_row):
    name_slug = data_row['Name'].replace(" ", "_")
    output_path = os.path.join(OUTPUT_DIR, f"Report_{name_slug}.pdf")
    story = []
    doc = SimpleDocTemplate(output_path, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)

    for group_name, tests in TEST_GROUPS.items():
        interpretation = next((v for k,v in INTERPRETATIONS.items() if k.lower() in group_name.lower()), "")
        generate_page(doc, story, data_row, group_name, tests, interpretation)

    doc.build(story)
    print(f"✅ Generated: {output_path}")

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    df = pd.read_excel(EXCEL_PATH)
    df.columns = df.columns.str.strip()
    for _, row in df.iterrows():
        generate_report(row)

if __name__ == "__main__":
    main()
