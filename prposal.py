from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor  # <-- CORRECT IMPORT PATH
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

# Create presentation (16:9 aspect ratio)
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

def add_title_slide(prs, title, subtitle):
    slide_layout = prs.slide_layouts[6] # Blank
    slide = prs.slides.add_slide(slide_layout)
    
    # Title
    left = Inches(0.5)
    top = Inches(1.5)
    width = Inches(12.333)
    height = Inches(2)
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0, 51, 102)
    p.alignment = PP_ALIGN.CENTER

    # Subtitle / Info
    top = Inches(4.0)
    height = Inches(2.5)
    txBox2 = slide.shapes.add_textbox(left, top, width, height)
    tf2 = txBox2.text_frame
    tf2.word_wrap = True
    p2 = tf2.paragraphs[0]
    p2.text = subtitle
    p2.font.size = Pt(18)
    p2.font.color.rgb = RGBColor(50, 50, 50)
    p2.alignment = PP_ALIGN.CENTER
    return slide

def add_content_slide(prs, title, bullets):
    slide_layout = prs.slide_layouts[6] # Blank
    slide = prs.slides.add_slide(slide_layout)
    
    # Title Box
    left = Inches(0.5)
    top = Inches(0.3)
    width = Inches(12.333)
    height = Inches(0.8)
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0, 51, 102)

    # Content Box
    top = Inches(1.3)
    height = Inches(5.8)
    txBox2 = slide.shapes.add_textbox(left, top, width, height)
    tf2 = txBox2.text_frame
    tf2.word_wrap = True
    
    for i, bullet in enumerate(bullets):
        if i == 0:
            p2 = tf2.paragraphs[0]
        else:
            p2 = tf2.add_paragraph()
        
        p2.text = bullet
        p2.font.size = Pt(18)
        p2.space_after = Pt(8)
    return slide

def add_table_slide(prs, title, headers, rows):
    slide_layout = prs.slide_layouts[6] # Blank
    slide = prs.slides.add_slide(slide_layout)
    
    # Title
    left = Inches(0.5)
    top = Inches(0.3)
    width = Inches(12.333)
    height = Inches(0.8)
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0, 51, 102)

    # Table
    cols = len(headers)
    table_rows = len(rows) + 1
    table = slide.shapes.add_table(table_rows, cols, Inches(0.5), Inches(1.3), Inches(12.333), Inches(5.5)).table

    # Set Header
    for i, header in enumerate(headers):
        cell = table.cell(0, i)
        cell.text = header
        cell.text_frame.paragraphs[0].font.bold = True
        cell.text_frame.paragraphs[0].font.size = Pt(14)
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(0, 51, 102)
        cell.text_frame.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)

    # Set Rows
    for r_idx, row_data in enumerate(rows):
        for c_idx, cell_text in enumerate(row_data):
            cell = table.cell(r_idx + 1, c_idx)
            cell.text = cell_text
            cell.text_frame.paragraphs[0].font.size = Pt(12)
            if r_idx % 2 == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(240, 240, 240)
    return slide

def add_end_slide(prs, text):
    slide_layout = prs.slide_layouts[6] # Blank
    slide = prs.slides.add_slide(slide_layout)
    left = Inches(0.5)
    top = Inches(2.5)
    width = Inches(12.333)
    height = Inches(2)
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(44)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0, 51, 102)
    p.alignment = PP_ALIGN.CENTER
    return slide

# ==========================================
# BUILD THE PRESENTATION
# ==========================================

# Slide 1: Title
add_title_slide(prs, 
    "DEVELOPMENT AND IMPLEMENTATION OF A LOW-POWER MEMS-BASED WEARABLE RESPIRATORY SHIELD\nFOR REAL-TIME ASTHMA TRIGGER DETECTION AND EXPOSURE MAPPING",
    "SURNAME, Other names\n\nFEDERAL UNIVERSITY OF TECHNOLOGY MINNA\nDepartment of Computer Engineering\nSupervisor: [Supervisor's Name]\n2024/2025\n[M.Eng or Phd/SEET/202X/XXXX]"
)

# Slide 2: Outline
add_content_slide(prs, "Outline", [
    "1. Introduction & Background",
    "2. Problem Statement",
    "3. Research Objectives & Questions",
    "4. Scope & Significance",
    "5. Literature Review (Global)",
    "6. Literature Review (Africa & Nigeria)",
    "7. Summary of Reviewed Works",
    "8. Identified Research Gaps",
    "9. Expected Contributions",
    "10. References"
])

# Slide 3: Introduction
add_content_slide(prs, "Introduction", [
    "▪ Asthma affects 262 million people globally, causing over 450,000 deaths annually (WHO, 2022)",
    "▪ Nigeria bears a disproportionate burden, with prevalence rates between 5% and 15% in urban/industrial areas",
    "▪ Current asthma management relies on post-symptom intervention rather than proactive trigger avoidance",
    "▪ Micro-Electromechanical Systems (MEMS) offer miniaturized, energy-efficient sensing (microwatt power consumption)",
    "▪ A wearable 'respiratory shield' merges MEMS sensing, IoT architecture, and health informatics for real-time alerts",
    "▪ Local context: Niger State's urban growth, industrial corridor activity, and biomass fuel use create a compelling deployment scenario"
])

# Slide 4: Problem Statement
add_content_slide(prs, "Problem Statement", [
    "Challenges with Current Asthma Management in Nigeria:",
    "▪ Commercial tools (e.g., peak flow meters) measure lung function only after symptoms begin",
    "▪ Hospital-based spirometry is financially and geographically inaccessible to most Nigerians",
    "▪ Government environmental monitoring stations are sparse, non-functional, and fail to capture micro-environmental exposures",
    "▪ Absence of affordable, patient-level tools for identifying and mapping personal asthma triggers in real time",
    "",
    "Research Gap:",
    "▪ There is a critical lack of locally developed research integrating low-power embedded systems with respiratory health monitoring in the Nigerian engineering context, leaving a gap for local policymakers and clinicians."
])

# Slide 5: Research Objectives
add_content_slide(prs, "Research Objectives", [
    "Aim: To develop and implement a low-power MEMS-based wearable respiratory shield capable of detecting asthma triggers in real time and generating exposure maps.",
    "",
    "▪ RO₁: Identify and characterize primary environmental asthma triggers relevant to Niger State",
    "▪ RO₂: Select and integrate appropriate MEMS sensors (PM2.5/PM10, VOCs, humidity, temperature) into a compact wearable platform",
    "▪ RO₃: Design a low-power embedded system architecture for continuous real-time data acquisition",
    "▪ RO₄: Develop firmware and signal processing algorithms for trigger threshold detection and alert generation",
    "▪ RO₅: Implement a data logging and wireless transmission module for GPS-referenced exposure mapping",
    "▪ RO₆: Evaluate system performance regarding sensor accuracy, power consumption, response latency, and usability"
])

# Slide 6: Scope & Significance
add_content_slide(prs, "Scope & Significance of the Study", [
    "Scope:",
    "▪ Prototype development and lab/field evaluation",
    "▪ Targets Particulate Matter (PM), VOCs, Humidity, and Temperature",
    "▪ Geographic testing within Minna metropolis and environs",
    "▪ Complementary tool (does not replace medical diagnosis)",
    "",
    "Significance:",
    "▪ Engineering: Demonstrates feasibility of low-cost wearable health tech using commercially available MEMS components",
    "▪ Public Health: Addresses unmet need for personalized monitoring for millions of Nigerians; generates granular geo-referenced air quality data",
    "▪ Academia: Provides a documented reference design for FUT-Minna and similar institutions for future IoT health systems"
])

# Slide 7: Literature Review - Global
add_content_slide(prs, "Literature Review - Global Context", [
    "Asthma Epidemiology & Triggers:",
    "▪ 25.9 million DALYs in 2019 (GBD, 2020); triggers include PM2.5, NO₂, VOCs, and extreme humidity (Papi et al., 2018)",
    "▪ Traffic-related pollution strongly linked to childhood asthma incidence (Khreis et al., 2017)",
    "",
    "MEMS & Wearable Architecture:",
    "▪ MEMS optical scattering and MOS sensors provide sufficient sensitivity for personal exposure monitoring (Sousan et al., 2016; Spinelle et al., 2017)",
    "▪ Core wearable layers: Sensing → Processing → Communication → Application (Ko et al., 2010)",
    "▪ Edge computing on ARM Cortex-M4 enables multi-day battery life (Castillo-Escario et al., 2021)",
    "",
    "Precedent System:",
    "▪ Yoo et al. (2018): Wrist-worn PM/VOC system achieved 87.4% accuracy but relied on smartphone pairing (limited standalone functionality)"
])

# Slide 8: Literature Review - Africa/Nigeria
add_content_slide(prs, "Literature Review - African & Nigerian Context", [
    "African Region:",
    "▪ ISAAC study: Asthma prevalence ranges from 2.5% (Ethiopia) to >20% (South Africa), driven by urbanization and biomass fuels (Ait-Khaled et al., 2009)",
    "▪ Low-cost sensor networks successfully deployed in Uganda (Mead et al., 2013) and Ghana via LoRa-WAN (Quayson et al., 2020)",
    "▪ Field calibration in Kenya proved vital for MEMS accuracy in African settings (Ndegwa et al., 2021)",
    "",
    "Nigerian Context:",
    "▪ Weighted adult asthma prevalence of 6.8%, highest in industrial corridors (Obaseki et al., 2016)",
    "▪ Absence of personalized trigger tools in Nigerian tertiary hospitals (Akanbi et al., 2017)",
    "▪ FUTA developed NodeMCU + MQ sensor IoT monitor, but lacked MEMS particulate sensing (Olawale & Adesanya, 2019)",
    "▪ ABU Zaria developed SMS-based alerts for low-connectivity areas (Abdullahi et al., 2020)",
    "▪ NISEPA confirms elevated PM around Chanchaga market/Minna-Bida road (NISEPA, 2022)"
])

# Slide 9: Table Summary
headers = ["Author (Year)", "Method / System", "Location", "Key Achievement", "Key Limitation"]
table_data = [
    ["Yoo et al. (2018)", "Wrist-worn PM/VOC Sensors", "S. Korea", "87.4% trigger detection accuracy", "Relied on smartphone pairing; no edge processing"],
    ["Olawale & Adesanya (2019)", "IoT NodeMCU + MQ Sensors", "Nigeria (FUTA)", "Functional cloud dashboard", "No MEMS PM sensing; not for asthma"],
    ["Quayson et al. (2020)", "LoRa-WAN AQ System", "Ghana", "6-month continuous solar operation", "No wearable form factor"],
    ["Abdullahi et al. (2020)", "SMS-based AQ Alert", "Nigeria (ABU)", "Reached low-connectivity areas", "Limited sensor integration"],
    ["Liu et al. (2019)", "ML Random Forest Classifier", "N/A", "91.3% accuracy on edge microcontroller", "Required pre-labeled environmental datasets"]
]
add_table_slide(prs, "Summary of Reviewed Works", headers, table_data)

# Slide 10: Gaps
add_content_slide(prs, "Identified Research Gaps", [
    "Based on the reviewed literature, three critical gaps exist:",
    "",
    "1. Environmental Specificity: Few MEMS wearable designs are engineered for the West African trigger landscape (biomass combustion, harmattan dust, high ambient humidity).",
    "",
    "2. Spatial Data Deficit: Most African wearable health research lacks GPS-referenced exposure mapping, preventing spatially actionable public health data.",
    "",
    "3. Integration Gap: No published Nigerian study has developed a fully integrated, low-power wearable respiratory shield combining MEMS particulate, VOC, and meteorological sensing with on-device edge processing and exposure mapping."
])

# Slide 11: Expected Contributions
add_content_slide(prs, "Expected Contributions", [
    "EC1: A fully integrated, low-power wearable hardware prototype combining MEMS (PM2.5/PM10, VOCs) and meteorological sensors tailored for the Nigerian environment.",
    "",
    "EC2: An optimized embedded system architecture and firmware utilizing edge computing for real-time, standalone trigger detection and alert generation without mandatory smartphone/cloud dependency.",
    "",
    "EC3: A GPS-referenced spatial exposure mapping framework capable of generating granular, geo-referenced air quality data for personal asthma management and public health policy support in Minna."
])

# Slide 12: References
add_content_slide(prs, "References", [
    "[1] Akanbi, M. O. et al. (2017). The burden of respiratory disease in Nigeria. African Journal of Respiratory Medicine.",
    "[2] Khreis, H. et al. (2017). Exposure to traffic-related air pollution and risk of development of childhood asthma. Environment International.",
    "[3] Ndegwa, J. et al. (2021). Field calibration of MEMS-based low-cost air quality sensors. Journal of Environmental Informatics.",
    "[4] Obaseki, D. O. et al. (2016). Prevalence of asthma in Nigeria: A systematic review. Nigerian Medical Journal.",
    "[5] World Health Organization. (2022). Asthma: Key facts. WHO.",
    "[6] Yoo, H. et al. (2018). A wearable IoT patient monitoring system for asthma management. Sensors and Actuators A: Physical.",
    "[7] Yi, W. J. et al. (2015). A review on MEMS sensors for wearable health monitoring. Sensors."
])

# Slide 13: Thank You
add_end_slide(prs, "Thank You!\n\nQuestions & Discussion")

# Save the file
prs.save('Respiratory_Shield_Presentation.pptx')
print("Presentation successfully created: Respiratory_Shield_Presentation.pptx")