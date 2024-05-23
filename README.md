# Projecto

A web application built with Django, designed to manage courses and proposals for different types of users.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [User Roles and Capabilities](#user-roles-and-capabilities)
- [Getting Started](#getting-started)

## Introduction

This project is a Django-based web application that facilitates the management of courses and proposals. It supports multiple user roles with varying levels of access and functionality, ensuring a seamless and efficient user experience.

## Features

- **View Running Courses**: Unregistered and registered users can see the list of ongoing courses.
- **View Notices**: All users can see announcements and notices.
- **Proposal Submission**: Students can submit proposals for courses.
- **Supervisor Assignment**: Supervisors can be assigned to student proposals, and notifications are sent to team leaders.
- **Proposal Management**: Teachers and super users can manage proposals, including marking, searching, and filtering.
- **Downloadable Reports**: Proposal lists and course results can be downloaded in PDF and CSV formats.
- **Course Management**: Super users can add, update, or delete courses.
- **Notice Board Announcements**: Super users can announce information on the notice board.
- **Teacher Management**: Super users can manage teacher information.

## Technologies Used

- **Django**
- **HTML**
- **CSS**
- **Bootstrap**
- **jQuery**
- **JavaScript**
- **Ajax**

## User Roles and Capabilities

### Unregistered User

- ⚡ Can see the list of running courses
- ⚡ Can see the notices

### Student User

- ⚡ All features of an unregistered user
- ⚡ Can submit a proposal for a course
- ⚡ Can see the supervisor assigned to their proposal
- ⚡ Team leader will receive an email notification when a supervisor is assigned

### Teacher User

- ⚡ Can see the list of submitted proposals for a course
- ⚡ Can see the count of teams they are assigned to
- ⚡ Can mark a student's proposal
- ⚡ Can search for a proposal with a specific student ID
- ⚡ Can see the list of proposals under their supervision
- ⚡ Can download the proposal list in PDF and CSV format

### Super User

- ⚡ All features of a Teacher User
- ⚡ Can add a new course
- ⚡ Can update an existing course
- ⚡ Can delete a course
- ⚡ Can announce something on the notice board
- ⚡ Can download the result of a currently running course in CSV/PDF format
- ⚡ Can assign/update supervisors for a proposal
- ⚡ Can update/delete a proposal
- ⚡ Can filter the proposal list by:
  - Assigned
  - Unassigned
- ⚡ Can download the result of a specific course
- ⚡ Can manage teachers

## Getting Started

To get a local copy up and running, follow these steps.

### Prerequisites

- Python: [Install Python](https://www.python.org/downloads/)
- Django: Install Django using `pip`
- An IDE (PyCharm Professional recommended)

### Installation

1. Clone the repository:
    ```sh
    git clone git@github.com:cloud-007/projecto.git
    ```
2. Navigate to the project directory:
    ```sh
    cd your-repo
    ```
3. Create and activate a virtual environment:
    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
4. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```
5. Run the Django development server:
    ```sh
    python manage.py runserver
    ```
