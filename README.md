# **InnovateSolutions**

# Introduction
The purpose of this project is to redesign the existing murdoch job portal by using the portal created by the previous group as a base.

# Project Task List
- [ ] Implement proper input validation
- [ ] Improve Student/Employer registration page UI
- [X] *Update FAQ page (Optional)*
- [ ] *Remove "Recent Actions" pane from admin dashboard (Optional)*
- [X] Get emails working
- [X] Implement password reset feature
- [X] Make the website responsive with mobile layouts
- [X] Admin can edit employer profile
- [X] Disable close/reset buttons for closed jobs
- [X] Employer can reopen closed jobs
- [X] Remove "News" page
- [X] Remove "Murdoch University Home" page
- [X] Put the Help Desk links on the navigation bar
- [X] Added address to footer

# Version History
## 07/01/20 - 10:37PM
- Some pages have been redesigned.
- Dropdown aren't working so some urls have to be entered manually.
    ### Installations:
    - Run "pip install django-crispy-forms"
    - Run "pip install django==2.2.13"
    - Alternatively, you can just run "pip install -r requirements"

## 07/01/20 - 10:41PM
- Modification made to readme.md to show update times.

## 07/01/20 - 10:45PM
- Fixed issue with last instruction in "07/01/20 - 10:37PM"

## 07/01/20 - 11:07PM
- Made further modifications to theme.html.
- Made formatting changes to readme.

## 07/02/20 - 10:12AM
- Changed container to container-fluid.
- Moved header and footer to body (previous group kept it outside the body which I didn't realize).
- Changed container-fluid padding-left, padding-right to 0.

## 07/02/20 - 03:43PM
- Modified navigation bar.
- Moved View Jobs and View Applications from drop down to navigation bar for some users.
- Fixed signup button drop-down.
- Changed footer color to match navigation bar color.

## 07/01/20 - 10:41PM
- Modification made to readme.md to show update times.

## 07/01/20 - 10:45PM
- Fixed issue with last instruction in "07/01/20 - 10:37PM".

## 07/01/20 - 11:07PM
- Made further modifications to "theme.html".
- Made formatting changes to readme.

## 07/02/20 - 10:12AM
- Changed container to container-fluid.
- Moved header and footer to body (previous group kept it outside the body which I didn't realize).
- Changed container-fluid padding-left, padding-right to 0.

## 07/02/20 - 03:40PM
- Modified navigation bar.
- Moved some options from drop down such as My Applications and View Jobs to the navigation bar of certain users.
- Fixed signup button dropdown.

## 07/02/20 - 05:43PM
- Changed from black to a gray color to match murdoch website.
- Modified footer.
- Moved some elements around in the footer.
- Added a section that exists in the murdoch website.
- Added social media icons to the footer
    ### Known issues:
    - YouTube icon points to LinkedIn
    - Horizontal lines don't show up. Probably css issue.
    - Some icons don't match

## 07/02/20 - 09:25PM
- Redesigned the view jobs page to make it look better.
- Updated student registration form with new styles.
- Updated employer registration form with new styles.

## 07/03/20 - 06:03PM
- Fixed banners and styled them using bootstrap alerts.
- Fixed an issue with login page.

## 07/03/20 - 08:54PM
- Redesigned job details page.
- Modified reopen job behavior so that the "Edit Job" button disappears.

## 07/04/20 - 12:10AM
- Modified some of the font sizes for mobile layouts.
- Made the bottom navigation bar disappear on mobile.
- Implemented the bottom navigation as a dropdown for mobile devices.

## 07/04/20 - 12:35PM
- Fixed footer for mobile devices.
- Added new horizontal line that appears in footer for mobile layouts to separate various sections.
- Modified image on index.html to better fit mobile layouts.
- Added a new CountryField to various forms that ask for location.
- Updated requirements.txt to include django-countries
    ### Installations:
    - pip install django-countries
	
## 07/04/20 - 01:30PM
- Fixed YouTube link.
- Fixed missing Statistics page link.

## 07/04/20 - 04:34PM
- Redesigned View Jobs page.
- Put the filter jobs form into a popup window.

## 07/04/20 - 04:38PM
- Turned location field in filter form into a country field.
- Modified locations through admin dashboard

## 07/04/20 - 05:42PM
- Moved the jQuery code in View Students to an external file.

## 07/04/20 - 08:26PM
- Redesigned View Students page.
- Put the filter students form into a popup window.
- Transformed filter students form into a crispy form. (Not food, it's a different way of rendering forms)

## 07/05/20 - 10:38AM
- Fix "My Applications" button

## 07/05/20 - 12:15PM
- Modified the View Statistics page.
- Modified the Generate Statistics page.

## 07/05/20 - 12:55PM
- Fixed the footer for the My Applications page so that it doesn't cut out all of a sudden.
- Modified the My Applications page so that it looks better.
- Added a link to the View Jobs page on the My Applications page for students who haven't applied to any jobs.
- Fixed the View Jobs page so that students can actually apply for jobs.

## 07/05/20 - 01:47PM
- Changed index page image.
- Put blockquote inside image.

## 07/05/20 - 02:35PM
- Redesigned the sitemap page. It looks ugly still but it's not the final design.

## 07/05/20 - 03:25PM
- Redesigned Student Profile View
- Redesigned Employer Profile View
- Renamed "I'm a Student" and "I'm an Employer" under the Sign Up dropdown to "Student Registration" and "Employer Registration".

## 07/05/20 - 05:10PM
- Redesigned Edit Profile View for students.
- Redesigned Edit Profile View for employers.
- Brought back the help desk links and placed them inside the navigation bar.

## 07/05/20 - 06:02PM
- Fixed the job creation form.
- Fixed a bug which I accidentally introduced into the job creation form.
- Add some styles to the View Jobs page so that the footer doesn't get cut off.

## 07/05/20 - 06:40PM
- Fixed the Edit Job Listing Form.

## 07/05/20 - 07:59PM
- Modified FAQ page (played with styles).
- Modified Anti Scam page.
- Modified Terms page.
- Modified privacy page.
- Added new address to footer.

## 07/06/20 - 12:12PM
- Modified My HelpDesk Requests page.
- Moved HelpDesk templates to App folder.
- Changed font to Open Sans to match murdoch website.

## 07/06/20 - 12:36PM
- Redesigned Student Details page.

## 07/06/20 - 02:57PM
- Used jQuery to highlight the page the user is currently on at any given time.

## 07/06/20 - 03:41PM
- Fixed a bug I created that prevented the checkbox in Employer Registration from showing up.
- Fixed another bug I caused in Student Registration that prevented students from registering.

## 07/06/20 - 09:37PM
- Created two separate js files for both student registration and employer registration page.
- Added some live validation to the student registration page but it's still a work in progress.
- Fixed a bug where the datepicker object did not appear. Naturally, I was the one who accidentally created this too.

## 07/06/20 -10:00PM
- Fixed the behavior of the alumni toggle. The right fields are disabled this time.
    ### Known Problems:
    - The program still requires that both emails are entered. Problem probably exits because of the way the
     database is structure i.e. there is probably a rule stating that these two fields must exist.
     
## 07/07/20 - 09:45AM
- Removed CountryFields :sob: .
- Turned location into a dropdown which allows users to select a location from dubai.
- Fixed the issue where admins cannot edit jobs.
- Fixed the issue where the information of the job that an admin is editing wasn't shown.
    ### Known Problems:
    - Fix for edit job required removal company form fields but I've tried the original groups
    project and it doesn't work there either so it's an issue as old as time.
    
## 07/07/20 - 05:29PM
- Added more live validation functionality to Student Registration.
- Added live validation functionality to Employer Registration.
- Changed the list of locations and added some more. 
- Fixed a bug which prevented users from bringing up drop-down on Student Registration page.
    ## Known Problems:
    - The verification for the phone number field in the Employer Registration page doesn't work
    for some reason.
    - Still have to change the form in View Jobs and View Students.
    
## 07/07/20 - 08:50PM
- Redesigned View Students and View Jobs pages
- Renamed Table.css to View.css

## 07/07/20 - 09:41PM
- Added FAQs from a document created by the previous group who worked on 
this project 

## 07/07/20 - 10:57PM
- Fixed some issues with the sitemap

## 07/08/20 - 01:04PM
- Fixed some more issues with the sitemap
- Shortened some of the code in the forms.py files (Home and Student)
- Changed "View Profile" to "My Profile"

## 07/08/20 - 02:29PM
- Shortened some more code
- Fixed an issue where users can't view applicants after reopening a job
 and would normally have to reload the job details page
 
## 07/08/20 - 04:28PM
- Fixed a bug where after login the url would still show that you were on the
 login page despite having been redirected to the index page. This would cause issues
 where if you were to move to another page and then go back to the index page by
 clicking the back button it would give an error
 
## 07/08/20 - 05:22PM 
- Fixed a bug where employers can close a job without verifying whether or not
a student received that job.

## 07/08/20 - 05:33PM
- Removed "My HelpDesk Requests" from admin view
- Fixed issue where admin couldn't respond to HelpDesk requests

## 07/08/20 - 05:45PM
- Used CSS to modify the main tag to provide space between body elements of every
page that uses the theme.html body template tags and form from cutting off in the middle
of the screen.

## 07/08/20 - 05:59PM
- Fixed links to password reset pages

## 07/08/20 - 10:45PM
- Modified index
- Modified View Jobs
- Modified View Students
- Modified Job Details
- Added font awesome icon folder

## 07/09/20 - 11:16AM
- Fixed horizontal overflow that existed on all devices (At least I think I 
did based on what I've seen).
- Replaced the drop down which listed areas in dubai with a drop down that 
lists all 7 states of UAE.

## 07/09/20 - 12:01PM
- Removed Student ID field from Edit Student Profile page
- Added (AED) and (in Months) to the Salary and Duration columns respectively
- Turned skills into a dropdown in the Create/Edit Job pages

## 07/09/20 - 03:54PM
- Added a new section to index page.
- Hid the top user login elements for mobile users
- Created login elements in the middle of the page for mobile users.

## 07/10/20 - 12:21PM
- Fixed a bug where users would be able to access the link to create a new job.
- Fixed a bug where admins could not create/edit jobs.
- Redesigned both the View Jobs and View Students pages.
- Added a link on the View Jobs filter form that lets users view all jobs.

## 07/10/20 - 01:29PM
- Fixed an issue with create job form not rendering for admins

## 07/10/20 - 02:30PM
- Made some CSS modifications in the privacy and terms and conditions pages.
- Replaced the social media icons in the footer with font-awesome icons.

## 07/10/20 - 11:50PM
- Created an Alumni table
- Modified the program to be able to handle Alumni models (to an extent)

## 07/11/20 - 12:42PM
- Modified many pages for alumni students
- Redesigned some pages
- Created a View Alumni page
- Created a new class called Majors which lets an admin add more majors through
the dashboard and these majors are assigned to students
- Created a Filter for Majors in the View Students and View Alumni pages
- Added a button to view alumni candidates on job details page
    ### Known Problems:
    - The View Alumni Candidates button on job details gives an empty list of
    alumni
    
## 07/11/20 - 01:03PM
- Fixed a typo in the View Alumni page where the filter form was called 
"Filter Student Listings" rather than "Filter Alumni Listings".

## 07/11/20 - 06:30PM
- Made some minor CSS modifications.

## 07/12/20 - 02:53PM
- Removed Salary field from Jobs
- Added Minimum Salary and Maximum Salary to Jobs
- Added Duration Type to Jobs
- Modified Job Creation form
- Modified job details
- Added message regarding consent above Apply button in the job details page for students
- Modified the job cards so that the minimum and maximum salary are visible
- Modified job filter for new fields
- Modified footer as per client request

## 07/12/20 -10:44PM
- Added working email functionality
- Fixed password reset forms
- Modified look of the password reset forms
- Modified some pages for the email functionality
- Fixed a bug where admins couldn't create jobs (I created this...I mean the bug)

## 07/12/20 - 11:45PM
- Changed the index image
- Removed the quote from Theodore Roosevelt
- Fixed HelpDesk request page footer cutting off
- Added alumni object to generate statistics page

## 07/13/20 - 10:59PM
- Modified registration pages
- Used new date widget
- Added AJAX validation in registration pages to prevent username re-use
- Modified live validation in registration pages
- Prevented submission of valid registration forms

## 07/14/20 - 12:58PM
- Added input validation to Edit Profile pages
- Fixed the issue where View Alumni Candidates in job details would show
 an empty list
 
## 07/14/20 - 06:41PM
- Changed the name of the "Apply" button to "Search" in filters
- Wrote AED besides MIN, MAX salary in Post a Job
- Updated Sitemap
- Added Student ID as optional field in Alumni Registration
- Redesigned HelpDesk page

## 07/14/20 - 11:07PM
- Added a confirmation message for when jobs are created
- Redesigned the job details and View Jobs pages

## 07/14/20 - 11:18PM
- Applied HelpDesk redesign to admin view

## 07/15/20 - 03:16PM
- Redesigned some pages
- Added recent jobs to index

## 07/15/20 - 04:29PM
- Fixed mobile layout for View Jobs and index

## 07/15/20 - 08:24PM
- Fixed bug that prevented users from editing jobs
- Remove Sites from admin view
- Redesigned View Students/Alumni pages
- Changed date entry fields in Filter Students Listing to dropdown

## 07/15/20 - 05:39PM
- Added details of murdoch career portal email
- Modified various functions to send emails
- Fixed an issue with live validation in alumni registration

## 07/15/20 - 11:39PM
- Fixed statistics page
- Fixed Apply button not disappearing
    ### Goofs
 - Spend the whole day trying to fix a bug that doesn't exist
 
## 07/18/20 - 08:06PM
- Fixed the issue with View Students not running.
    ### Failed
    - Failed to fix the issue mentioned regarding reapplication of jobs because I don't know how
    to replicate that issue and as far as I can see it's working fine.
    
## 07/19/20 - 01:02PM
- Changed text for View Student Candidates and View Alumni Applicants.
- Modified recent jobs pane on index page to show recent 3 jobs.
- Changed behavior of send_email functions to fail silently.