from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from io import BytesIO


def generate_pdf_report(result):
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("ATS Resume Intelligence Report", styles["Title"]))
    story.append(Spacer(1, 0.3 * inch))

    story.append(Paragraph(f"Semantic Match Score: {result.get('semantic_score', 0)}%", styles["Heading2"]))
    story.append(Spacer(1, 0.2 * inch))

    def add_section(title, items):
        story.append(Paragraph(title, styles["Heading2"]))

        if items:
            for item in items:
                story.append(Paragraph(f"- {item}", styles["BodyText"]))
        else:
            story.append(Paragraph("No data available.", styles["BodyText"]))

        story.append(Spacer(1, 0.2 * inch))

    add_section("Matched Skills", result.get("matched_skills", []))
    add_section("Missing Skills", result.get("missing_skills", []))
    add_section("Strengths", result.get("strengths", []))
    add_section("Weaknesses", result.get("weaknesses", []))
    add_section("Suggestions", result.get("suggestions", []))

    doc.build(story)

    buffer.seek(0)
    return buffer