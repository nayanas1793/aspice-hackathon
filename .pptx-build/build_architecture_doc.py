from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.section import WD_SECTION


OUT = r"C:\Users\FLEX\Downloads\aspice-springboot-hackathon\architecture-doc\ASPICE-CI-Architecture.docx"
NAVY = "17324D"
BLUE = "236B8E"
TEAL = "2A8C82"
PALE = "EAF1F5"
PALE2 = "F5F8FA"
INK = "253746"
MUTED = "536777"
WHITE = "FFFFFF"
ACCENT = "D28A2E"


def shade(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = tc_pr.find(qn("w:shd"))
    if shd is None:
        shd = OxmlElement("w:shd")
        tc_pr.append(shd)
    shd.set(qn("w:fill"), fill)


def cell_margins(cell, top=95, start=100, bottom=95, end=100):
    tc = cell._tc
    tc_pr = tc.get_or_add_tcPr()
    margins = tc_pr.first_child_found_in("w:tcMar")
    if margins is None:
        margins = OxmlElement("w:tcMar")
        tc_pr.append(margins)
    for edge, value in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        node = margins.find(qn(f"w:{edge}"))
        if node is None:
            node = OxmlElement(f"w:{edge}")
            margins.append(node)
        node.set(qn("w:w"), str(value))
        node.set(qn("w:type"), "dxa")


def set_repeat_table_header(row):
    tr_pr = row._tr.get_or_add_trPr()
    tbl_header = OxmlElement("w:tblHeader")
    tbl_header.set(qn("w:val"), "true")
    tr_pr.append(tbl_header)


def prevent_row_split(row):
    tr_pr = row._tr.get_or_add_trPr()
    cant_split = OxmlElement("w:cantSplit")
    tr_pr.append(cant_split)


def set_cell_text(cell, text, *, bold=False, color=INK, size=9.2, align=None):
    cell.text = ""
    cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.line_spacing = 1.08
    if align is not None:
        p.alignment = align
    run = p.add_run(text)
    run.bold = bold
    run.font.name = "Aptos"
    run._element.get_or_add_rPr().rFonts.set(qn("w:ascii"), "Aptos")
    run._element.get_or_add_rPr().rFonts.set(qn("w:hAnsi"), "Aptos")
    run.font.size = Pt(size)
    run.font.color.rgb = RGBColor.from_string(color)
    cell_margins(cell)


def format_table(table, widths, header=True, font_size=9.2):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    for row_index, row in enumerate(table.rows):
        prevent_row_split(row)
        if row_index == 0 and header:
            set_repeat_table_header(row)
        for col_index, cell in enumerate(row.cells):
            cell.width = Inches(widths[col_index])
            if row_index == 0 and header:
                shade(cell, NAVY)
                for p in cell.paragraphs:
                    for run in p.runs:
                        run.bold = True
                        run.font.color.rgb = RGBColor.from_string(WHITE)
                        run.font.size = Pt(font_size)
            elif row_index % 2 == 0:
                shade(cell, PALE2)


def add_table(doc, headers, rows, widths, font_size=9.2):
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = "Table Grid"
    for i, text in enumerate(headers):
        set_cell_text(table.rows[0].cells[i], text, bold=True, color=WHITE, size=font_size)
    for values in rows:
        cells = table.add_row().cells
        for i, text in enumerate(values):
            set_cell_text(cells[i], text, size=font_size)
    format_table(table, widths, header=True, font_size=font_size)
    doc.add_paragraph().paragraph_format.space_after = Pt(0)
    return table


def add_bullet(doc, lead, text):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.left_indent = Inches(0.24)
    p.paragraph_format.first_line_indent = Inches(-0.13)
    r = p.add_run(lead)
    r.bold = True
    p.add_run(text)
    return p


def add_callout(doc, label, text, fill=PALE):
    t = doc.add_table(rows=1, cols=1)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.style = "Table Grid"
    c = t.cell(0, 0)
    shade(c, fill)
    cell_margins(c, top=140, start=170, bottom=140, end=170)
    p = c.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    r = p.add_run(label + "  ")
    r.bold = True
    r.font.color.rgb = RGBColor.from_string(BLUE)
    p.add_run(text)
    doc.add_paragraph().paragraph_format.space_after = Pt(1)


def add_heading(doc, text, level=1):
    p = doc.add_paragraph(text, style=f"Heading {level}")
    p.paragraph_format.keep_with_next = True
    return p


doc = Document()
section = doc.sections[0]
section.top_margin = Inches(0.62)
section.bottom_margin = Inches(0.62)
section.left_margin = Inches(0.7)
section.right_margin = Inches(0.7)

styles = doc.styles
normal = styles["Normal"]
normal.font.name = "Aptos"
normal._element.rPr.rFonts.set(qn("w:ascii"), "Aptos")
normal._element.rPr.rFonts.set(qn("w:hAnsi"), "Aptos")
normal.font.size = Pt(10)
normal.font.color.rgb = RGBColor.from_string(INK)
normal.paragraph_format.space_after = Pt(5)
normal.paragraph_format.line_spacing = 1.12

for name, size, color in (("Title", 25, NAVY), ("Heading 1", 16, NAVY), ("Heading 2", 12, BLUE)):
    style = styles[name]
    style.font.name = "Aptos Display" if name == "Title" else "Aptos"
    style._element.rPr.rFonts.set(qn("w:ascii"), style.font.name)
    style._element.rPr.rFonts.set(qn("w:hAnsi"), style.font.name)
    style.font.size = Pt(size)
    style.font.bold = True
    style.font.color.rgb = RGBColor.from_string(color)
    style.paragraph_format.space_before = Pt(10 if name != "Title" else 0)
    style.paragraph_format.space_after = Pt(5)

# Cover and executive architecture overview
p = doc.add_paragraph(style="Title")
p.add_run("ASPICE CI Architecture")
p = doc.add_paragraph()
p.paragraph_format.space_after = Pt(13)
r = p.add_run("Spring Boot hackathon solution | High-level design and job guide")
r.font.name = "Aptos"
r.font.size = Pt(12)
r.font.color.rgb = RGBColor.from_string(MUTED)

add_heading(doc, "Purpose and scope", 1)
doc.add_paragraph(
    "This document explains how the Spring Boot application, GitHub Actions pipeline, evidence artifacts, "
    "Python report generator, and GitHub Pages deployment fit together. The pipeline provides reviewable "
    "engineering evidence for a demonstration; it does not establish ASPICE compliance or certification."
)

add_heading(doc, "Architecture at a glance", 1)
steps = [
    ("APPLICATION", "Spring Boot API\nGET /api/health\nGET /api/status", BLUE),
    ("CI PIPELINE", "Build, test, analyze, scan\nBuild container image", TEAL),
    ("EVIDENCE", "JUnit / JaCoCo\nSBOM / Sonar / Trivy", "4A657A"),
    ("REPORT", "Python combines files\nand job results", ACCENT),
    ("PUBLISH", "HTML + JSON artifact\nGitHub Pages on main", NAVY),
]
t = doc.add_table(rows=1, cols=9)
t.alignment = WD_TABLE_ALIGNMENT.CENTER
t.autofit = False
for idx, (label, body, color) in enumerate(steps):
    cell = t.cell(0, idx * 2 if idx < 4 else 8)
    cell.width = Inches(1.35)
    shade(cell, color)
    cell_margins(cell, top=140, start=100, bottom=140, end=100)
    cell.text = ""
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run(label + "\n")
    r.bold = True
    r.font.size = Pt(8.5)
    r.font.color.rgb = RGBColor.from_string(WHITE)
    r2 = p.add_run(body)
    r2.font.size = Pt(8.4)
    r2.font.color.rgb = RGBColor.from_string(WHITE)
    if idx < 4:
        arrow = t.cell(0, idx * 2 + 1)
        arrow.width = Inches(0.28)
        set_cell_text(arrow, "->", bold=True, color=TEAL, size=10, align=WD_ALIGN_PARAGRAPH.CENTER)
for j in range(1, 9, 2):
    t.cell(0, j).width = Inches(0.28)
for j in (1, 3, 5, 7):
    t.cell(0, j).width = Inches(0.28)
doc.add_paragraph().paragraph_format.space_after = Pt(0)

add_callout(doc, "Key design point", "Jobs run on separate hosted runners. Uploaded workflow artifacts are the handoff between producer jobs and the report job; there is no shared runner filesystem.")

add_heading(doc, "Application and container", 1)
doc.add_paragraph(
    "The application starts from AspiceDemoApplication. HealthController exposes /api/health and the legacy "
    "/api/status route, returning application, status, and timestamp fields as JSON. Actuator exposes its "
    "health and info web endpoints. Maven targets Java 21, packages the JAR, runs tests and coverage, and "
    "provides the Sonar scanner plugin."
)
doc.add_paragraph(
    "The Dockerfile is a two-stage build: Maven and a JDK compile the app in the build stage; a smaller Java "
    "runtime image runs the packaged JAR on port 8080. In the current workflow, Docker performs this build "
    "again inside the container build, so it does not directly consume the JAR downloaded by the Docker job."
)

# Job matrix
doc.add_page_break()
add_heading(doc, "CI jobs and execution rules", 1)
doc.add_paragraph("Jobs without a dependency can run in parallel. A needs dependency normally requires upstream success; job-level conditions can also skip work.")
job_rows = [
    ("Requirement Traceability", "Pull request only; Dev environment", "Finds SCRUM-<number> in PR title/body. Jira API verifies issue in SCRUM and aspice-requirement label. Produces issue-key job output; no code/test conformance check."),
    ("Software Bill of Materials", "Every workflow run; independent", "Trivy filesystem mode writes CycloneDX JSON. Uploads ASPICE-Software-Bill-of-Materials for 90 days."),
    ("Maven Build", "Every workflow run; independent", "Runs clean package with tests skipped, verifies a JAR exists, and uploads the JAR for 7 days."),
    ("JUnit and JaCoCo", "Every workflow run; independent", "Runs mvn clean verify. Publishes JUnit results and uploads JUnit/Failsafe XML and JaCoCo reports for 90 days."),
    ("SonarCloud Analysis", "Needs successful JUnit/JaCoCo; Dev environment", "Submits coverage and source analysis. sonar.qualitygate.wait=true makes a failed Quality Gate fail this job. Saves measures, gate, and issue JSON when available."),
    ("Trivy Filesystem Scan", "Every workflow run; independent", "Scans source tree for configured vulnerability, misconfiguration, and secret findings. Saves JSON; findings alone do not fail the job (exit code 0)."),
    ("Docker Image Build", "Needs successful Maven Build", "Downloads the JAR artifact, builds and saves a Docker image archive. Dockerfile currently rebuilds the app in its own build stage."),
    ("Trivy Docker Image Scan", "Needs successful Docker Image Build", "Loads the image and scans vulnerabilities. Saves JSON; findings alone do not fail the job (exit code 0)."),
    ("Docker Image Push", "Non-PR only; needs successful build and image scan", "Uses GITHUB_TOKEN with package write permission to push SHA and branch tags to GHCR. Skipped for PR events."),
    ("ASPICE Evidence Report", "Runs with always() after listed jobs", "Downloads available evidence, invokes the Python generator, writes Actions summary, and uploads HTML, JSON, and evidence for 90 days."),
    ("Deploy HTML Report", "Only successful report on main push or manual main run", "Publishes the HTML report to GitHub Pages, downloads it to validate the content, and saves a validation copy."),
]
add_table(doc, ["Job", "When / dependency", "Purpose and outcome"], job_rows, [1.48, 1.72, 3.6], font_size=8.25)

add_heading(doc, "Dependency flow", 2)
doc.add_paragraph(
    "Unit Test -> SonarCloud. Maven Build -> Docker Build -> Trivy Image -> Docker Push (non-PR). "
    "SBOM and Trivy Filesystem are independent. The ASPICE report waits for the declared jobs but uses "
    "always() so it can capture partial results. Deployment is downstream of the report."
)

# Evidence map and report generation
doc.add_page_break()
add_heading(doc, "Evidence creation and handoff", 1)
doc.add_paragraph(
    "Producer jobs upload artifacts from their own runners. The ASPICE Evidence Report job downloads those "
    "artifacts into evidence/ before Python runs. The download action creates the destination folders; "
    "there is no separate mkdir evidence command in the workflow."
)
evidence_rows = [
    ("JUnit / JaCoCo", "XML: TEST-*.xml; jacoco.xml", "evidence/tests/", "Test case outcomes and coverage counters"),
    ("SBOM", "JSON: aspice-sbom.cdx.json", "evidence/sbom/", "CycloneDX format, root component, dependency inventory"),
    ("SonarCloud", "JSON: measures, quality gate, issues", "evidence/sonar/", "Quality measures, gate conditions, unresolved issues"),
    ("Trivy filesystem", "JSON: trivy-fs-results.json", "evidence/trivy/<artifact>/", "Filesystem vulnerability, misconfiguration, secret findings"),
    ("Trivy image", "JSON: trivy-image-results.json", "evidence/trivy/<artifact>/", "Container image vulnerability findings"),
    ("Docker build / push", "JAR, image .tar, job outputs", "Artifact handoff / environment", "Image tag and digest; archive feeds scan/push jobs"),
]
add_table(doc, ["Producer", "Output", "Report-job location", "Report use"], evidence_rows, [1.05, 1.8, 1.55, 2.4], font_size=8.25)

add_heading(doc, "Report generator", 1)
doc.add_paragraph(
    "scripts/generate_aspice_report.py reads the downloaded evidence under evidence/ and job-result values "
    "passed by the workflow as environment variables. It parses JUnit and JaCoCo XML, and parses the SBOM, "
    "SonarCloud, and Trivy JSON. Docker image details and Jira issue keys arrive as job outputs/environment "
    "values rather than evidence files."
)
add_table(doc, ["Inputs", "Output"], [
    ("Job statuses, Jira keys, Docker image metadata, XML and JSON evidence files", "aspice-report/aspice-report.html - readable report"),
    ("Same normalized report data", "aspice-report/aspice-report.json - structured report for tools and later processing"),
], [3.65, 3.15], font_size=9)
doc.add_paragraph(
    "Missing or malformed evidence is generally represented as unavailable/empty so the report can describe "
    "partial runs. The report generator summarizes automated evidence; it does not determine whether the code "
    "satisfies a Jira requirement."
)

# Event matrix, gates, practical configuration
doc.add_page_break()
add_heading(doc, "Triggers, gates, and publication", 1)
trigger_rows = [
    ("Push", "main, develop, feature/**, codex/**", "Build, tests, scans, report. Image push is eligible after build and image scan succeed. Pages deployment only for main."),
    ("Pull request", "Target branch main; opened, synchronize, reopened, edited", "Requirement check runs. Build, tests, scans and report run. Docker push and Pages deployment are skipped."),
    ("Manual dispatch", "Branch selected by person starting the run", "Pipeline runs on that branch. Docker push can run after required jobs succeed; Pages deployment only when selected branch is main."),
]
add_table(doc, ["Event", "Scope", "Expected behavior"], trigger_rows, [1.0, 2.0, 3.8], font_size=8.8)

add_heading(doc, "What blocks progress", 2)
add_bullet(doc, "Requirement check: ", "fails if Jira secrets are unavailable, no SCRUM key is found, Jira cannot return the issue, the project is wrong, or the aspice-requirement label is absent.")
add_bullet(doc, "Tests and Sonar: ", "test/build failures stop dependent jobs; the Sonar Quality Gate is enforced. Environment protection rules can pause jobs that need Dev secrets until approved.")
add_bullet(doc, "Trivy: ", "configured findings are retained as evidence but do not alone fail scans because exit-code is 0. Scanner/action errors can still fail a job.")
add_bullet(doc, "Container publication: ", "Docker Push is skipped on PRs and requires both Docker Build and Trivy Image to succeed. It needs packages: write permission.")
add_bullet(doc, "Report and deployment: ", "the report attempts to run after upstream failures. Pages deployment requires a successful report and a main push or manual main run.")

add_heading(doc, "Configuration notes", 2)
add_bullet(doc, "Jira: ", "JIRA_BASE_URL, JIRA_EMAIL, and JIRA_API_TOKEN are expected in the GitHub Dev environment. The project key SCRUM is configured in the workflow; update it and the PR issue references together if the Jira key changes.")
add_bullet(doc, "Report links: ", "JIRA_BASE_URL is passed to the report job, but that job does not currently select the Dev environment. If the URL is only an environment secret, the report may show Jira keys without clickable links.")
add_bullet(doc, "ASPICE status: ", "the report provides traceability and engineering evidence for this demo. An assessor or organization process is still needed to evaluate process compliance.")

doc.core_properties.title = "ASPICE CI Architecture"
doc.core_properties.subject = "High-level architecture and GitHub Actions job guide for the Spring Boot ASPICE hackathon solution"
doc.core_properties.author = ""
doc.save(OUT)
print(OUT)
