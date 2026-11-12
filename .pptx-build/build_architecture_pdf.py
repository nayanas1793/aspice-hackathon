from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from xml.sax.saxutils import escape
import os


OUT = r"C:\Users\FLEX\Downloads\aspice-springboot-hackathon\output\pdf\ASPICE-CI-Architecture.pdf"
os.makedirs(os.path.dirname(OUT), exist_ok=True)

NAVY = colors.HexColor("#17324D")
BLUE = colors.HexColor("#236B8E")
TEAL = colors.HexColor("#2A8C82")
PALE = colors.HexColor("#EAF1F5")
PALE2 = colors.HexColor("#F5F8FA")
INK = colors.HexColor("#253746")
MUTED = colors.HexColor("#536777")
ORANGE = colors.HexColor("#D28A2E")
WHITE = colors.white

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="DocTitle", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=23, leading=27, textColor=NAVY, alignment=TA_LEFT, spaceAfter=5))
styles.add(ParagraphStyle(name="Subtitle", parent=styles["Normal"], fontName="Helvetica", fontSize=10, leading=14, textColor=MUTED, spaceAfter=14))
styles.add(ParagraphStyle(name="H1x", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=15, leading=18, textColor=NAVY, spaceBefore=8, spaceAfter=6, keepWithNext=True))
styles.add(ParagraphStyle(name="H2x", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=10.5, leading=13, textColor=BLUE, spaceBefore=6, spaceAfter=4, keepWithNext=True))
styles.add(ParagraphStyle(name="Bodyx", parent=styles["BodyText"], fontName="Helvetica", fontSize=9.2, leading=13, textColor=INK, spaceAfter=6))
styles.add(ParagraphStyle(name="Smallx", parent=styles["BodyText"], fontName="Helvetica", fontSize=7.5, leading=9.4, textColor=INK))
styles.add(ParagraphStyle(name="Cellx", parent=styles["BodyText"], fontName="Helvetica", fontSize=7.8, leading=9.7, textColor=INK))
styles.add(ParagraphStyle(name="HeadCellx", parent=styles["BodyText"], fontName="Helvetica-Bold", fontSize=7.8, leading=9.5, textColor=WHITE))
styles.add(ParagraphStyle(name="FlowHead", parent=styles["BodyText"], fontName="Helvetica-Bold", fontSize=8, leading=10, textColor=WHITE, alignment=TA_CENTER))
styles.add(ParagraphStyle(name="FlowBody", parent=styles["BodyText"], fontName="Helvetica", fontSize=7.6, leading=9.2, textColor=WHITE, alignment=TA_CENTER))
styles.add(ParagraphStyle(name="Arrowx", parent=styles["BodyText"], fontName="Helvetica-Bold", fontSize=11, leading=12, textColor=TEAL, alignment=TA_CENTER))


def P(text, style="Bodyx"):
    return Paragraph(text, styles[style])


def cell(text, header=False):
    return P(text, "HeadCellx" if header else "Cellx")


def table(data, widths, header=True, font=7.8):
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0, hAlign="LEFT")
    commands = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#C9D4DC")),
    ]
    if header:
        commands.append(("BACKGROUND", (0, 0), (-1, 0), NAVY))
        for r in range(1, len(data)):
            if r % 2 == 0:
                commands.append(("BACKGROUND", (0, r), (-1, r), PALE2))
    t.setStyle(TableStyle(commands))
    return t


def footer(canvas, doc):
    canvas.saveState()
    width, height = A4
    canvas.setStrokeColor(colors.HexColor("#D8E0E6"))
    canvas.setLineWidth(0.5)
    canvas.line(18 * mm, 14 * mm, width - 18 * mm, 14 * mm)
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(18 * mm, 9 * mm, "ASPICE CI architecture | Spring Boot hackathon demonstration")
    canvas.drawRightString(width - 18 * mm, 9 * mm, f"Page {doc.page}")
    canvas.restoreState()


doc = SimpleDocTemplate(OUT, pagesize=A4, rightMargin=18 * mm, leftMargin=18 * mm, topMargin=16 * mm, bottomMargin=19 * mm, title="ASPICE CI Architecture", author="")
story = []

# Page 1: purpose and system architecture
story += [P("ASPICE CI Architecture", "DocTitle"), P("High-level design and job guide for the Spring Boot hackathon solution", "Subtitle")]
story += [P("Purpose and scope", "H1x"), P("This document explains how the Spring Boot service, GitHub Actions pipeline, evidence artifacts, Python report generator, and GitHub Pages deployment fit together. The pipeline provides reviewable engineering evidence for a demonstration; it does not establish ASPICE compliance or certification.")]
story += [P("Architecture overview", "H1x")]
flow = []
stages = [
    ("APPLICATION", "Spring Boot API<br/>Health and status routes", BLUE),
    ("CI PIPELINE", "Build, test, analyze,<br/>scan, package", TEAL),
    ("EVIDENCE", "JUnit / JaCoCo<br/>SBOM / Sonar / Trivy", colors.HexColor("#4A657A")),
    ("REPORT", "Python reads files<br/>and job results", ORANGE),
    ("PUBLISH", "HTML + JSON artifact<br/>Pages on main", NAVY),
]
for i, (head, body, color) in enumerate(stages):
    if i:
        flow.append(P("-&gt;", "Arrowx"))
    flow.append(Table([[P(head, "FlowHead")], [P(body, "FlowBody")]], colWidths=[29 * mm], rowHeights=[9 * mm, 16 * mm], style=TableStyle([("BACKGROUND", (0, 0), (-1, -1), color), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3), ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2)])))
story.append(Table([flow], colWidths=[29 * mm if i % 2 == 0 else 6 * mm for i in range(9)], hAlign="LEFT", style=TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LEFTPADDING", (0, 0), (-1, -1), 1), ("RIGHTPADDING", (0, 0), (-1, -1), 1), ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2)])))
story.append(Spacer(1, 6))
story.append(table([[P("Job isolation", "Cellx"), P("Each GitHub Actions job runs in its own hosted workspace. Producer jobs upload artifacts; the report job downloads them. There is no shared runner filesystem.", "Cellx")]], [35 * mm, 139 * mm], header=False))
story += [P("Application and container", "H1x"), P("AspiceDemoApplication starts Spring Boot. HealthController maps GET /api/health and the compatibility route GET /api/status to a JSON response containing application, status, and timestamp. Actuator exposes health and info endpoints. Maven targets Java 21 and packages the service; tests verify the custom health response.")]
story.append(P("The Dockerfile uses two stages: Maven and a JDK build the application, then a smaller Java runtime image runs the JAR on port 8080. The current CI Docker job downloads a Maven JAR, but the Dockerfile builds another JAR inside its own build stage; it does not copy the downloaded JAR.", "Bodyx"))

# Page 2: jobs
story.append(PageBreak())
story += [P("CI jobs and execution rules", "DocTitle"), P("Jobs without a dependency can run in parallel. A needs dependency normally requires upstream success; job conditions can also skip work.", "Subtitle")]
jobs = [
    ("Requirement Traceability", "PR only; Dev environment", "Extracts SCRUM-<number> from PR title/body. Jira API checks project SCRUM and the aspice-requirement label. Validates traceability metadata, not code correctness."),
    ("Software Bill of Materials", "Every run; independent", "Trivy filesystem mode creates CycloneDX JSON. Uploads the SBOM artifact for 90 days."),
    ("Maven Build", "Every run; independent", "Runs clean package with tests skipped, verifies a JAR exists, uploads it for 7 days."),
    ("JUnit and JaCoCo", "Every run; independent", "Runs mvn clean verify. Publishes JUnit results and uploads XML test reports plus JaCoCo reports for 90 days."),
    ("SonarCloud Analysis", "Needs successful tests; Dev", "Submits source and coverage analysis. Quality Gate is enforced with sonar.qualitygate.wait=true. Saves measures, gate, and issue JSON when available."),
    ("Trivy Filesystem Scan", "Every run; independent", "Scans configured vulnerability, misconfiguration, and secret categories. Saves JSON. Findings alone do not fail the scan (exit-code 0)."),
    ("Docker Image Build", "Needs Maven Build success", "Downloads the JAR artifact, builds the Docker image and saves an image archive for later scan/push jobs."),
    ("Trivy Docker Image Scan", "Needs Docker Build success", "Loads the image and scans vulnerabilities. Saves JSON. Findings alone do not fail the scan (exit-code 0)."),
    ("Docker Image Push", "Non-PR; build and image scan succeed", "Uses GITHUB_TOKEN with package write permission to push commit-SHA and branch tags to GHCR. Skipped on PRs."),
    ("ASPICE Evidence Report", "Always after listed jobs", "Downloads available artifacts, runs Python, writes an Actions summary, and uploads the HTML, JSON, and evidence for 90 days."),
    ("Deploy HTML Report", "Successful report; main push/manual main", "Publishes the report to GitHub Pages, downloads it for a content check, and stores a validation copy."),
]
job_data = [[cell("Job", True), cell("When / dependency", True), cell("Purpose and outcome", True)]]
job_data += [[cell(a), cell(b), cell(c)] for a, b, c in jobs]
story.append(table(job_data, [43 * mm, 46 * mm, 85 * mm], font=7.4))
story += [P("Dependency path", "H2x"), P("Unit Test -> SonarCloud. Maven Build -> Docker Build -> Trivy Image -> Docker Push (non-PR). SBOM and Trivy Filesystem are independent. The report waits for its declared jobs but uses always() to record partial results. Deployment follows the report.")]

# Page 3: artifact flow and report generator
story.append(PageBreak())
story += [P("Evidence flow and report generation", "DocTitle"), P("The report job downloads artifacts into evidence/ before the generator runs. The download action creates the destination folders; the workflow does not need a separate mkdir evidence command.", "Subtitle")]
evidence = [
    ("JUnit / JaCoCo", "XML: TEST-*.xml and jacoco.xml", "evidence/tests/", "Test cases and coverage metrics"),
    ("SBOM", "JSON: aspice-sbom.cdx.json", "evidence/sbom/", "CycloneDX components, versions, licenses, package URLs"),
    ("SonarCloud", "JSON: measures, quality gate, issues", "evidence/sonar/", "Measures, gate conditions, unresolved issues"),
    ("Trivy filesystem", "JSON: trivy-fs-results.json", "evidence/trivy/{artifact}/", "Filesystem vulnerability, misconfiguration, secret findings"),
    ("Trivy image", "JSON: trivy-image-results.json", "evidence/trivy/{artifact}/", "Container image vulnerability findings"),
    ("Docker build / push", "JAR, image .tar, job outputs", "Artifact handoff / outputs", "Image archive feeds scan/push; image tag and digest feed report"),
]
ev_data = [[cell("Producer", True), cell("Output / type", True), cell("Report location", True), cell("Report use", True)]]
ev_data += [[cell(a), cell(b), cell(c), cell(d)] for a,b,c,d in evidence]
story.append(table(ev_data, [30 * mm, 48 * mm, 39 * mm, 57 * mm], font=7.5))
story += [P("Python report generator", "H1x"), P("scripts/generate_aspice_report.py combines downloaded files under evidence/ with job-result values passed by the workflow. It parses JUnit and JaCoCo XML, plus the SBOM, SonarCloud, and Trivy JSON. Jira issue keys, Docker metadata, and job states arrive through workflow outputs/environment values rather than files in evidence/.")]
outputs = [
    [cell("Generated file", True), cell("Purpose", True)],
    [cell("aspice-report/aspice-report.html"), cell("Readable report with pipeline metadata, job results, traceability, tests, coverage, Sonar, SBOM, Trivy, Docker details, evidence map." )],
    [cell("aspice-report/aspice-report.json"), cell("Structured representation of the same report data for later processing." )],
]
story.append(table(outputs, [62 * mm, 112 * mm]))
story.append(Spacer(1, 5))
story.append(table([[cell("Missing evidence", True), cell("Artifact downloads are allowed to continue when files are missing. The generator generally marks data unavailable or empty so the report can describe a partial run.")]], [35 * mm, 139 * mm], header=False))

# Page 4: triggers, gates, boundaries
story.append(PageBreak())
story += [P("Triggers, gates, and operating notes", "DocTitle"), P("The event type controls which conditional jobs are enabled. A skipped job often means its condition was not met, rather than an execution failure.", "Subtitle")]
trigger_rows = [
    ("Push", "main, develop, feature/**, codex/**", "Build, tests, scans, and report run. Image push is eligible after build and image scan succeed. Pages deploys only for main."),
    ("Pull request", "Target main; opened, synchronize, reopened, edited", "Requirement check plus build, tests, scans, and report. Docker push and Pages deployment are skipped."),
    ("Manual dispatch", "Branch selected by the person starting the run", "Pipeline runs on the selected branch. Docker push can run after its gates; Pages deployment requires main."),
]
tr_data = [[cell("Event", True), cell("Scope", True), cell("Expected behavior", True)]]
tr_data += [[cell(a), cell(b), cell(c)] for a,b,c in trigger_rows]
story.append(table(tr_data, [30 * mm, 54 * mm, 90 * mm]))
story += [P("Success and skip behavior", "H1x")]
story.append(table([
    [cell("Check", True), cell("Behavior", True)],
    [cell("Jira traceability"), cell("Fails when secrets are unavailable, no SCRUM key is present, the issue cannot be retrieved, the project is not SCRUM, or the aspice-requirement label is missing." )],
    [cell("Unit tests / Sonar"), cell("Test failure blocks Sonar because Sonar needs the test job. A failed Sonar Quality Gate fails the Sonar job." )],
    [cell("Trivy scans"), cell("Findings are retained as evidence but do not alone fail scans because exit-code is set to 0. Scanner/action execution errors may still fail." )],
    [cell("Docker push"), cell("Skipped for pull requests. Requires successful Docker build and image scan, plus packages: write permission." )],
    [cell("Report / deployment"), cell("Report attempts to run after upstream results. Pages deploys only if report succeeds on a main push or manual main run." )],
], [38 * mm, 136 * mm]))
story += [P("Configuration and boundaries", "H1x")]
story.append(P("Jira credentials JIRA_BASE_URL, JIRA_EMAIL, and JIRA_API_TOKEN are expected in the GitHub Dev environment. The workflow hardcodes the Jira project key as SCRUM, so a project-key change requires updating the workflow and PR references. The report job receives Jira issue keys, but does not select Dev; if JIRA_BASE_URL exists only as a Dev environment secret, the report may show keys without clickable Jira links.", "Bodyx"))
story.append(P("The report is engineering evidence for this demonstration. It does not verify that implementation behavior meets a requirement, and it is not an ASPICE compliance or certification determination.", "Bodyx"))

doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(OUT)
