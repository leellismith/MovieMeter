<h1 align="center">MovieMeter</h1>

<h2 align="center"> A Movie Review Site</h2>

<h2 align="center">Milestone Project 3 - Lee Smith</h2>

![Am I Responsive Image](readme-docs/testing/MM%20-%20amiresponsive.PNG)


## <p align='center'>[MovieMeter Live Site](https://moviemeter-e678ab17db18.herokuapp.com/)

## <p align='center'>[MovieMeter Repository](https://github.com/leellismith/MovieMeter)

# UXD

# Purpose of the Project

I have decided to create a movie review site that users can come to the website and search any film to review.

I am aiming to create a website that feels easy to use by being up to date and steamlined.

The website is designed to give information about the films they want to review while being able to see other user's reviews.

The site also give the user full CRUD functionality by Creating, Reading, Updating and Deleting reviews their own reviews.

# User Stories

* As a user, I would like to be able to visit and search for a film.
* As a user, I wouuld like to see other users reviews.
* As a user, I would like to be able to make a review.
* As a user, I would like to see all my reviews.
* As a user, I would like to website to look good.
* As a user, I would like to be able to change or delete my reviews.

## Steps to be taken

1. Research websites.
2. Sketch up designs.
3. Create wireframes designs.
4. find mixed content that works together (Colour Scheme, Font Styles and Background).
5. Find how the content will work together.
6. Design Website.
7. Create Website (Using API, Mongodb, Animated background.)
8. Test website.
9. Deploy Website.

# Features

* __Background Image__
    > The animated background was selected to give the website a look of excitment.

* __Search Bar__
    > On the home screen you will locate a search bar which you will be able to search for a film and find information about the film. The search will find either find the film in mongodb or will search for in the API and then store it in the mongodb database.

* __Carousel__
    > Also on the home screen you will film a carousel which will on refreshing the page will randomise the 8 films shown in the carousel.

* __Reviews page__
    > The reviews page shows all reviews made by users who have an account.

* __Profile Page__
    > After the user logs in, they will be sent to an easy access profile page, that has links to Reviews, Manage reviews and make review.

* __Add Review Page__
    > Only a user that is logged in is able to see this page. All the user needs to do is search the film and then the film title and film poster is shown with a text box giving the user 200 characters to review the film. Below the text field are two boxes for submit review and cancel review.

* __Manage Revie Page__
    > Only a user that is logged in is able to see this page. The manage reviews page is like the reviews page but will only show the reviews the user has made. These reviews have two buttons in them. The first box is an update box which give the user the option to change what their review says and save the update to the database. The second box is a delete box which will delete the review from the database.




## Future Features

* Like and dislike feature.
* Randomizer film picker.
* A page when users just search by category.
* A option for users, to click and go to a website to buy the movie if not seen.
* An option for users to select reviews for selected films.

# Typography and Color Scheme

The Colour Scheme will include of HEX colours -

* `#FAFAFA` - White
* `#000000` - Background cover incase failed animated background.
* `#c7c7c7` - Grey hover color
* `#06060696` - Black with opacity
* `#ff0000` - Red for the Cancel or delete buttons

These colours work well together and will make the website clear and visually appealing.

# Wireframes

## Mobile Wireframe

![Mobile Wireframe](readme-docs/wireframes/Wireframe%20-%201-2%20mobile.PNG)
![Mobile Wireframe](readme-docs/wireframes/Wireframe%20-%202-2%20mobile.PNG)

## Tablet Wireframe

![Tablet Wireframe](readme-docs/wireframes/Wireframe%20-%201-2%20tablet.PNG)
![Tablet Wireframe](readme-docs/wireframes/Wireframe%20-%202-2%20tablet.PNG)

## Desktop Wireframe

![Desktop Wireframe](readme-docs/wireframes/Wireframe%20-%201-2%20desktop.PNG)
![Desktop Wireframe](readme-docs/wireframes/Wireframe%20-%202-2%20desktop.PNG)

# Technology
* __HTML__
* __CSS__
* __Python__
* __JavaScript__
* __Hover.css__
* __FlexBox__
* __Bootstrap__
* __Font Awesome__
* __Google Fonts__
* __Git__
* __GitHub__
* __Heroku__
* __Mongodb__
* __Figma__
* __vantajs__
* __jsdelivr__
* __favicon__

# Testing

## Code Validation

### __W3 Validator__

#### __Home Page__

![Site Validation](readme-docs/testing/MM%20-%20HTML%20Validator.PNG)

#### __CSS Validation__

![CSS Validation](readme-docs/testing/MM%20-%20CSS%20Validator.PNG)

## __Lighthouse Testing__

#### __Home Page__

![Home Page Validation](readme-docs/testing/MM%20-%20Home%20Page%20-%20Lighthouse.PNG)

#### __Reviews Page__

![Reviews Validation](readme-docs/testing/MM%20-%20Reviews%20-%20Lighthouse.PNG)

#### __Login Page__

![Login Validation](readme-docs/testing/MM%20-%20Login%20Page%20-%20Lighthouse.PNG)

#### __Sign Up Page__

![Sign Up Validation](readme-docs/testing/MM%20-%20Register%20Page%20-%20Lighthouse.PNG)

#### __Add Review Page__

![Add Review Validation](readme-docs/testing/MM%20-%20Add%20Review%20-%20Lighthouse.PNG)

#### __Manage Reviews Page__

![Manage Reviews Validation](readme-docs/testing/MM%20-%20Manage%20Reviews%20-%20Lighthouse.PNG)

#### __Profile Page__

![Profile Validation](readme-docs/testing/MM%20-%20Profile%20-%20Lighthouse.PNG)

## __Jshint Testing__

![Javascript Site Validation](readme-docs/testing/MM%20-%20Jshint.PNG)

## __CI Python Linter Testing__

![CI Python Linter Validation](readme-docs/testing/MM%20-%20CI%20Python%20Linter.PNG)

# Test Cases

## User Experience 

### __Home 

    When the user first comes to the MovieMeter site the will be greeted with a up-to-date interface displaying a random selection of 8 movies shown on a carousel.

    The page also has a search bar for the user to be able to search for any movie and find information about the movie.


### __Reviews Page__

    Any user who vists the site will be able to view all reviews on the site, they will be able to view the movie poster, movie title, review of the movie and when the review was made but only logged in users are able to make reviews.

### __Login Page__

    For the users who have already signed up the login page is straight forward and only requires a username and password to sign in. Once user has signed in they will be sent to the profile page.

### __Sign Up Page__

    The sign up page matches the look of the login page, and only required a username and password to signup to start reviewing films.

### __Add Review Page__

    The add review page has a search bar feature where the user can search for films. Once the movie has been selected the users will see the movie title, movie poster and a review text box with a save review button and cancel review button if they decide the do not want to make the review.

### __Manage Reviews Page__

    If the user decides they are not happy with their review they can vist the manage reviews page where the user is able to see all the reviews they have made. The user is able to update the review or if they decide that they don't want to anymore they can delete the review.

# MongoDB Non-relational Database

### First Collection -

    How I decided to store data to mongodb I decided to user an API which retrieved the data. The movie information from the API is then stored in my database for future searches.
    Data is stored in this collection as:
            Tilte :
            Actors :
            Director :
            Genre :
            Poster :
            Rated :
            Released :
            Runtime :
            Year :
            imdbID :
            imdbRating :

### Second Collection - 
    This collection stores the movie reviews, This uses the nearly the same retrieval method as the first collection but a smaller amount of data for the collection.
    Data is stored in this collection as :
            movie : 
            review :
            image_url :
            user : 
            timestamp :

### Third Collection - 
    This collection stores the data of users.
    Data is stored in this collection as :
            username :
            password :


    
    

# User Testing

| Users | Results | Fixed Issues |
|--- |--- |--- |
| First User | Found issue where they where able to make a review from the main page if they clicked on the carousel without being logged in. | Fixed by removing the function to click on the corousel and added a button which only shows for logged in users. |
| Second User | Issue found in Adding a review where it only affects one film - Fight Club | Bug fixed by changing movie_details = get_movie_details at line 184 to movie_details = search_movies_in_api(movie_title) |
| Third User | No Issues Found | N/A |
| Fourth User | No Issues Found | N/A |
| Fifth User | No Issues Found | N/A |

# Manual Testing

I used manual testing and debugging in the devlopment of this project. I used this to look into every feature and functionality to ensure it was working correctly. The hands on approach allowed me to ensure that this project would meet the requirement while uncover any potential issues straight away.

# Fixed Bugs

* Fixed a bug with the search bar where when a user selected A film e.g StarWars it bring forward all star wars films which is great but when the user just selected Star Wars: Episode IV - A New Hope it throws up No movies found for 'Star Wars: Episode IV - A New Hope'. This seemed to be happening with long named full titles. To work around this I changed the database query to handle exact matches better and for the search to be more flexible.

* Fixed issue with Heroku Live site where I wasn't able to view my live site after searching on the heroku site and checking my code I realised that API(omdbapi) in my env.py file were not added to Config Vars after I added these and committed the live site worked.

### Supported Screens and Browsers

| Screens | Supported |
|---|---|
| Phone | Yes
| Tablet | Yes |
| Laptop | Yes |
| Desktop | Yes |
---
Browsers | Supported|
|---| ---|
| Google Chrome | Yes |
| Safari | Yes |
| Firefox | Yes |
| Mircosoft Edge | Yes |
---

# Deployment

## MongoDB Non-Relational Database

[MongoDB](https://www.mongodb.com) was used for the Non-Relational database for this project.

To get your own MongoDB Database URI. Follow these steps.

>1. Go to [MongoDB](https://www.mongodb.com).
>2. Sign up for a free account or login if you have an account already.
>3. Once Logged in, Click "__Build a Cluster__"
>4. Choose your preferred cloud provider (AWS, Azure, GCP) and region (Nearest region to you). 
>5. Select a Cluster Tier
>6. Go down and then select your Cluster Name e.g myfirstCluster.
>7. Once you have done that click on Database on the left. 
>8. Click on the __Collections__ tag and click on Create Database.
>9. Give you Database a name e.g moviemeter and click created.
>10. Just below the Created Database you will now see your Database name. Click on that.
>11. Click on Create Collection and add as many as you need. This project only required 3 __movies__, __reviews__ and __users__.
>12. Go back to the __overview__ and  Click on the __Connect__ button.
>13. Click __Connect Your Application__.
>14. Copy the connection string, and replace `<password>` with your own password.


## Heroku Deployment
[Heroku](https://dashboard.heroku.com/) was used for The MovieMeter project. Heroku is a cloud platform that allows developers to build, run, and operate applications entirely in the cloud.

To deploy your own, follow these steps -

>1. Select __New__ in the top-right corner of your Heroku Dashboard, and select __Create new app__ from the dropdown menu.
>2. Your app name must be unique, and then choose a region closest to you (EU or USA), and finally, select __Create App__.
>3. From the new app __Settings__, click __Reveal Config Vars__, and set your environment variables.

| Key | Value |
| --- | --- |
| `DATABASE_URL` | user's own value |
| `IP` | 0.0.0.0 |
| `MONGO_DBNAME` | user's own value |
| `MONGO_URI` | user's own value |
| `PORT` | 5000 |
| `SECRET_KEY` | user's own value |

>4. Heroku needs two additional files in order to deploy properly.
- requirements.txt
- Procfile

>5. You can install this project's __requirements__ (where applicable) using:

- `pip3 install -r requirements.txt`

>6. If you have your own packages that have been installed, then the requirements file needs updated using:

- `pip3 freeze --local > requirements.txt`

>7. The **Procfile** can be created with the following command:

- `echo web: python app.py > Procfile`
- *replace __app.py__ with the name of your primary Flask app name; the one at the root-level*

NOTE: The Procfile uses a capital P and doesn't have a file extension on the end.

>8. For Heroku deployment, follow these steps to connect your own GitHub repository to the newly created app:

Either:

- Select __Automatic Deployment__ from the Heroku app.

>9. Or:

- In the Terminal/CLI, connect to Heroku using this command: `heroku login -i`
- Set the remote for Heroku: `heroku git:remote -a app_name` (replace *app_name* with your app name)
- After performing the standard Git `add`, `commit`, and `push` to GitHub, you can now type:
	- `git push heroku main`

The project should now be connected and deployed to Heroku!

## Gitpod.io Deployment

>1. Go to github.
>2. Find MovieMeter repository or [Click Here](https://github.com/leellismith/MovieMeter).
>3. Click on the green <> Code button.
>4. In the dropdown you will find the HTTP url. Copy that.
>5. Load up [Gitpod](https://gitpod.io/)
>6. Once logged in, Select Orange new workspace button.
>7. Click on select a respository.
>8. Paste in the repository. See steps 1 - 4.
>9. Click continue.
>10. Your workspace has been set up.
___
 __Making a Clone__

 >1. Follow steps 1 - 4 from the Gitpod.io deployment steps.
 >2. Open your Terminal.
 >3. Select a location where you would like the clone to save to.
 >4. Type __git clone__ and paste the respository.
 >5. Press Enter to create your local clone.

 # Credits

 API was used from [omdbapi.com](https://www.omdbapi.com/)

[Bootstrap](https://getbootstrap.com/) was used throughout my site.

Animated 3D background taken from [Vanta JS](https://www.vantajs.com/).

Followed through the [mini project](https://learn.codeinstitute.net/courses/course-v1:CodeInstitute+NRDB_L5+2/courseware/9e2f12f5584e48acb3c29e9b0d7cc4fe/054c3813e82e4195b5a4d8cd8a99ebaa/) to make sure I had the correct CRUD functionality.

### Acknowledgements

* Amy Richardson - Cohort Facilitator: For providing great resources to help with everyone's projects through weekly stand ups and even checking in if I missed a meeting.

* I would like to thank my family, for their support and understanding, for believing in me, and allowing me to make this transition into software development.

* A special thanks to my two friends who both work in software development, whose advice during this project was invaluable.