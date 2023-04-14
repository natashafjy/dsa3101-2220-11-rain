<a name="readme-top"></a>

# dsa3101-2220-11-rain  :umbrella:



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li>
       <a href="#user-manual">User Manual</a>
    </li>
  </ol>
</details>


<!-- ABOUT THE PROJECT -->
## About The Project :cloud_with_rain:

DryRun is a web application created using Dash, Flask, and mySQL database. 
It is provides **accurate** rainfall predictions at **any location** in Singapore **up to 30 minutes in advance** for outdoor runners with fixed running routines. The application is able to store the running routines and give suggestions on whether to continue the run based on the predicted amount of rainfall and the corresponding wetness level of the ground.


Hope you will enjoy our app and have a Dry Run!

<p align="right">(<a href="#readme-top">back to top</a>)</p>




<!-- GETTING STARTED -->
## Getting Started :droplet:

To get a local copy up and running follow these simple steps.

### Prerequisites

* Docker

### Installation

1. Clone the repository
   ```sh
   git clone https://github.com/natashafjy/dsa3101-2220-11-rain.git
   ```
2. Install the required modules
   ```sh
   pip3 install -r requirements.txt
   ```
3. Navigate to the following directory
   ```sh
   cd frontend
   ```
4. Deploy to a Docker container
   ```
   docker compose up -d
   ```

### User Manual :page_facing_up:
<details>
<summary>Click me for a detailed guide with images</summary>
  
  
1. Sign up

    <img width="1512" alt="Screenshot 2023-04-14 at 10 48 20 PM" src="https://user-images.githubusercontent.com/77218431/232077649-3112d096-07b4-413f-9517-e6b2e7306818.png">

    If you are a new user, click the sign up button and create your username and password.

2. Log in

    <img width="1512" alt="Screenshot 2023-04-14 at 10 53 40 PM" src="https://user-images.githubusercontent.com/77218431/232078929-19865066-8846-472b-a062-cd0cae252a8b.png">
    If log in is successful, you can click the "Click me to go!" button to proceed to the gallery page.
    
3. Gallery

    <img width="1512" alt="Screenshot 2023-04-14 at 10 54 38 PM" src="https://user-images.githubusercontent.com/77218431/232079171-b1844f23-18ae-42dc-a019-7c78559197a8.png">
    When first logged in, the dropdown would have no routines to choose from. You may click `add new routine` button to proceed.

4. Add routine

    <img width="1512" alt="Screenshot 2023-04-14 at 10 56 08 PM" src="https://user-images.githubusercontent.com/77218431/232079565-6ec018cd-5c05-4ec3-964b-041ffa970995.png">
    To add a routine, you need to input the required information as shown above. The location input is linked with Google Maps API so you may search with both postal code and name of address.
  
5. Back to gallery

    <img width="1512" alt="Screenshot 2023-04-14 at 10 58 16 PM" src="https://user-images.githubusercontent.com/77218431/232080078-0e53466a-498b-4e79-ab39-609d18a7f797.png">

    Now, select the routine you wish to predict for and then click the "go to current prediction page" button. 

6. Results
    <img width="1512" alt="Screenshot 2023-04-14 at 10 59 40 PM" src="https://user-images.githubusercontent.com/77218431/232080400-87d1d98b-0f2b-44f0-8cff-195e268a2a47.png">
    * Now comes the most important results page. You may need to wait for up to 20 seconds to fetch the results, and the browser tab would display "Updating.." until the result is retrieved successfully. 
    * As the prediction is accurate to every ooint, you may click select "start point" or "end point" to view the predictions for each point. The plots in the sidebar are showing the precipitation and wetness level across the next 30 minutes window, with weather icons updating accordingly. The overall suggestion for this route is also given. 
    * There are 2 tabs in the map, the first one displaying the route of choice, while the second one is a dynamic rainfall map. You may click the start button at the bottom to view the animation. 
    <img width="1512" alt="Screenshot 2023-04-14 at 11 04 13 PM" src="https://user-images.githubusercontent.com/77218431/232081357-de247f0e-8e0a-404a-80a0-82af7a64fac9.png">

  
  
  With that, we hope that you will enjoy our application! We are also happy to hear any feedback so feel free to reach out to us if you have any!

<p align="right">(<a href="#readme-top">back to top</a>)</p>


Template Credits: https://github.com/othneildrew/Best-README-Template


