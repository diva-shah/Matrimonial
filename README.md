# My Mate - A Matrimonial Website

**Table of Contents**

<!-- vim-markdown-toc GFM -->

* [Introduction](#introduction)
* [Sample](#sample)
* [Project Setup](#project-setup)
    * [Basic requirements](#basic-requirements)
    * [How to Setup the project](#how-to-setup-the-project)
* [User Guide](#user-guide)
    * [Navigation](#navigation)
    * [Registeration](#registeration)
    * [Profile](#profile)
    * [Partner preference](#partner-preference)
    * [Personal contact](#personal-contact)
    * [LIKES PAGE](#likes-page)
    * [USER PROFILE PAGE](#user-profile-page)
    * [PREFERENCE PAGE](#preference-page)
    * [SEARCH PAGE](#search-page)
* [Project Details](#project-details)
    * [Made By](#made-by)
    * [Made For](#made-for)
* [Acknowledgements](#acknowledgements)

<!-- vim-markdown-toc -->
# Introduction
This is a website that we have created that acts as a dating app. You can like someone by swiping right and reject someone by swiping left. We allow profile setup and allow setting up preferences.

We have built this project using Django Framework and blah blah... 

The complete user guide for this application is available [here](./Docs/Project%20Inspiration.md).

# Sample

[![Demo Video](https://img.youtube.com/vi/TcpuCZkloCA/0.jpg)](https://www.youtube.com/watch?v=TcpuCZkloCA)

# Project Setup

## Basic requirements

- Python 3.11
- pip3

## How to Setup the project

Clone the repository to your computer. Open a new terminal and type:

```bash
git clone https://github.com/pythonqueen7/Matrimonial
```

Open the repository using
```bash
cd Matrimonial
```

Install the dependencies from requirements.txt using:
```bash
pip install -r requirements.txt
```

Once the dependenices are installed, run the application using:
```bash
python3 application.py
```

# User Guide

## Navigation

The navigation consists of  'home', 'search', 'messages', and 'logout'.  The said buttons will navigated to their respective pages. The navigation will be in the upper right corner of the website, while opposite to that on the left upper corner will be the site's name, which also link to the homepage.

## Registeration

Register.html is one of four parts of the registration process. It asks for the user's username, password, email, birthday, gender, country, reason for joining, where they
heard about us, and a security question. All the questions are stored in the db for reference. These are all general information except for the security question.
The security question is helpful when the user goes to forgot password. It's hard to know if the same user that registered is changing their password, so the
security question helps to see if a hacker is behind the computer or not.


## Profile

## Partner preference

## Personal contact

## LIKES PAGE
MyMate has a feature to like and unlike profiles. If they like a profile, the like button gets inverted and says "Unlike". And if clicked again, it inverts back
    and says "Like". This was done by if conditions. When the user likes a profile, they are inserted to our profileLikes table and using that information, we can make a
    gridview of all the liked profiles. But if they click "Unlike", they are deleted from the profileLikes table. On the hompage, there is a section "My Likes". When the user
    clicks on that, they see 2 tabs, one is "My Liked Profiles", and the other is "Profiles that Liked Me". The profiles that the user liked come as a gridview and the user
    can click on their name and be taken to their profile. "Profiles that like me" shows all the profiles that liked the user in a gridview. This helps organize everything and
    is meant to help the user in the end.

## USER PROFILE PAGE


## PREFERENCE PAGE


## SEARCH PAGE

# Project Details
## Made By
- [Diva Shah - pythonqueen7](https://github.com/pythonqueen7)
- [Diva Shah - pythonqueen7](https://github.com/pythonqueen7)
- [Diva Shah - pythonqueen7](https://github.com/pythonqueen7)
## Made For
- Harvard CS50 Graduation Project

# Acknowledgements
- The initial flask setup, session configuration and login was borrowed from the finance problem set of the [cs50x course](https://cs50.harvard.edu/x/2023/)
- [GeekforGeeks](https://www.geeksforgeeks.org/) helped us with documentation and implementation of Python.
- W3Schools helped with Algorithm development.
- Discord Server for CS50 for all the doubts and problem solving.
