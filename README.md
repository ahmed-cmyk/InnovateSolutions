# **InnovateSolutions**

# Introduction
The purpose of this project is to redesign the existing murdoch job portal by using the portal created by the previous group as a base.

# Project Task List
- [ ] Implement proper input validation
- [ ] Improve Student/Employer registration page UI
- [ ] *Update FAQ page (Optional)*
- [ ] *Remove "Recent Actions" pane from admin dashboard (Optional)*
- [ ] Get emails working
- [ ] Implement password reset feature
- [ ] Make the website responsive with mobile layouts
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