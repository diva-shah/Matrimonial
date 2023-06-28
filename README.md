#### project: Matrimonial Website
#### Video Demo:  https://www.youtube.com/watch?v=TcpuCZkloCA
#### Group members: pythoqueen7, myilm

## Worked on:

# pythoqueen7
1. register
2. Likes
3. Block
4. Message button
5. Preferences
    a. preferences
    b. edit profile
    c. edit partner preference
    d. edit contact information
    e. change username
    f. change password
    g. change email
    h. blocked users
    i. delete profile

# myilm
1. navigation links
2. registration
    a. profile,
    b. partner preference,
    c. contact information
3. index page
    a. messaging panel,
    b. browse profiles with tabs,
    c. user profile card
4. user profile
5. search profiles

-----------------------------
The aesthetics page allows the user to make their profile Live or Hidden. If its Live,
other people can view the profile, but if its Hidden, nobody can view their profile. They can also "Show" picture guidelines or "Hide" picture guidelines which just shows
or hides their profile picture. Last, they can enable/disable messaging. If the user does not want to message others, they can disabled their messaging. But, if they try
messaging others with messaging disabled, they get a pop up saying to turn it back on. However, if their messaging is enabled but the person they are trying to contact has
it disabled, they will see a pop up saying that the person they are trying to contact has their messaging disabled.

Blockedusers.html gives a gridview of the profiles the user has blocked. There is an option to unblock
an user and if clicked, the user will be unblocked. This was done by getting data from sql commands and passing that data onto the html files. Using forloops, it
showed each profile that was blocked and below that profile is an option to unblock.

Change email, change password, and change username are all pages that just edit the personal information of the user. If the user clicked change email, they will see their
previous email and be asked to enter the new email and their password. The password is needed to make sure that this not a hacker that is changing the user's personal
information. Change password prompts the user to enter the new password and to retype it, and to also enter the old password for security reasons. On the change username
site, the user will see their old username and they can change that area to whatever they want as their new username. They are also asked to enter their password to make
sure that it is not a hacker changing their username. If the password is incorrect, an apology pops up saying that "Incorrect Password". However, if the password is correct
the information updates.

The delete page takes the user to such a page that allows the user to delete their profile. On the page are checkboxes of the
reasons that the user wants to leave this website, which is required, there is an option for "Other" if there is a reason that is not listed that the user wants to check.
There is also a comments/suggestions box which allows the user to give feedback, this is not required. Last, the delete page has a password area where the user must enter
their password to delete their profile to make sure that the same user who registered is the user who is deleting their profile. If no reason for leaving is selected,
then the user receives an apology saying that you must select a reason for leaving. But, if all goes well, the user successfully deleted their profile.

Edit contact, edit preferences, and editting (edit profile) are all meant for the user to change any information that needs to be updated from the time they registered.
On these pages the user will see the same questions that were asked to them the first time when they were registering. When the page opens, they will see the answers to the
questions that were asked that are text inputs and not drop down menus. Once they click update, the information updates. The user was able to see the answers to the
questions because the python functions passed the information from the sql commands to the html files, and then the values were set by using the data passed on.


Forgot and forgot password are meant to change the password of the user because they forgot it. Since the user forgot their password, the session id is unknown. So,
the user is taken to a site that first asks for their username and then that information is passed on to forgot.html and the page is redirected to /forgot. Now the user's
username is known, the tables can be updated correctly. When registering the user was asked a security question meant for this scenario. Anyone can click forgot password and
enter a user's username and then change their password. But, it is important to know if a hacker is behind the computer or not. So, the security question is asked that
the user answered while registering and if the answer is correct, we update their password, but if its not, an apology comes up saying "Incorrect answer to your question".

Report.html is the report function. On each profile there is a button to report a user. When the user clicks the report button, they are redirected to a page that is similar
to delete. There is a section asks for the reason of report. With the use of lists and forloops, the implementation of checkboxes was successful. The user could check any
reason, or select "Other", and then has to give an explanation. Both of these fields are required. This information is then inserted into our tables. If the user does not
select a reason for reporting, an apology pops up saying that you have to select a reason.


When the user clicks "Block" on any profile, the block button turns to "Unblock" and the Like and Message section says "Blocked"
with white lettering and a red background. This user is then inserted into the table and this information is then updated to blocked users. When the users clicks block,
they stay on the same profile and can go anywhere from there. They can also unblock the user from there and everything goes back to how it was before. Also, if the user
previously liked this profile then blocked the profile, they would be removed from the likes list. Meaning that when, or if, the user unblocks this user, they will not
have them as liked anymore.

User.html is everything you see on the profiles. The implementation of the aesthetics of the Like and Message button was done by if conditions. If the user liked this profile,
the like button would change to "Unlike", or else it would stay the same as before with "Like". Same with the block button. If the user blocked this profile,
the block button would say "Unblock", and the Like and Message section would turn to "Blocked" with white lettering and red background. However, the user is not blocked,
the like button and message stay the same, and block button says "Block".

Some tweaks were made to the search and index.html as well. There is not point of the Profile Status if it is not used. So, the sql commands were changed and gave data of
the users who had a profile status of 'Live'. This made it so that only profiles with a profile status of 'Live' were shown on the homepage and search page.
This was done by adding a WHERE condition in the sql commands saying "user.profileStatus = 'Live'". This was also added to the MyLikes page and Blocked users page.
So, if a user liked or blocked a user, but then later that user turned their profile status to "Hidden", they will not show up in those pages anymore.

When the message button is clicked, the user is taken to function written in javascript. The attributes are choice and otherPerson. The values passed into the function for
choice is wheter the messaging is disabled or not for the user, and for otherPerson the information passed is if the person the user is trying to contact has their
messaging disabled. In the function I do if conditions to see if the messaging is disabled for the user or for the person they are trying to contact. If the condition
passes, a pop up comes up saying that either you have to turn on messaging or that the user they are trying to contact has messaging disabled. However, if the conditions
are false, the function is redirected to the python function of messaging. Here it checks if the user is a gold member or not. If the user is not a gold member, they are
redirected to page where they can upgrade to gold since only gold members have the feature to message others.

------------------------------------


#### Description:

For this project, we have chosen to create a matrimonial website. This is a two person project divided into sections by features that each person takes on. The flow of the website is such as that upon visiting the website, one may login if they already have an account or they can register to proceed. Under the login form, the end user will have the option to show password as well as a forgot password link to reset their password. The registration process itself is a four part process. First part is the registration, which will allow one to signup for a username and be allowed to login. The other three parts are for creating one's profile. Only when all parts are completed will the end user be allowed into the site. All registered users will be registered as basic users, and to enabled extra features, such as messaging, they would need to upgrade to a gold member.

Once's logged in, the end user will land on the index page. The index page will consist of a panel to view messages, a tabbed panel below messages listing all the profiles. The tabs will be of three count, first one showing all the profiles, second one showing those near proximity to the end user by region and the last one showing all profiles registered within the last 6 months. The left of these two panels will be end users profile card from where the user may access their photo gallery, likes, profile and preferences. The website will also show navigation on the upper right corner for a logged in user who has completed their profile.

A user profile being viewed will be as such that a profile card and pertinent information will be displayed on the left side of the page and the right side will consist of bio-data and partner preferences of the profile owner. The profile card will consist of the profile owner's photo, their username and age and below that a 'likes' and 'message' button. The 'like' is a toggle feature that allows one to add the profile to their favorites. Below the pertinent information will be two buttons, one to report the profile and the other to block the profile owner. The report button will lead to another page with a form to provide details for reporting. The block bottom will be a toggle that can be blocked/unblocked from the profile as well as from the logged in user's preferences.

There will be a search page as well which will allow the user to search profiles based on a number of criteria. The user will be able to view profiles by gender as well as most of the data provided within the profiles.

The preferences link leads to a user preference page where a number of options are available. Here the use is able to change their preferences, edit parts of their profile, manage their photos, and hand account and security information, such as change username/password/email, look at membership history, blocked users with unblock capabilities, and delete their profiles.

The photos and messaging has not been implemented into the site, nor an admin page. They maybe considered in the future if further development is of interest. As for rest of the features and files, they are as follows:

NAVIGATION

The navigation will consist of  'home', 'search', 'messages', and 'logout'.  The said buttons will navigated to their respective pages. The navigation will be in the upper right corner of the website, while opposite to that on the left upper corner will be the site's name, which also link to the homepage.

REGISTRATION

1. register
    Register.html is one of four parts of the registration process. It asks for the user's username, password, email, birthday, gender, country, reason for joining, where they
heard about us, and a security question. All the questions are stored in the db for reference. These are all general information except for the security question.
The security question is helpful when the user goes to forgot password. It's hard to know if the same user that registered is changing their password, so the
security question helps to see if a hacker is behind the computer or not.


2. profile

3. partner preference

4. personal contact


INDEX PAGE


LIKES PAGE

    MyMate has a feature to like and unlike profiles. If they like a profile, the like button gets inverted and says "Unlike". And if clicked again, it inverts back
    and says "Like". This was done by if conditions. When the user likes a profile, they are inserted to our profileLikes table and using that information, we can make a
    gridview of all the liked profiles. But if they click "Unlike", they are deleted from the profileLikes table. On the hompage, there is a section "My Likes". When the user
    clicks on that, they see 2 tabs, one is "My Liked Profiles", and the other is "Profiles that Liked Me". The profiles that the user liked come as a gridview and the user
    can click on their name and be taken to their profile. "Profiles that like me" shows all the profiles that liked the user in a gridview. This helps organize everything and
    is meant to help the user in the end.

USER PROFILE PAGE


PREFERENCE PAGE


SEARCH PAGE

Acknowledgements:
The initial flask setup, session configuration and login was borrowed from the finance problem set of the cs50x course. The two websites GeeksForGeeks and
W3SCHOOLS also helped with the implementation of this website.

During the course I received lots of help from the Discord chat of cs50 and all of my submissions of the credits given to what was not mine; I would encourage you to look at those credits to make sure nothing is wrong.
