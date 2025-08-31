#!/usr/bin/env python3
"""
Script to generate comprehensive legal reference document and client files
for testing the RAG system with legal document search.
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import os

def create_legal_reference_pdf():
    """Create a comprehensive legal reference document"""
    
    # Create the PDF
    doc = SimpleDocTemplate("/Users/kostispodaras/code/RAG/legal_reference.pdf", 
                          pagesize=letter,
                          rightMargin=72, leftMargin=72,
                          topMargin=72, bottomMargin=18)
    
    # Get styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=1  # Center alignment
    )
    
    heading_style = styles['Heading2']
    normal_style = styles['Normal']
    
    # Build the content
    story = []
    
    # Title
    story.append(Paragraph("COMPREHENSIVE LEGAL REFERENCE GUIDE", title_style))
    story.append(Paragraph("Corporate, Employment, and Contract Law", styles['Heading3']))
    story.append(Spacer(1, 20))
    
    # Table of Contents
    story.append(Paragraph("TABLE OF CONTENTS", heading_style))
    toc_content = [
        "1. Employment Law",
        "2. Contract Law", 
        "3. Corporate Law",
        "4. Intellectual Property Law",
        "5. Privacy and Data Protection",
        "6. Litigation Procedures",
        "7. Settlement Guidelines"
    ]
    
    for item in toc_content:
        story.append(Paragraph(item, normal_style))
    
    story.append(PageBreak())
    
    # 1. Employment Law
    story.append(Paragraph("1. EMPLOYMENT LAW", heading_style))
    
    story.append(Paragraph("1.1 Wrongful Termination", styles['Heading3']))
    story.append(Paragraph("""
    Under California Labor Code Section 2922, employment relationships are generally "at-will," 
    meaning either party can terminate the relationship at any time. However, wrongful termination 
    occurs when an employee is fired for reasons that violate public policy, including:
    
    • Filing workers' compensation claims
    • Reporting workplace safety violations (whistleblowing)
    • Refusing to commit illegal acts
    • Taking legally protected leave (FMLA, pregnancy leave)
    • Reporting discrimination or harassment
    
    Remedies for wrongful termination include reinstatement, back pay, front pay, and in some cases, 
    punitive damages. The statute of limitations is typically 2-3 years depending on the specific claim.
    """, normal_style))
    
    story.append(Paragraph("1.2 Wage and Hour Violations", styles['Heading3']))
    story.append(Paragraph("""
    California Labor Code requires employers to pay minimum wage ($16.00/hour as of 2024), 
    provide meal and rest breaks, and pay overtime compensation:
    
    • Overtime: 1.5x regular rate for hours over 8 per day or 40 per week
    • Double time: 2x regular rate for hours over 12 per day or after 8 hours on 7th consecutive day
    • Meal breaks: 30 minutes for shifts over 5 hours, 1 hour penalty pay if denied
    • Rest breaks: 10 minutes per 4 hours worked, 1 hour penalty pay if denied
    
    Employers must provide accurate wage statements and pay all wages owed within 72 hours of termination.
    """, normal_style))
    
    story.append(Paragraph("1.3 Workplace Discrimination", styles['Heading3']))
    story.append(Paragraph("""
    The Fair Employment and Housing Act (FEHA) prohibits discrimination based on:
    
    • Race, color, national origin
    • Religion, creed  
    • Sex, gender, gender identity, gender expression
    • Sexual orientation
    • Marital status, pregnancy
    • Age (40 and over)
    • Physical or mental disability
    • Medical condition
    • Military or veteran status
    
    Employees must file complaints with DFEH within 3 years. Remedies include damages, 
    reinstatement, promotion, and attorney's fees.
    """, normal_style))
    
    story.append(PageBreak())
    
    # 2. Contract Law  
    story.append(Paragraph("2. CONTRACT LAW", heading_style))
    
    story.append(Paragraph("2.1 Contract Formation", styles['Heading3']))
    story.append(Paragraph("""
    Valid contracts require four essential elements:
    
    1. OFFER: Clear, definite proposal communicated to offeree
    2. ACCEPTANCE: Unqualified agreement to terms (mirror image rule)
    3. CONSIDERATION: Exchange of value (money, services, forbearance)  
    4. CAPACITY: Legal ability to enter contracts (age, mental competency)
    
    Contracts may be written, oral, or implied by conduct. Statute of Frauds requires written 
    contracts for sales of goods over $500, real estate transfers, and agreements that cannot 
    be performed within one year.
    """, normal_style))
    
    story.append(Paragraph("2.2 Breach of Contract", styles['Heading3']))
    story.append(Paragraph("""
    Material breach occurs when a party's failure to perform substantially defeats the purpose 
    of the contract. Remedies include:
    
    • EXPECTATION DAMAGES: Put non-breaching party in position they would have been in
    • RELIANCE DAMAGES: Reimburse costs incurred in reliance on contract
    • RESTITUTION: Restore value conferred to prevent unjust enrichment
    • SPECIFIC PERFORMANCE: Court order to perform (available for unique goods/real estate)
    • LIQUIDATED DAMAGES: Pre-agreed reasonable estimate of damages
    
    Mitigation doctrine requires non-breaching party to minimize damages where reasonable.
    """, normal_style))
    
    story.append(Paragraph("2.3 Contract Defenses", styles['Heading3']))
    story.append(Paragraph("""
    Common contract defenses include:
    
    • MISTAKE: Mutual mistake of material fact makes contract voidable
    • DURESS: Improper threat that overcomes free will
    • UNDUE INFLUENCE: Abuse of position of trust/authority
    • UNCONSCIONABILITY: Contract terms are unfairly one-sided
    • ILLEGALITY: Contract purpose or performance violates law
    • IMPOSSIBILITY/FRUSTRATION: Performance becomes impossible or purpose is frustrated
    
    Statute of limitations for contract claims is generally 4 years for written contracts, 
    2 years for oral contracts in California.
    """, normal_style))
    
    story.append(PageBreak())
    
    # 3. Corporate Law
    story.append(Paragraph("3. CORPORATE LAW", heading_style))
    
    story.append(Paragraph("3.1 Business Entity Formation", styles['Heading3']))
    story.append(Paragraph("""
    California offers several business entity types:
    
    • CORPORATION (C-Corp): Limited liability, double taxation, suitable for investors
    • S-CORPORATION: Pass-through taxation, restrictions on shareholders
    • LIMITED LIABILITY COMPANY (LLC): Flexible management, pass-through taxation
    • LIMITED PARTNERSHIP: General partners have unlimited liability, limited partners protected
    • SOLE PROPRIETORSHIP: No liability protection, simplest structure
    
    Formation requires filing appropriate documents with California Secretary of State and 
    paying required fees. Corporations must adopt bylaws and issue stock certificates.
    """, normal_style))
    
    story.append(Paragraph("3.2 Fiduciary Duties", styles['Heading3']))
    story.append(Paragraph("""
    Directors and officers owe fiduciary duties to corporation and shareholders:
    
    • DUTY OF CARE: Make informed decisions, exercise reasonable business judgment
    • DUTY OF LOYALTY: Act in good faith, avoid conflicts of interest
    • BUSINESS JUDGMENT RULE: Protects directors who make informed, good faith decisions
    
    Breach of fiduciary duty can result in personal liability for damages, disgorgement 
    of profits, and removal from office.
    """, normal_style))
    
    story.append(Paragraph("3.3 Securities Law Compliance", styles['Heading3']))
    story.append(Paragraph("""
    California Corporate Securities Law and federal securities laws regulate:
    
    • REGISTRATION: Securities offerings must be registered or qualify for exemption
    • DISCLOSURE: Material information must be disclosed to investors
    • ANTI-FRAUD: Prohibition on misrepresentations and omissions
    • INSIDER TRADING: Trading on material non-public information prohibited
    
    Violations can result in civil and criminal penalties, rescission rights, and SEC enforcement actions.
    """, normal_style))
    
    story.append(PageBreak())
    
    # 4. Intellectual Property Law
    story.append(Paragraph("4. INTELLECTUAL PROPERTY LAW", heading_style))
    
    story.append(Paragraph("4.1 Copyright Protection", styles['Heading3']))
    story.append(Paragraph("""
    Copyright protects original works of authorship including:
    
    • Literary works (books, articles, software code)
    • Musical compositions and sound recordings  
    • Dramatic works and choreography
    • Visual arts (paintings, photographs, sculptures)
    • Motion pictures and audiovisual works
    
    Protection arises automatically upon creation and fixation. Registration with Copyright Office 
    provides enhanced remedies. Duration is generally life of author plus 70 years.
    """, normal_style))
    
    story.append(Paragraph("4.2 Trademark Rights", styles['Heading3']))
    story.append(Paragraph("""
    Trademarks protect distinctive marks used in commerce:
    
    • WORD MARKS: Company names, product names, slogans
    • DESIGN MARKS: Logos, symbols, distinctive packaging
    • SERVICE MARKS: Marks used to identify services
    
    Rights arise through use in commerce. Federal registration provides nationwide protection. 
    Trademarks can last indefinitely with proper use and renewal.
    """, normal_style))
    
    story.append(Paragraph("4.3 Trade Secret Protection", styles['Heading3']))
    story.append(Paragraph("""
    Trade secrets include confidential business information that:
    
    • Derives economic value from secrecy
    • Is subject to reasonable efforts to maintain secrecy
    • Examples: formulas, processes, customer lists, business strategies
    
    California Uniform Trade Secrets Act provides remedies including injunctive relief, 
    monetary damages, and attorney's fees for willful misappropriation.
    """, normal_style))
    
    story.append(PageBreak())
    
    # 5. Privacy and Data Protection
    story.append(Paragraph("5. PRIVACY AND DATA PROTECTION", heading_style))
    
    story.append(Paragraph("5.1 California Consumer Privacy Act (CCPA)", styles['Heading3']))
    story.append(Paragraph("""
    CCPA grants California consumers rights regarding personal information:
    
    • RIGHT TO KNOW: What personal information is collected and how it's used
    • RIGHT TO DELETE: Request deletion of personal information
    • RIGHT TO OPT-OUT: Opt out of sale of personal information  
    • RIGHT TO NON-DISCRIMINATION: Equal service regardless of privacy rights exercise
    
    Applies to businesses with $25M+ revenue, 50,000+ consumers, or 50%+ revenue from 
    selling personal information. Penalties up to $2,500 per violation ($7,500 if intentional).
    """, normal_style))
    
    story.append(Paragraph("5.2 GDPR Compliance", styles['Heading3']))
    story.append(Paragraph("""
    General Data Protection Regulation applies to EU residents' data:
    
    • LAWFUL BASIS: Must have valid legal basis for processing
    • DATA MINIMIZATION: Collect only necessary information
    • CONSENT: Must be freely given, specific, informed
    • BREACH NOTIFICATION: Must notify within 72 hours
    • DATA SUBJECT RIGHTS: Access, rectification, erasure, portability
    
    Maximum fines: 4% of annual revenue or €20 million, whichever is higher.
    """, normal_style))
    
    story.append(PageBreak())
    
    # 6. Litigation Procedures
    story.append(Paragraph("6. LITIGATION PROCEDURES", heading_style))
    
    story.append(Paragraph("6.1 Pre-Litigation Strategy", styles['Heading3']))
    story.append(Paragraph("""
    Before filing lawsuit, consider:
    
    • DEMAND LETTERS: Formal notice of claim and opportunity to resolve
    • ALTERNATIVE DISPUTE RESOLUTION: Mediation, arbitration clauses
    • STATUTE OF LIMITATIONS: Time limits vary by claim type
    • JURISDICTIONAL ISSUES: Proper court and venue selection
    • EVIDENCE PRESERVATION: Litigation hold notices, document retention
    
    Cost-benefit analysis essential given litigation expenses and time commitment.
    """, normal_style))
    
    story.append(Paragraph("6.2 Discovery Process", styles['Heading3']))
    story.append(Paragraph("""
    California Code of Civil Procedure provides discovery tools:
    
    • INTERROGATORIES: Written questions (maximum 35)
    • DOCUMENT REQUESTS: Production of relevant documents
    • DEPOSITIONS: Sworn testimony under oath
    • REQUESTS FOR ADMISSION: Admissions of fact or genuineness
    • EXPERT WITNESS DISCLOSURE: Timely disclosure required
    
    Discovery must be proportional to case value and complexity. Sanctions available for abuse.
    """, normal_style))
    
    story.append(Paragraph("6.3 Motion Practice", styles['Heading3']))
    story.append(Paragraph("""
    Common motions in civil litigation:
    
    • DEMURRER: Challenges legal sufficiency of pleadings
    • MOTION TO STRIKE: Remove improper or irrelevant matter
    • SUMMARY JUDGMENT: No triable issues of material fact
    • MOTION IN LIMINE: Exclude evidence at trial
    • MOTION FOR SANCTIONS: Seek penalties for misconduct
    
    Meet and confer requirements often required before filing motions.
    """, normal_style))
    
    story.append(PageBreak())
    
    # 7. Settlement Guidelines  
    story.append(Paragraph("7. SETTLEMENT GUIDELINES", heading_style))
    
    story.append(Paragraph("7.1 Settlement Valuation", styles['Heading3']))
    story.append(Paragraph("""
    Factors in settlement valuation:
    
    • ECONOMIC DAMAGES: Lost wages, medical expenses, out-of-pocket costs
    • NON-ECONOMIC DAMAGES: Pain and suffering, emotional distress
    • PUNITIVE DAMAGES: Available in cases of malice, fraud, or oppression
    • PROBABILITY OF SUCCESS: Likelihood of favorable verdict
    • LITIGATION COSTS: Attorney's fees, expert witness fees, court costs
    • TIME VALUE: Present value of future damages
    
    Settlement often preferable to avoid litigation risks and costs.
    """, normal_style))
    
    story.append(Paragraph("7.2 Settlement Agreement Terms", styles['Heading3']))
    story.append(Paragraph("""
    Key provisions in settlement agreements:
    
    • PAYMENT TERMS: Amount, timing, method of payment
    • RELEASE SCOPE: Claims being released, parties covered
    • CONFIDENTIALITY: Non-disclosure of terms and facts
    • NON-DISPARAGEMENT: Prohibiting negative statements
    • NON-ADMISSION: Settlement not admission of liability
    • ENFORCEMENT: Jurisdiction, attorney's fees provision
    
    Agreements should be clear, comprehensive, and legally enforceable.
    """, normal_style))
    
    # Build the PDF
    doc.build(story)
    print("Legal reference document created: legal_reference.pdf")

if __name__ == "__main__":
    create_legal_reference_pdf()