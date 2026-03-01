# Customer Support Ticketing System

## Project Overview
This is a full-stack web application for managing IT or customer service tickets.  
Users can submit tickets, track their status, and provide issue details.  
Admins can view all tickets, update statuses, and export ticket data for reporting.  

The system also supports **SLA tracking** by setting default resolution times for tickets.  
It uses **Flask** for the backend and **SQLite** for storage, making it lightweight and easy to deploy.

---

## Features
- **Ticket Submission:** Users can submit new support tickets with:
  - Name and email
  - Issue type
  - Priority (Low, Medium, High)
  - Description of the problem
- **Ticket Status Tracking:** Tickets can be Open, In Progress, or Closed.  
- **Admin Panel:** View all tickets, update status, and manage support workflow.  
- **SLA Tracking:** Tickets have default due dates for resolution (e.g., 2 days).  
- **Reporting & Export:** Export all tickets to JSON format for analysis.  
- **SQLite Backend:** No external database setup required.  

---

## Dependencies
- Python 3.x  
- Flask

Install Flask using pip:

pip install flask

---

## To Run
python app.py

http://127.0.0.1:5000/      -> Ticket submission page
http://127.0.0.1:5000/admin -> Admin panel
