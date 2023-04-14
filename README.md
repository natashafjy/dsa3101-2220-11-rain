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
  </ol>
</details>


<!-- ABOUT THE PROJECT -->
## About The Project :cloud_with_rain:

Amy is a fitness fanatic, who lives in the Queenstown area. Almost every evening, she tries to go for a run or a bike ride along Alexandra Canal Park. Her exercise routine is an intense 30 minutes each time, starting at 6pm every day. On days when it is raining, she skips her exercise. If she misses that window to train, she can't go later, because she must take a call with her US team at night. It's ok to miss a training session - that's ok to her, but it is 
-  frustrating that she is not given a good indication of the path of the storm.
-  even more frustrating to decide to skip based on a weather forecast, only for it to not rain a single drop.
- most frustrating to get stuck in the rain.

She usually starts at the River Valley Road junction, and is willing to go either direction, if only she knew which direction the rain was moving, and how heavy the rain was going to be (how wet the ground will be, not how many mm).

The challenge in this problem is to forecast rainfall at all locations (i.e given any latitude-longitude) in Singapore, up to 30 minutes in advance during these heavy rainfall events.


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

<p align="right">(<a href="#readme-top">back to top</a>)</p>


Template Credits: https://github.com/othneildrew/Best-README-Template


