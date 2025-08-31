#!/usr/bin/env python3
"""
Generate 10 client files for law firm with various legal cases
"""

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import os

def create_client_files():
    """Create 10 client PDF files with different legal cases"""
    
    clients = [
        {
            "name": "Rebecca Martinez",
            "case_type": "Wrongful Termination",
            "client_id": "LAW-001",
            "phone": "(415) 555-0191",
            "email": "r.martinez@email.com",
            "address": "2847 Pine Street, San Francisco, CA 94115",
            "employer": "TechFlow Solutions Inc.",
            "case_details": """
            Client was terminated on March 15, 2024, after filing a workers' compensation claim for repetitive 
            stress injury. Employee handbook states progressive discipline policy, but client received no 
            warnings. Supervisor made statements about "troublemakers" and workers' comp being expensive. 
            Client worked as Senior QA Engineer for 3 years with excellent performance reviews.
            
            LEGAL ISSUES: Wrongful termination in violation of public policy (Labor Code 132a), 
            breach of implied contract (employee handbook), intentional infliction of emotional distress.
            
            DAMAGES: Lost wages $8,500/month, benefits worth $1,200/month, seeking reinstatement 
            or front pay. Client experienced anxiety and depression requiring therapy.
            """,
            "case_status": "Active - Discovery Phase",
            "settlement_demand": "$250,000"
        },
        {
            "name": "David Kim",
            "case_type": "Wage and Hour Violation", 
            "client_id": "LAW-002",
            "phone": "(408) 555-0278",
            "email": "david.kim.dev@email.com",
            "address": "1456 Oak Avenue, San Jose, CA 95128",
            "employer": "Digital Marketing Partners LLC",
            "case_details": """
            Software developer classified as exempt but performed non-exempt duties. Required to work 
            60-70 hours per week without overtime pay. No meal or rest breaks provided during crunch periods. 
            Employer failed to provide accurate wage statements showing overtime calculations.
            
            LEGAL ISSUES: Misclassification of exempt employee, unpaid overtime violations (Labor Code 510), 
            meal and rest break violations (Labor Code 226.7), inaccurate wage statements (Labor Code 226).
            
            DAMAGES: 18 months unpaid overtime estimated at $45,000, meal/rest break premiums $8,400, 
            waiting time penalties, attorney's fees. PAGA penalties potentially available.
            """,
            "case_status": "Active - Settlement Negotiations",
            "settlement_demand": "$85,000"
        },
        {
            "name": "Angela Foster", 
            "case_type": "Employment Discrimination",
            "client_id": "LAW-003", 
            "phone": "(650) 555-0342",
            "email": "angela.foster@email.com",
            "address": "892 Elm Drive, Palo Alto, CA 94301",
            "employer": "Precision Manufacturing Corp",
            "case_details": """
            Pregnant client denied promotion to management position despite being most qualified candidate. 
            Supervisor made comments about pregnancy affecting work performance and travel requirements. 
            After returning from maternity leave, client was transferred to less desirable position 
            with reduced responsibilities and pay cut.
            
            LEGAL ISSUES: Pregnancy discrimination (FEHA), retaliation for taking protected leave, 
            failure to provide reasonable accommodation, constructive termination.
            
            DAMAGES: Lost promotion opportunity worth $15,000 salary increase, reduction in pay $2,000/month, 
            emotional distress, loss of advancement opportunities. Seeking reinstatement to original position.
            """,
            "case_status": "Active - Mediation Scheduled",
            "settlement_demand": "$175,000"
        },
        {
            "name": "Michael Rodriguez",
            "case_type": "Contract Dispute",
            "client_id": "LAW-004",
            "phone": "(916) 555-0455", 
            "email": "m.rodriguez.consult@email.com",
            "address": "3721 River Road, Sacramento, CA 95814",
            "employer": "Global Consulting Services",
            "case_details": """
            Independent contractor agreement for IT consulting services. Client completed $150,000 project 
            but employer refuses payment claiming work was unsatisfactory. Contract specifications were 
            met according to technical documentation. Employer attempting to use work despite non-payment.
            
            LEGAL ISSUES: Breach of contract, quantum meruit recovery, account stated, 
            possible conversion of work product.
            
            DAMAGES: Unpaid contract amount $150,000, additional work performed $25,000, 
            interest and costs. Seeking immediate payment and return of work product if payment refused.
            """,
            "case_status": "Active - Pre-Trial Motions",
            "settlement_demand": "$185,000"
        },
        {
            "name": "Sarah Chen",
            "case_type": "Trade Secret Misappropriation", 
            "client_id": "LAW-005",
            "phone": "(619) 555-0567",
            "email": "sarah.chen.cto@email.com", 
            "address": "1647 Sunset Boulevard, San Diego, CA 92103",
            "employer": "Former employer: InnovateTech Systems",
            "case_details": """
            Former employee of client's company downloaded proprietary algorithms and customer database 
            before departure. Started competing business using identical technology and contacted client's 
            customers. Signed non-disclosure and non-compete agreements during employment.
            
            LEGAL ISSUES: Trade secret misappropriation (Civil Code 3426), breach of confidentiality agreement, 
            breach of non-compete agreement, unfair competition, conversion of confidential information.
            
            DAMAGES: Loss of customers valued at $300,000 annually, development costs for proprietary technology 
            $500,000, ongoing competitive harm. Seeking injunctive relief and monetary damages.
            """,
            "case_status": "Active - Temporary Restraining Order Granted",
            "settlement_demand": "$1,200,000"
        },
        {
            "name": "Robert Thompson",
            "case_type": "Personal Injury - Slip and Fall",
            "client_id": "LAW-006", 
            "phone": "(510) 555-0689",
            "email": "rob.thompson@email.com",
            "address": "4582 Broadway Street, Oakland, CA 94612", 
            "employer": "N/A - Incident at Westfield Shopping Center",
            "case_details": """
            Client slipped on wet floor near food court without warning signs. Sustained fractured wrist, 
            back injury requiring physical therapy. Security footage shows maintenance staff had mopped 
            area 10 minutes before incident without placing warning cones or signs.
            
            LEGAL ISSUES: Premises liability, negligent maintenance, failure to warn of dangerous condition.
            
            DAMAGES: Medical expenses $15,000, lost wages 6 weeks at $3,200/month, ongoing physical therapy, 
            pain and suffering. Client is right-handed and injury affects work as graphic designer.
            """,
            "case_status": "Active - Medical Treatment Ongoing",
            "settlement_demand": "$125,000"
        },
        {
            "name": "Jennifer Walsh",
            "case_type": "Copyright Infringement",
            "client_id": "LAW-007",
            "phone": "(559) 555-0734", 
            "email": "jennifer.walsh.photo@email.com",
            "address": "2917 Maple Avenue, Fresno, CA 93721",
            "employer": "Self-employed photographer",
            "case_details": """
            Professional photographer's images used by marketing company without permission or payment. 
            Images appeared in national advertising campaign and social media promotions. Copyright 
            registration filed prior to infringement. Defendant removed copyright notice and used 
            images as if they were stock photos.
            
            LEGAL ISSUES: Copyright infringement (17 USC 501), removal of copyright notice (17 USC 506), 
            false advertising, unfair competition.
            
            DAMAGES: Licensing fees would have been $25,000, defendant's profits from campaign $200,000, 
            statutory damages available. Seeking injunctive relief and maximum statutory damages.
            """,
            "case_status": "Active - Defendant Failed to Respond",
            "settlement_demand": "$150,000"
        },
        {
            "name": "James Wilson",
            "case_type": "Business Partnership Dissolution", 
            "client_id": "LAW-008",
            "phone": "(707) 555-0823",
            "email": "james.wilson.ventures@email.com", 
            "address": "1823 Vine Street, Napa, CA 94559",
            "employer": "Wilson & Associates Construction",
            "case_details": """
            50/50 partnership in construction business. Partner misappropriated funds, failed to pay 
            subcontractors, and damaged business reputation. Partnership agreement provides for buyout 
            at fair market value. Client seeks dissolution and damages for partner's misconduct.
            
            LEGAL ISSUES: Breach of fiduciary duty, breach of partnership agreement, conversion, 
            accounting of partnership assets, dissolution and winding up.
            
            DAMAGES: Business valuation $400,000, client entitled to 50% share, claims for partner's 
            misappropriation $75,000. Seeking court-ordered dissolution and accounting.
            """,
            "case_status": "Active - Forensic Accounting in Progress", 
            "settlement_demand": "$275,000"
        },
        {
            "name": "Lisa Garcia",
            "case_type": "Medical Malpractice",
            "client_id": "LAW-009",
            "phone": "(805) 555-0912", 
            "email": "lisa.garcia.rn@email.com",
            "address": "3456 Ocean View Drive, Santa Barbara, CA 93101",
            "employer": "N/A - Patient at Regional Medical Center",
            "case_details": """
            Misdiagnosis of chest pain as anxiety attack. Patient discharged from emergency room without 
            proper cardiac evaluation. Suffered heart attack 6 hours later causing permanent heart damage. 
            Standard of care required EKG and cardiac enzymes given patient's age and symptoms.
            
            LEGAL ISSUES: Medical negligence, failure to diagnose, deviation from standard of care, 
            informed consent issues.
            
            DAMAGES: Additional medical expenses $125,000, lost earning capacity as registered nurse, 
            pain and suffering, reduced life expectancy. Life care plan estimates ongoing costs at $300,000.
            """,
            "case_status": "Active - Expert Witness Discovery",
            "settlement_demand": "$850,000"
        },
        {
            "name": "Daniel Park",
            "case_type": "Real Estate Fraud", 
            "client_id": "LAW-010",
            "phone": "(925) 555-0045",
            "email": "daniel.park.realtor@email.com",
            "address": "7891 Hill Street, Walnut Creek, CA 94597", 
            "employer": "Park Properties Investment Group",
            "case_details": """
            Real estate developer sold commercial properties with undisclosed environmental contamination. 
            Client purchased $2.3M office building for investment. Discovered soil contamination requiring 
            $800,000 cleanup. Developer knew of contamination from previous environmental report.
            
            LEGAL ISSUES: Real estate fraud, concealment of material facts, breach of warranty, 
            negligent misrepresentation, violation of environmental disclosure laws.
            
            DAMAGES: Cleanup costs $800,000, diminished property value $500,000, lost rental income 
            during remediation $150,000. Seeking rescission or full damages plus attorney's fees.
            """,
            "case_status": "Active - Environmental Assessment Complete",
            "settlement_demand": "$1,650,000"
        }
    ]
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=20
    )
    
    for client in clients:
        filename = f"/Users/kostispodaras/code/RAG/client_{client['client_id'].split('-')[1]}_{client['name'].replace(' ', '_').lower()}.pdf"
        
        doc = SimpleDocTemplate(filename, pagesize=letter,
                              rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=18)
        
        story = []
        
        # Header
        story.append(Paragraph("CONFIDENTIAL ATTORNEY-CLIENT PRIVILEGED", styles['Heading3']))
        story.append(Paragraph(f"CLIENT FILE: {client['name'].upper()}", title_style))
        story.append(Spacer(1, 20))
        
        # Client Information Table
        client_data = [
            ['Client ID:', client['client_id']],
            ['Full Name:', client['name']], 
            ['Phone:', client['phone']],
            ['Email:', client['email']],
            ['Address:', client['address']],
            ['Case Type:', client['case_type']],
            ['Case Status:', client['case_status']],
            ['Settlement Demand:', client['settlement_demand']]
        ]
        
        if client['employer'] and not client['employer'].startswith('N/A'):
            client_data.insert(-3, ['Employer/Defendant:', client['employer']])
        
        client_table = Table(client_data, colWidths=[2*inch, 4*inch])
        client_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        
        story.append(client_table)
        story.append(Spacer(1, 20))
        
        # Case Details
        story.append(Paragraph("CASE DETAILS AND ANALYSIS", styles['Heading2']))
        story.append(Paragraph(client['case_details'], styles['Normal']))
        story.append(Spacer(1, 15))
        
        # Case Timeline (sample dates)
        story.append(Paragraph("CASE TIMELINE", styles['Heading2']))
        timeline_items = [
            "• Initial incident/violation occurred", 
            "• Client consultation scheduled",
            "• Retainer agreement signed", 
            "• Demand letter sent to opposing party",
            "• Complaint filed (if applicable)",
            "• Discovery phase initiated",
            "• Mediation/settlement discussions"
        ]
        
        for item in timeline_items:
            story.append(Paragraph(item, styles['Normal']))
        
        story.append(Spacer(1, 15))
        
        # Legal Strategy
        strategy_text = f"""
        LEGAL STRATEGY: Pursue all available remedies under applicable state and federal law. 
        Document all damages and maintain detailed records. Consider alternative dispute resolution 
        to minimize costs and time. Evaluate strength of case based on evidence and witness testimony.
        
        NEXT STEPS: Complete discovery, conduct depositions, prepare expert witness reports, 
        evaluate settlement opportunities, prepare for trial if necessary.
        
        ESTIMATED CASE VALUE: {client['settlement_demand']} based on current damages assessment.
        """
        
        story.append(Paragraph("LEGAL STRATEGY", styles['Heading2']))
        story.append(Paragraph(strategy_text, styles['Normal']))
        
        # Build PDF
        doc.build(story)
        print(f"Created client file: {filename}")

if __name__ == "__main__":
    create_client_files()