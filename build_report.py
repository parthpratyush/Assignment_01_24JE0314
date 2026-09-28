from pathlib import Path
import csv
from datetime import date

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle,
    PageBreak, KeepTogether
)

ROOT = Path(__file__).resolve().parent
FIG = ROOT / "figures"
OUT = ROOT / "REPORT.pdf"
RESULTS = ROOT / "results.csv"

student = "Pratyush Singh Parmar"
roll = "24JE0314"

def read_results():
    values = {}
    with RESULTS.open(newline="") as handle:
        for row in csv.reader(handle):
            if row and row[0] != "quantity":
                values[row[0]] = float(row[1])
    return values

def page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.grey)
    canvas.drawString(2.0 * cm, 1.2 * cm, "Viscous Flow - Assignment 01")
    canvas.drawRightString(A4[0] - 2.0 * cm, 1.2 * cm, f"Page {doc.page}")
    canvas.restoreState()

results = read_results()

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name="CoverTitle", parent=styles["Title"], fontName="Helvetica-Bold",
    fontSize=22, leading=27, alignment=TA_CENTER, spaceAfter=18
))
styles.add(ParagraphStyle(
    name="CoverSub", parent=styles["Normal"], fontName="Helvetica",
    fontSize=12, leading=18, alignment=TA_CENTER, textColor=colors.HexColor("#444444")
))
styles.add(ParagraphStyle(
    name="Section", parent=styles["Heading1"], fontName="Helvetica-Bold",
    fontSize=15, leading=19, spaceBefore=8, spaceAfter=8, textColor=colors.HexColor("#17365D")
))
styles.add(ParagraphStyle(
    name="Subsection", parent=styles["Heading2"], fontName="Helvetica-Bold",
    fontSize=11.5, leading=15, spaceBefore=7, spaceAfter=5, textColor=colors.HexColor("#315F87")
))
styles.add(ParagraphStyle(
    name="Body2", parent=styles["BodyText"], fontName="Helvetica",
    fontSize=9.5, leading=14, spaceAfter=7
))
styles.add(ParagraphStyle(
    name="Eq", parent=styles["BodyText"], fontName="Courier",
    fontSize=9.5, leading=14, leftIndent=22, rightIndent=22,
    spaceBefore=5, spaceAfter=8, backColor=colors.HexColor("#F5F7FA")
))
styles.add(ParagraphStyle(
    name="Caption2", parent=styles["Normal"], fontSize=8.5, leading=11,
    alignment=TA_CENTER, textColor=colors.HexColor("#555555"), spaceAfter=8
))

story = []

story.append(Spacer(1, 2.0 * cm))
story.append(Paragraph("NUMERICAL INVESTIGATION OF<br/>STAGNATION-POINT BOUNDARY-LAYER FLOW", styles["CoverTitle"]))
story.append(Paragraph("Viscous Flow - Assignment 01", styles["CoverSub"]))
story.append(Spacer(1, 1.0 * cm))
story.append(Paragraph(f"<b>Student:</b> {student}", styles["CoverSub"]))
story.append(Paragraph(f"<b>Roll No.:</b> {roll}", styles["CoverSub"]))
story.append(Paragraph("IIT (ISM) Dhanbad", styles["CoverSub"]))
story.append(Spacer(1, 1.0 * cm))
story.append(Image(str(FIG / "stagnation_flow_schematic.png"), width=15.4*cm, height=7.2*cm))
story.append(Spacer(1, 0.35 * cm))
story.append(Paragraph(
    "A numerical study comparing direct boundary-value collocation, "
    "Newton shooting with adaptive IVP integration, and fixed-step RK4 shooting "
    "with a propagated sensitivity equation.",
    styles["CoverSub"]
))
story.append(PageBreak())

story.append(Paragraph("1. Objective", styles["Section"]))
story.append(Paragraph(
    "The objective of this assignment is to obtain the similarity solution of the "
    "two-dimensional stagnation-point boundary layer and to examine the consistency "
    "of several numerical solution strategies. The problem is a nonlinear third-order "
    "boundary-value problem in the similarity coordinate eta.",
    styles["Body2"]
))
story.append(Paragraph("Governing similarity equation", styles["Subsection"]))
story.append(Paragraph(
    "f''' + f f'' - (f')² + 1 = 0", styles["Eq"]
))
story.append(Paragraph("Boundary conditions", styles["Subsection"]))
story.append(Paragraph(
    "f(0) = 0     (impermeable wall)<br/>"
    "f'(0) = 0    (no-slip condition)<br/>"
    "f'(infinity) = 1    (matching with the outer flow)",
    styles["Eq"]
))
story.append(Paragraph(
    "For numerical work, the semi-infinite domain is truncated at eta_infinity = 7. "
    "The main quantity extracted from the solution is the dimensionless wall-shear "
    "parameter f''(0).",
    styles["Body2"]
))

story.append(Paragraph("2. First-Order Form", styles["Section"]))
story.append(Paragraph(
    "Introducing y1 = f, y2 = f' and y3 = f'' converts the third-order equation "
    "to the system below.",
    styles["Body2"]
))
story.append(Paragraph(
    "y1' = y2<br/>"
    "y2' = y3<br/>"
    "y3' = y2² - y1 y3 - 1",
    styles["Eq"]
))

story.append(Paragraph("3. Numerical Methods", styles["Section"]))
story.append(Paragraph("3.1 Direct BVP collocation", styles["Subsection"]))
story.append(Paragraph(
    "The complete boundary-value problem is solved directly with a collocation-based "
    "BVP solver. A smooth tanh-type velocity estimate is used as the initial profile, "
    "after which the solver refines the mesh where the solution requires additional "
    "resolution.",
    styles["Body2"]
))
story.append(Paragraph("3.2 IVP shooting and Newton-Raphson correction", styles["Subsection"]))
story.append(Paragraph(
    "The unknown initial value s = f''(0) is treated as a shooting parameter. "
    "For a trial s, the equations are integrated from eta = 0 to eta = 7 and the "
    "terminal residual is defined as",
    styles["Body2"]
))
story.append(Paragraph("R(s) = f'(7; s) - 1", styles["Eq"]))
story.append(Paragraph(
    "Newton's method then updates the shooting parameter using "
    "s(next) = s - R(s)/R'(s). The derivative is evaluated using a small forward "
    "perturbation in the shooting parameter.",
    styles["Body2"]
))
story.append(Paragraph("3.3 Fixed-step RK4 with sensitivity", styles["Subsection"]))
story.append(Paragraph(
    "A classical fourth-order Runge-Kutta integrator is implemented explicitly. "
    "In addition to the physical variables, the sensitivities of f, f' and f'' "
    "with respect to the shooting parameter are integrated simultaneously. "
    "This supplies the Newton derivative from the same numerical trajectory and "
    "provides an independent implementation of the shooting method.",
    styles["Body2"]
))

story.append(PageBreak())
story.append(Paragraph("4. Boundary-Layer Quantities", styles["Section"]))
story.append(Paragraph(
    "The converged velocity profile provides several standard dimensionless measures. "
    "The displacement thickness, momentum thickness and shape factor are evaluated as",
    styles["Body2"]
))
story.append(Paragraph(
    "delta* = integral[0, eta_infinity] (1 - f') d eta<br/>"
    "theta  = integral[0, eta_infinity] f'(1 - f') d eta<br/>"
    "H = delta* / theta",
    styles["Eq"]
))
story.append(Paragraph(
    "The 99 percent boundary-layer thickness delta_99 is obtained by linear "
    "interpolation at the point where f'(eta) = 0.99.",
    styles["Body2"]
))

story.append(Paragraph("5. Numerical Results", styles["Section"]))
table_data = [
    ["Method", "f''(0)", "Abs. error vs ref."],
    ["Direct BVP", f"{results['Direct BVP f\'\'(0)']:.12f}", f"{abs(results['Direct BVP f\'\'(0)']-results['Reference f\'\'(0)']):.2e}"],
    ["IVP + Newton", f"{results['IVP + Newton f\'\'(0)']:.12f}", f"{abs(results['IVP + Newton f\'\'(0)']-results['Reference f\'\'(0)']):.2e}"],
    ["RK4 + sensitivity", f"{results['RK4 + sensitivity f\'\'(0)']:.12f}", f"{abs(results['RK4 + sensitivity f\'\'(0)']-results['Reference f\'\'(0)']):.2e}"],
    ["Reference", f"{results['Reference f\'\'(0)']:.12f}", "-"],
]
tbl = Table(table_data, colWidths=[7.0*cm, 4.0*cm, 4.2*cm], repeatRows=1)
tbl.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#17365D")),
    ("TEXTCOLOR", (0,0), (-1,0), colors.white),
    ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
    ("ALIGN", (1,1), (-1,-1), "RIGHT"),
    ("FONTNAME", (0,1), (-1,-1), "Helvetica"),
    ("FONTSIZE", (0,0), (-1,-1), 8.5),
    ("GRID", (0,0), (-1,-1), 0.35, colors.HexColor("#B7C3D0")),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#F5F7FA")]),
    ("TOPPADDING", (0,0), (-1,-1), 6),
    ("BOTTOMPADDING", (0,0), (-1,-1), 6),
]))
story.append(tbl)
story.append(Spacer(1, 0.25*cm))
props = [
    ["Quantity", "Value"],
    ["delta_99", f"{results['delta_99']:.6f}"],
    ["Displacement thickness delta*", f"{results['displacement_thickness']:.6f}"],
    ["Momentum thickness theta", f"{results['momentum_thickness']:.6f}"],
    ["Shape factor H", f"{results['shape_factor']:.6f}"],
]
pt = Table(props, colWidths=[9.2*cm, 6.0*cm], repeatRows=1)
pt.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#315F87")),
    ("TEXTCOLOR", (0,0), (-1,0), colors.white),
    ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
    ("ALIGN", (1,1), (-1,-1), "RIGHT"),
    ("FONTSIZE", (0,0), (-1,-1), 8.5),
    ("GRID", (0,0), (-1,-1), 0.35, colors.HexColor("#B7C3D0")),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#F5F7FA")]),
    ("TOPPADDING", (0,0), (-1,-1), 5),
    ("BOTTOMPADDING", (0,0), (-1,-1), 5),
]))
story.append(pt)

story.append(Spacer(1, 0.35*cm))
story.append(Paragraph("The three approaches give nearly indistinguishable similarity profiles.", styles["Body2"]))
story.append(Image(str(FIG / "solution_profiles.png"), width=17.0*cm, height=5.25*cm))
story.append(Paragraph("Figure 1. Similarity function, velocity and shear profiles.", styles["Caption2"]))

story.append(PageBreak())
story.append(Paragraph("6. Convergence and Sensitivity Studies", styles["Section"]))
story.append(Image(str(FIG / "newton_convergence.png"), width=13.8*cm, height=9.1*cm))
story.append(Paragraph("Figure 2. Newton-Raphson residual reduction for the two shooting formulations.", styles["Caption2"]))
story.append(Image(str(FIG / "domain_truncation.png"), width=13.8*cm, height=9.1*cm))
story.append(Paragraph("Figure 3. Effect of the finite computational endpoint eta_infinity.", styles["Caption2"]))

story.append(PageBreak())
story.append(Paragraph("7. RK4 Refinement and Derived Quantities", styles["Section"]))
story.append(Image(str(FIG / "rk4_refinement.png"), width=13.8*cm, height=9.1*cm))
story.append(Paragraph("Figure 4. Fixed-step RK4 refinement study with an O(h^4) reference trend.", styles["Caption2"]))
story.append(Image(str(FIG / "wall_shear_error.png"), width=13.8*cm, height=8.2*cm))
story.append(Paragraph("Figure 5. Deviation of the computed wall shear from the reference value.", styles["Caption2"]))

story.append(PageBreak())
story.append(Paragraph("8. Boundary-Layer Measures and Flow Configuration", styles["Section"]))
story.append(Image(str(FIG / "boundary_layer_measures.png"), width=14.0*cm, height=8.2*cm))
story.append(Paragraph("Figure 6. Dimensionless boundary-layer measures extracted from the RK4 solution.", styles["Caption2"]))
story.append(Image(str(FIG / "stagnation_flow_schematic.png"), width=14.0*cm, height=6.4*cm))
story.append(Paragraph("Figure 7. Two-dimensional stagnation-point flow schematic used to interpret the similarity solution.", styles["Caption2"]))

story.append(Paragraph("9. Discussion", styles["Section"]))
story.append(Paragraph(
    "The three numerical formulations converge to essentially the same wall-shear parameter, "
    "providing a cross-check between direct and shooting formulations. Direct BVP collocation "
    "solves the boundary conditions simultaneously, whereas shooting converts the unknown wall "
    "shear into a scalar root-finding problem. The sensitivity-based RK4 implementation is "
    "particularly transparent because the Newton derivative is propagated as part of the "
    "state vector rather than reconstructed from separate solves.",
    styles["Body2"]
))
story.append(Paragraph(
    "The computational-domain study shows the influence of replacing infinity with a finite endpoint. "
    "Once the endpoint is sufficiently far into the outer-flow region, the wall-shear estimate changes "
    "very little. The RK4 refinement study provides an additional consistency check on the fixed-step "
    "implementation and its expected fourth-order behavior.",
    styles["Body2"]
))

story.append(Paragraph("10. Conclusion", styles["Section"]))
story.append(Paragraph(
    "The stagnation-point similarity problem was solved using direct collocation, adaptive IVP "
    "shooting with Newton correction, and a fixed-step RK4 sensitivity formulation. The calculated "
    "wall-shear parameter is 1.23258766 to the displayed precision, and the associated boundary-layer "
    "integral quantities are reproduced consistently. The repository contains the numerical source, "
    "figures, tabulated results, and this report so that the complete calculation can be reproduced.",
    styles["Body2"]
))

story.append(Paragraph("References", styles["Section"]))
for ref in [
    "H. Schlichting and K. Gersten, Boundary-Layer Theory, Springer.",
    "F. M. White, Viscous Fluid Flow, McGraw-Hill.",
    "V. M. Falkner and S. W. Skan, Some approximate solutions of the boundary layer equations, Philosophical Magazine."
]:
    story.append(Paragraph("• " + ref, styles["Body2"]))

doc = SimpleDocTemplate(
    str(OUT), pagesize=A4,
    rightMargin=1.7*cm, leftMargin=1.7*cm,
    topMargin=1.6*cm, bottomMargin=1.8*cm,
    title="Numerical Investigation of Stagnation-Point Boundary-Layer Flow",
    author=student,
)
doc.build(story, onFirstPage=page_number, onLaterPages=page_number)
print(f"Built {OUT}")
