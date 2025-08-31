#!/usr/bin/env python3
"""
Script to create mock PDF files with sensitive personal data for RAG testing
"""

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import os

# Mock sensitive data for 5 people
people_data = [
    {
        "file": "person1.pdf",
        "name": "Sarah Michelle Johnson",
        "ssn": "123-45-6789",
        "dob": "March 15, 1985",
        "age": 39,
        "address": "1247 Oak Street, Apartment 3B, San Francisco, CA 94102",
        "phone": "(415) 555-0123",
        "email": "sarah.johnson@email.com",
        "salary": 125000,
        "position": "Senior Software Engineer",
        "department": "Engineering",
        "manager": "David Chen",
        "start_date": "June 10, 2018",
        "emergency_contact": "Michael Johnson (husband) - (415) 555-0124",
        "bank_account": "Wells Fargo ****-****-****-4567",
        "health_plan": "Kaiser Permanente - Policy #KP789456123",
        "notes": "Authorized for remote work. Security clearance Level 2."
    },
    {
        "file": "person2.pdf",
        "name": "Marcus Antonio Rodriguez",
        "ssn": "987-65-4321",
        "dob": "August 22, 1990",
        "age": 34,
        "address": "892 Pine Avenue, Unit 12, Austin, TX 78701",
        "phone": "(512) 555-0198",
        "email": "m.rodriguez@email.com",
        "salary": 98500,
        "position": "Product Manager",
        "department": "Product Development",
        "manager": "Lisa Chen",
        "start_date": "February 3, 2020",
        "emergency_contact": "Carmen Rodriguez (mother) - (512) 555-0199",
        "bank_account": "Chase Bank ****-****-****-8901",
        "health_plan": "Blue Cross Blue Shield - Policy #BC456789012",
        "notes": "Bilingual (Spanish/English). Handles international clients."
    },
    {
        "file": "person3.pdf",
        "name": "Dr. Emily Rose Thompson",
        "ssn": "456-78-9012",
        "dob": "December 5, 1982",
        "age": 41,
        "address": "3456 Maple Drive, Boston, MA 02118",
        "phone": "(617) 555-0167",
        "email": "emily.thompson.md@email.com",
        "salary": 180000,
        "position": "Chief Medical Officer",
        "department": "Healthcare Division",
        "manager": "Board of Directors",
        "start_date": "September 15, 2019",
        "emergency_contact": "James Thompson (spouse) - (617) 555-0168",
        "bank_account": "Bank of America ****-****-****-2345",
        "health_plan": "Harvard Pilgrim - Policy #HP345678901",
        "notes": "MD from Harvard Medical School. Licensed in MA, NY, CA."
    },
    {
        "file": "person4.pdf",
        "name": "Kevin Michael O'Brien",
        "ssn": "789-01-2345",
        "dob": "May 18, 1987",
        "age": 37,
        "address": "567 Cedar Lane, Chicago, IL 60614",
        "phone": "(312) 555-0134",
        "email": "kevin.obrien@email.com",
        "salary": 75000,
        "position": "Marketing Specialist",
        "department": "Marketing & Communications",
        "manager": "Jennifer Walsh",
        "start_date": "November 12, 2021",
        "emergency_contact": "Patrick O'Brien (brother) - (312) 555-0135",
        "bank_account": "US Bank ****-****-****-6789",
        "health_plan": "Aetna - Policy #AE234567890",
        "notes": "Certified in Google Ads and Facebook Marketing."
    },
    {
        "file": "person5.pdf",
        "name": "Alexandra Sofia Petrov",
        "ssn": "345-67-8901",
        "dob": "October 30, 1993",
        "age": 30,
        "address": "2108 Birch Street, Seattle, WA 98101",
        "phone": "(206) 555-0145",
        "email": "alexandra.petrov@email.com",
        "salary": 110000,
        "position": "Data Scientist",
        "department": "Analytics & AI",
        "manager": "Dr. Robert Kim",
        "start_date": "January 8, 2022",
        "emergency_contact": "Dimitri Petrov (father) - (206) 555-0146",
        "bank_account": "Credit Union ****-****-****-0123",
        "health_plan": "Premera Blue Cross - Policy #PB123456789",
        "notes": "PhD in Machine Learning from MIT. Fluent in Russian and Bulgarian."
    }
]

def create_person_pdf(person_data):
    """Create a PDF file for a person with their sensitive data"""
    filename = person_data["file"]
    doc = SimpleDocTemplate(filename, pagesize=letter)
    
    # Get styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        textColor='darkred'
    )
    header_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=15,
        textColor='darkblue'
    )
    
    # Content
    content = []
    
    # Title
    content.append(Paragraph(f"CONFIDENTIAL PERSONNEL FILE", title_style))
    content.append(Paragraph(f"{person_data['name']}", styles['Heading1']))
    content.append(Spacer(1, 0.3*inch))
    
    # Personal Information
    content.append(Paragraph("PERSONAL INFORMATION - RESTRICTED ACCESS", header_style))
    personal_info = f"""
    <b>Full Name:</b> {person_data['name']}<br/>
    <b>Date of Birth:</b> {person_data['dob']}<br/>
    <b>Age:</b> {person_data['age']} years old<br/>
    <b>Social Security Number:</b> {person_data['ssn']}<br/>
    <b>Home Address:</b> {person_data['address']}<br/>
    <b>Phone Number:</b> {person_data['phone']}<br/>
    <b>Email Address:</b> {person_data['email']}<br/>
    """
    content.append(Paragraph(personal_info, styles['Normal']))
    content.append(Spacer(1, 0.2*inch))
    
    # Employment Information
    content.append(Paragraph("EMPLOYMENT DETAILS - CONFIDENTIAL", header_style))
    employment_info = f"""
    <b>Position:</b> {person_data['position']}<br/>
    <b>Department:</b> {person_data['department']}<br/>
    <b>Annual Salary:</b> ${person_data['salary']:,}<br/>
    <b>Direct Manager:</b> {person_data['manager']}<br/>
    <b>Start Date:</b> {person_data['start_date']}<br/>
    <b>Employee Status:</b> Active - Full Time<br/>
    """
    content.append(Paragraph(employment_info, styles['Normal']))
    content.append(Spacer(1, 0.2*inch))
    
    # Financial Information
    content.append(Paragraph("FINANCIAL & BENEFITS - SENSITIVE", header_style))
    financial_info = f"""
    <b>Primary Bank Account:</b> {person_data['bank_account']}<br/>
    <b>Health Insurance:</b> {person_data['health_plan']}<br/>
    <b>401(k) Contribution:</b> 6% with company match<br/>
    <b>Life Insurance:</b> 2x annual salary coverage<br/>
    <b>Stock Options:</b> Vested shares available<br/>
    """
    content.append(Paragraph(financial_info, styles['Normal']))
    content.append(Spacer(1, 0.2*inch))
    
    # Emergency Contact
    content.append(Paragraph("EMERGENCY CONTACT", header_style))
    emergency_info = f"""
    <b>Emergency Contact:</b> {person_data['emergency_contact']}<br/>
    """
    content.append(Paragraph(emergency_info, styles['Normal']))
    content.append(Spacer(1, 0.2*inch))
    
    # Additional Notes
    content.append(Paragraph("ADDITIONAL NOTES", header_style))
    notes_info = f"""
    {person_data['notes']}<br/>
    <br/>
    <b>Background Check:</b> Completed and approved<br/>
    <b>Drug Test:</b> Passed - Date: {person_data['start_date']}<br/>
    <b>Security Badge ID:</b> EMP{person_data['ssn'].replace('-', '')[-4:]}<br/>
    """
    content.append(Paragraph(notes_info, styles['Normal']))
    content.append(Spacer(1, 0.3*inch))
    
    # Footer
    content.append(Paragraph(
        "<b>CONFIDENTIALITY NOTICE:</b> This document contains sensitive personal and financial information. "
        "Access is restricted to authorized HR personnel only. Unauthorized disclosure is prohibited by law.",
        styles['Italic']
    ))
    
    # Build PDF
    doc.build(content)
    print(f"Created {filename}")
    return filename

def main():
    """Create all person PDF files"""
    print("Creating mock personnel files with sensitive data...")
    
    try:
        for person in people_data:
            create_person_pdf(person)
        
        print(f"\nSuccessfully created {len(people_data)} PDF files:")
        for person in people_data:
            print(f"  - {person['file']} ({person['name']})")
        
        print("\nThese files contain mock sensitive data for testing the RAG system.")
        print("You can now upload them to test document ingestion and querying.")
        
    except ImportError:
        print("Error: reportlab library not found.")
        print("Install with: pip install reportlab")
    except Exception as e:
        print(f"Error creating PDFs: {e}")

if __name__ == "__main__":
    main()