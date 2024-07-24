<h1 align="center">MovieMeter</h1>

<h2 align="center"> A Movie Review Site</h2>

<h2 align="center">Milestone Project 3 - Lee Smith</h2>

![Am I Responsive Image](readme-docs/wireframes/MM%20-%20amiresponsive.PNG)


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

## Future Features

* Like and dislike feature.
* Randomizer film picker.
* A page when users just search by category.
* A option for users, to click and go to a website to buy the movie if not seen.
* An option for users to select reviews for selected films.

# Typography and Color Scheme

# Wireframes

## Mobile Wireframe

![Mobile Wireframe]()

## Tablet Wireframe

![Mobile Wireframe]()

## Desktop Wireframe

![Mobile Wireframe]()

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

![Site Validation](readme-docs/wireframes/MM%20-%20HTML%20Validator.PNG)

#### __CSS Validation__

![CSS Validation](readme-docs/wireframes/MM%20-%20CSS%20Validator.PNG)

## __Lighthouse Testing__

#### __Home Page__

![Home Page Validation](readme-docs/wireframes/MM%20-%20Home%20Page%20-%20Lighthouse.PNG)

#### __Reviews Page__

![Reviews Validation](readme-docs/wireframes/MM%20-%20Reviews%20-%20Lighthouse.PNG)

#### __Login Page__

![Login Validation](readme-docs/wireframes/MM%20-%20Login%20Page%20-%20Lighthouse.PNG)

#### __Sign Up Page__

![Sign Up Validation](readme-docs/wireframes/MM%20-%20Register%20Page%20-%20Lighthouse.PNG)

#### __Add Review Page__

![Add Review Validation](readme-docs/wireframes/MM%20-%20Add%20Review%20-%20Lighthouse.PNG)

#### __Manage Reviews Page__

![Manage Reviews Validation](readme-docs/wireframes/MM%20-%20Manage%20Reviews%20-%20Lighthouse.PNG)

#### __Profile Page__

![Profile Validation](readme-docs/wireframes/MM%20-%20Profile%20-%20Lighthouse.PNG)

## __Jshint Testing__

![Javascript Site Validation](readme-docs/wireframes/MM%20-%20Jshint.PNG)

## __CI Python Linter Testing__

![CI Python Linter Validation](readme-docs/wireframes/MM%20-%20CI%20Python%20Linter.PNG)

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
| First User | Found issue where they where able to make a review from the main page if they clicked of the carousel | Fixed by removing the function to click on the corousel and added a button which only shows for logged in users. |
| Second User | No Issues Found | N/A |
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

