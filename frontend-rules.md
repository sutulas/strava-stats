Follow the following rules and guidelines when creating the frontend:


You are tasked with designing a professional and clean frontend to allow a user to login with strava, then interact with the backend services in ./backend.
Start by examening the ./backend folder to understand the available apis, use backend\BACKEND_DOCUMENTATION.md as a source for context about the backedn and \frontend-old\src\app\services as a guide to how to interact with the apis.

The website should start with a login with strava page, that should clearly display the strava logo and say "built with strava" to comply with strava dev api guidelines. strava logo is available at frontend-old\src\assets\strava-2.svg

The site should then use the data service to load the users data. Display some sort of loading/skeleton screen at this time. Once the data is loaded the user can access the site. There should be a pages, including a profile page with details from the users strava page (username, photo, etc..) use the strava api to grab these. Also display some interesting charts on the user's profile page based on their running data. Choose 2 or 3 visualizations that would look cool. Try and make it original and not just copy stravas exisiting page. this is what the data will be formatted like: 
id,start_date,name,distance,moving_time,elapsed_time,total_elevation_gain,type,start_date_local,average_speed,max_speed,average_cadence,average_heartrate,max_heartrate,suffer_score,year,month,day,day_of_week,time
15780318235,2025-09-11 20:38:06+00:00,New territory,9.0046599836,67.6,73.53333333333333,51.5,Run,2025-09-11 16:38:06+00:00,7.506856982927512,5.587916666666667,82.4,151.3,163.0,34.0,2025,9,11,Thursday,16:38:06
also on the login page include a logout button.

The next page is the main part of the website, this is the data analysis page. On this page the user will be able to enter a query which is then passed to the backend, and the resulting message or chart is returned. Make this page user-freindly, and clean.

Lastly include a page that shows some of the data and gives a download option. 

Ensure this site is production ready not just in code style but in frontend style.

Source components and style from ./dev-fox-ui-mui-dashboard-theme. This is a comprehensive styling framwork with components that will be very useful in designing this frontend. Use this folder as context for how to design. Use black and white as main colors with a subtle organe highlight if possible.


My style vision:

1. Overall Style

Theme: Dark mode with high-contrast white text and grayscale accents.

Layout: Classic sidebar + topbar + main content structure.

Design Language: Minimalist, flat, slightly neumorphic with clean cards and strong hierarchy.

Typography: Bold headings, medium-weight subheadings, light body text. Sans-serif font, modern and clean (e.g., Inter, Roboto, Poppins).

2. Sidebar (Left Navigation)

Background: Solid black (#000 or near-black).

Logo Area: Top-left with icon + brand name in white.

Menu Items:

White text (#fff) with muted gray (#aaa) for secondary items.

Icons (line-style, minimal, likely SVG/Lucide or Feather).

Hover/active state → item background becomes lighter (#111/#1a1a1a), text stays white.

Current page highlighted with rounded white pill background and black text


3. Visual Design Principles

Spacing: Generous padding (20–30px inside cards).

Shadows: Very minimal or none (flat look).

Rounded Corners: Subtle (8–12px radius).

Contrast: White text on near-black, secondary text muted.

Consistency: Every card follows the same size, padding, and typography system.
Ask futher questions/guidance if needed.