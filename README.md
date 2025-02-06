## Assignment: Unit Testing and Database Operations

### Objective:

In this assignment, you will learn how to write unit tests for a database-driven application, add functions for updating and deleting users, and generate a coverage report. You will also improve the code quality and submit a comprehensive report in PDF format.

### Instructions:

#### Part 1: Unit Tests

Write unit tests for the existing Database class using a mocking library (e.g., unittest.mock). Ensure that you cover all the methods, including insert_user, get_user, update_user, and delete_user.
Do not use an in-memory database for testing. Instead, use mocking to simulate the database behavior. This is because in-memory databases can lead to test pollution, where tests interfere with each other's data. By using mocking, you can isolate each test and ensure that they run independently.

#### Part 2: Update and Delete Functions

Add functions for updating and deleting users to the Database class. Ensure that these functions are properly tested using unit tests.
Use the same mocking approach as in Part 1 to test these new functions.

#### Part 3: Coverage Report

Generate a coverage report using a tool like coverage.py. This report should show the percentage of code covered by your unit tests.
Include **the coverage report** in your submission.

#### Code Improvements

Review the existing code and suggest improvements. This could include refactoring, optimizing queries, or improving error handling.
Implement these improvements and include a **brief explanation** of the changes in your report.

#### Submission

Submit your assignment as a **PDF** document.
Include images to illustrate your points, such as screenshots of **the coverage report** or **database schema**.
Ensure that your report is well-organized and easy to follow.

### Getting Started

Install the necessary requirements using pip install -r requirements.txt.
Use a SQLite viewer extension (e.g., sqlite3 command-line tool or a GUI client like DB Browser for SQLite) to view the database schema and data.

#### Grading Criteria

1. Unit tests (40%): Completeness, correctness, and coverage of tests.
2. Update and delete functions (30%): Correctness, testing, and implementation.
3. Coverage report (10%): Accuracy and completeness of the report.
4. Code improvements (10%): Quality and effectiveness of suggested improvements.
   Report quality (10%): Clarity, organization, and overall quality of the report.
   Deadline

Submit your assignment by the deadline.

### Late Submissions

not allowed. Upload your assignment early to avoid server overloading issue.
