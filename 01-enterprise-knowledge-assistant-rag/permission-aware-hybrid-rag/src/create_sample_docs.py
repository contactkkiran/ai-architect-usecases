import json
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

OUT = Path("data/pdfs")
OUT.mkdir(parents=True, exist_ok=True)

styles = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=styles["Heading1"], fontSize=18, spaceAfter=8)
H2 = ParagraphStyle(
    "H2", parent=styles["Heading2"], fontSize=13, spaceBefore=12, spaceAfter=4
)
BODY = ParagraphStyle("Body", parent=styles["BodyText"], fontSize=10, leading=14)
CELL = ParagraphStyle("Cell", parent=BODY, fontSize=9, leading=12)
CELLH = ParagraphStyle(
    "CellH", parent=CELL, textColor=colors.white, fontName="Helvetica-Bold"
)


def h1(text):
    return Paragraph(text, H1)


def h2(text):
    return Paragraph(text, H2)


def p(text):
    return Paragraph(text, BODY)


def table(rows, widths_mm):
    """rows[0] is the header row. Cells are Paragraphs so long text wraps."""
    data = [[Paragraph(c, CELLH) for c in rows[0]]]
    data += [[Paragraph(c, CELL) for c in r] for r in rows[1:]]
    t = Table(data, colWidths=[w * mm for w in widths_mm], repeatRows=1)
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F3A5F")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [colors.white, colors.HexColor("#F2F5F9")],
                ),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return t


def doc_control(meta):
    """Document-control table that real policies carry on page 1."""
    rows = [
        ["Document ID", "Owner", "Version", "Effective date", "Classification"],
        [
            meta["doc_id"],
            meta["owner"],
            str(meta["version"]),
            meta["effective_date"],
            meta["classification"],
        ],
    ]
    return table(rows, [30, 45, 20, 35, 40])


def build(meta, story):
    def decorate(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.grey)
        canvas.drawString(20 * mm, 287 * mm, f"Northwind Systems  |  {meta['title']}")
        canvas.drawRightString(190 * mm, 287 * mm, meta["doc_id"])
        canvas.drawString(
            20 * mm,
            10 * mm,
            f"{meta['classification']} - printed copies are uncontrolled",
        )
        canvas.drawRightString(190 * mm, 10 * mm, f"Page {doc.page}")
        canvas.restoreState()

    pdf = SimpleDocTemplate(
        str(OUT / meta["filename"]),
        pagesize=A4,
        leftMargin=20 * mm,
        rightMargin=20 * mm,
        topMargin=25 * mm,
        bottomMargin=20 * mm,
        title=meta["title"],
    )
    pdf.build(story, onFirstPage=decorate, onLaterPages=decorate)
    print("Created:", OUT / meta["filename"])


# ---------------------------------------------------------------- documents
REGISTRY = []


def register(meta):
    REGISTRY.append(
        {
            k: meta[k]
            for k in [
                "doc_id",
                "filename",
                "title",
                "department",
                "version",
                "effective_date",
                "allowed_groups",
            ]
        }
    )


# 1. Leave policy -------------------------------------------------------------
m = dict(
    doc_id="HR-001",
    filename="leave-policy.pdf",
    title="Leave Policy",
    department="HR",
    owner="HR Operations",
    version=3,
    effective_date="2026-01-01",
    classification="Internal",
    allowed_groups="all-employees",
)
register(m)
build(
    m,
    [
        h1(m["title"]),
        doc_control(m),
        Spacer(1, 6),
        h2("1. Purpose and Scope"),
        p(
            "This policy defines paid leave entitlements for all full-time employees of "
            "Northwind Systems. Contractors and interns are covered by their agreements."
        ),
        h2("2. Annual Leave Entitlement"),
        p(
            "Annual leave increases with length of service, as shown in Table 1. Leave accrues "
            "monthly and is credited on 1 January each year."
        ),
        table(
            [
                [
                    "Length of service",
                    "Annual leave (days)",
                    "Maximum carry-forward (days)",
                ],
                ["Less than 2 years", "20", "5"],
                ["2 to 5 years", "24", "10"],
                ["More than 5 years", "28", "10"],
            ],
            [60, 50, 60],
        ),
        Spacer(1, 4),
        p(
            "Carried-forward days expire on 31 March. Leave requests longer than 10 consecutive "
            "working days require approval from the department head."
        ),
        h2("3. Sick Leave"),
        p(
            "Employees receive 12 days of paid sick leave per calendar year. A medical certificate "
            "is required for absences longer than 3 consecutive days. Unused sick leave does not "
            "carry forward."
        ),
        h2("4. Parental Leave"),
        table(
            [
                ["Caregiver type", "Paid leave", "Must start within"],
                ["Primary caregiver", "26 weeks", "6 months of birth or adoption"],
                ["Secondary caregiver", "4 weeks", "6 months of birth or adoption"],
            ],
            [60, 40, 70],
        ),
        Spacer(1, 4),
        h2("5. Related Policies"),
        p(
            "See the Remote Work Policy (HR-003) for working from another country while on leave."
        ),
    ],
)

# 2. Expense policy ----------------------------------------------------------
m = dict(
    doc_id="FIN-002",
    filename="expense-policy.pdf",
    title="Expense Reimbursement Policy",
    department="Finance",
    owner="Finance Controller",
    version=2,
    effective_date="2026-03-01",
    classification="Internal",
    allowed_groups="all-employees",
)
register(m)
build(
    m,
    [
        h1(m["title"]),
        doc_control(m),
        Spacer(1, 6),
        h2("1. Submission Deadline"),
        p(
            "Expense claims must be submitted within 30 days of the expense date. Claims submitted "
            "later require written approval from the department head."
        ),
        h2("2. Receipts"),
        p(
            "A receipt is required for every expense above 25 USD. Missing receipts must be "
            "explained in the claim notes."
        ),
        h2("3. Travel Limits"),
        p("Limits depend on the city tier of the destination, as shown in Table 1."),
        table(
            [
                [
                    "City tier",
                    "Hotel (per night)",
                    "Meals (per day)",
                    "Ground transport (per day)",
                ],
                [
                    "Tier 1 (for example London, New York, Singapore)",
                    "220 USD",
                    "75 USD",
                    "60 USD",
                ],
                ["Tier 2 (all other major cities)", "150 USD", "60 USD", "40 USD"],
                ["Tier 3 (other locations)", "110 USD", "45 USD", "30 USD"],
            ],
            [70, 35, 35, 35],
        ),
        Spacer(1, 4),
        p(
            "Economy class is required for flights under 6 hours. Business class is allowed for "
            "flights over 6 hours with manager approval. Alcohol is not reimbursable."
        ),
        h2("4. Approval Limits"),
        table(
            [
                ["Claim amount (USD)", "Approver"],
                ["Up to 500", "Line manager"],
                ["501 to 2,500", "Department head"],
                ["2,501 to 10,000", "Finance director"],
                ["Above 10,000", "Chief Financial Officer"],
            ],
            [70, 100],
        ),
        Spacer(1, 4),
        p("Reimbursement is paid within 10 working days of final approval."),
    ],
)

# 3. Remote work policy ---------------------------------------------------------
m = dict(
    doc_id="HR-003",
    filename="remote-work-policy.pdf",
    title="Remote Work Policy",
    department="HR",
    owner="HR Operations",
    version=4,
    effective_date="2026-02-15",
    classification="Internal",
    allowed_groups="all-employees",
)
register(m)
build(
    m,
    [
        h1(m["title"]),
        doc_control(m),
        Spacer(1, 6),
        h2("1. Eligibility"),
        p(
            "Employees who have completed their 90-day probation may work remotely up to 3 days per "
            "week, subject to manager approval."
        ),
        h2("2. Core Hours"),
        p(
            "Remote employees must be available between 10:00 and 16:00 in their local time zone."
        ),
        h2("3. Working From Another Country"),
        p(
            "Working from outside the country of employment is limited to 20 days per calendar year "
            "and requires prior approval from HR because of tax and legal implications. "
            "Table 1 shows the approval path."
        ),
        table(
            [
                ["Days abroad per year", "Approval required", "Request lead time"],
                ["1 to 5", "Line manager", "5 working days"],
                ["6 to 20", "Line manager and HR", "20 working days"],
                ["More than 20", "Not permitted", "Not applicable"],
            ],
            [50, 60, 60],
        ),
        Spacer(1, 4),
        h2("4. Equipment and Allowance"),
        table(
            [
                ["Item", "Provided by company", "Notes"],
                ["Laptop", "Yes", "Replaced every 3 years"],
                ["External monitor", "Yes", "One per employee"],
                [
                    "Home office allowance",
                    "300 USD one-time",
                    "Available after probation",
                ],
                ["Internet reimbursement", "No", "Not covered"],
            ],
            [50, 50, 70],
        ),
    ],
)

# 4. Security policy ----------------------------------------------------------
m = dict(
    doc_id="IT-004",
    filename="security-policy.pdf",
    title="Information Security Policy",
    department="IT",
    owner="Chief Information Security Officer",
    version=5,
    effective_date="2026-04-01",
    classification="Internal",
    allowed_groups="all-employees",
)
register(m)
build(
    m,
    [
        h1(m["title"]),
        doc_control(m),
        Spacer(1, 6),
        h2("1. Passwords and Authentication"),
        p(
            "Passwords must be at least 14 characters and changed every 180 days. Multi-factor "
            "authentication is mandatory for all company systems."
        ),
        h2("2. Incident Reporting"),
        p(
            "Suspected security incidents, including phishing emails, must be reported to the "
            "security team within 1 hour of discovery. A lost or stolen company device must be "
            "reported immediately so it can be remotely wiped."
        ),
        h2("3. Data Classification"),
        p("All company data must be classified. Handling rules are shown in Table 1."),
        table(
            [
                [
                    "Class",
                    "Examples",
                    "Personal devices",
                    "Personal email",
                    "Encryption required",
                ],
                ["Public", "Press releases, job ads", "Allowed", "Allowed", "No"],
                [
                    "Internal",
                    "Policies, org charts",
                    "Read-only via company app",
                    "Not allowed",
                    "In transit",
                ],
                [
                    "Confidential",
                    "Contracts, customer lists",
                    "Not allowed",
                    "Not allowed",
                    "At rest and in transit",
                ],
                [
                    "Restricted",
                    "Salary data, source code, health data",
                    "Not allowed",
                    "Not allowed",
                    "At rest and in transit",
                ],
            ],
            [24, 48, 36, 28, 34],
        ),
        Spacer(1, 4),
        p(
            "Confidential and Restricted data must never be stored on personal devices or sent to "
            "personal email accounts."
        ),
    ],
)

# 5. Salary bands (restricted) ----------------------------------------------------
m = dict(
    doc_id="HR-005",
    filename="salary-bands-confidential.pdf",
    title="Salary Bands (Confidential)",
    department="HR",
    owner="Head of Compensation",
    version=1,
    effective_date="2026-01-01",
    classification="Restricted",
    allowed_groups="hr-team",
)
register(m)
build(
    m,
    [
        h1(m["title"]),
        doc_control(m),
        Spacer(1, 6),
        h2("1. Overview"),
        p(
            "This document is restricted to the HR team. Salary bands are reviewed annually and "
            "must not be shared with other employees."
        ),
        h2("2. Bands"),
        table(
            [
                ["Band", "Typical role level", "Minimum (USD)", "Maximum (USD)"],
                ["L3", "Associate", "40,000", "55,000"],
                ["L4", "Senior", "55,000", "75,000"],
                ["L5", "Lead", "75,000", "100,000"],
            ],
            [30, 60, 40, 40],
        ),
        Spacer(1, 4),
        h2("3. Exceptions"),
        p("Offers above the top of a band require approval from the HR director."),
    ],
)

# registry -------------------------------------------------------------------
(OUT / "registry.json").write_text(json.dumps(REGISTRY, indent=2), encoding="utf-8")
print(f"\nTotal PDFs: {len(REGISTRY)}  |  Registry: {OUT / 'registry.json'}")
