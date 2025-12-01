# Meeting Log

This document summarizes the discussions and action items from various project meetings, structured around the 5W1H framework. Each meeting is detailed in its own table.

---

### Meeting 1: Project Kickoff & Initial Planning

| Category | Details |
|---|---|
| **Who** | **Attendees:** Member A, Member B, Member C. <br> **Leader:** Member A. |
| **What** | **Topic:** Project Kickoff and Initial Planning. <br> **Discussion:** The team discussed the Software Requirements Specification (SRS) document to align on the project's scope. Core functionalities were brainstormed, including different security modes (armed, disarmed), user authentication, and the integration of various devices like cameras and sensors. |
| **When** | **Date:** November 20, 2025. <br> **Time:** 10:00 AM - 11:30 AM. |
| **Why** | **Purpose:** To formally commence the project, ensuring all members share a common understanding of the objectives and requirements. The primary goal was to establish a foundational plan and assign initial responsibilities. |
| **Where** | **Location:** Online meeting via Zoom. <br> **Link:** `https://zoom.us/j/1234567890` |
| **How** | **Actions & Outcomes:** <br> 1. Member A presented the overall project vision and high-level goals. <br> 2. The team collectively reviewed and dissected the SRS document. <br> 3. **Decisions:** The project will be developed using Python, with a GUI framework (Tkinter/PyQt to be decided), and will use SQLite for the database. <br> 4. **Action Items:** Member B to research and propose a suitable GUI framework by the next meeting. Member C to design a preliminary database schema. |

---

### Meeting 2: Technical Design & Task Delegation

| Category | Details |
|---|---|
| **Who** | **Attendees:** Member A, Member B, Member C, Member D. <br> **Leader:** Member A. |
| **What** | **Topic:** Technical Design and Task Delegation. <br> **Discussion:** The main focus was on defining the system architecture, finalizing the database schema presented by Member C, and reviewing initial UI mockups created by Member B. |
| **When** | **Date:** November 25, 2025. <br> **Time:** 02:00 PM - 04:00 PM. |
| **Why** | **Purpose:** To establish a concrete technical blueprint before the main implementation phase begins. A key objective was to distribute primary development responsibilities to each team member. |
| **Where** | **Location:** University Study Room 301. |
| **How** | **Actions & Outcomes:** <br> 1. Member C's proposed database schema was approved with minor modifications. <br> 2. Member B presented UI wireframes, which were discussed and approved. PyQt was selected as the GUI framework. <br> 3. **Task Assignments:** <br> - **Member A:** Responsible for the core system logic and application state management. <br> - **Member B:** Responsible for front-end UI/UX implementation. <br> - **Member C:** Responsible for database implementation and device integration logic. <br> - **Member D:** To begin drafting the unit and integration test plans. |

---

### Meeting 3: First Sprint Review & Integration Planning

| Category | Details |
|---|---|
| **Who** | **Attendees:** Member A, Member B, Member C, Member D. <br> **Leader:** Member B. |
| **What** | **Topic:** First Sprint Review and Integration Strategy. <br> **Discussion:** Each member presented the progress made on their assigned components. The team discussed the strategy for integrating the UI, core logic, and database. A few initial bugs and roadblocks were identified and addressed. |
| **When** | **Date:** November 28, 2025. <br> **Time:** 11:00 AM - 12:30 PM. |
| **Why** | **Purpose:** To assess the progress from the first development sprint, ensure that the individual components will be compatible with each other, and collaboratively solve any immediate technical challenges. |
| **Where** | **Location:** Online meeting via Discord. |
| **How** | **Actions & Outcomes:** <br> 1. Each member provided a brief demonstration of their work. <br> 2. **Issue Identified:** A potential conflict was found between the UI's event loop and the continuous device polling mechanism, which could cause the UI to freeze. <br> 3. **Solution:** The team decided to implement an observer design pattern to decouple the back-end logic from the front-end interface, using signals and slots. <br> 4. **Action Items:** Member A and Member B to collaborate on implementing the observer pattern. Member C to create mock device objects for testing before physical devices are integrated. |

---

### Meeting 4: System Testing & Finalization Strategy

| Category | Details |
|---|---|
| **Who** | **Attendees:** Member A, Member B, Member C, Member D. <br> **Leader:** Member D. |
| **What** | **Topic:** System Testing Results and Project Finalization Plan. <br> **Discussion:** Member D presented the results from the initial unit and integration tests, highlighting a list of bugs and their severity. The team then planned the final development phase, focusing on bug fixing, completing documentation, and preparing for the final project presentation. |
| **When** | **Date:** December 1, 2025. <br> **Time:** 09:00 AM - 10:30 AM. |
| **Why** | **Purpose:** To ensure the system is stable and robust by addressing critical bugs. The meeting also aimed to create a clear work plan for the remaining time to ensure all project deliverables are met on schedule. |
| **Where** | **Location:** University Library, Group Discussion Area. |
| **How** | **Actions & Outcomes:** <br> 1. The team reviewed the bug report and prioritized critical issues, such as a database persistence error and several UI layout inconsistencies. <br> 2. A code freeze date was set for December 5, 2025, after which only critical bug fixes will be permitted. <br> 3. **Action Items:** <br> - **Member C:** To resolve the database persistence issues by EOD. <br> - **Member B:** To fix all high-priority UI bugs. <br> - **Member A:** To finalize the User Manual and update the main README file. <br> - **Member D:** To prepare the system for user acceptance testing (UAT). |