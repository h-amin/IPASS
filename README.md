# IPASS
### Hamed Amin Student at the HU - Artificial Intelligence


## IPASS - Gardening Program Introduction

This project is made with the intent to help gardeners all over the world that have no prior experience nor time to spend figuring out what combination of plants to use for their garden to get the optimal result.
Gardening seems easier than it truly is, when taken at face value. Usually someone would argue that gardening and general plant knowledge is not anything to write home about. Experts however, will beg to differ.
Plants have alot of specific attributes and needs that will need to be recognized and cared for, otherwise you might just end up seeing your beautiful flowers or succulent fruit dying in matter of weeks, if not less.
This project is meant to help beginner gardeners get an idea of plant combinations, so that they may enjoy a vibrant garden without having to consort to experts and read 15 cm thick books just to get fluctuating results.

## Technicalities / Algorithm

With this project the algorithm will ask the user what plant they want to develop in their garden, after having ascertained which plant they will have to focus on, the program will look into a plant database
**(Disclaimer. The database used in this project is handmade and supposed to serve as a "mock" version of an actual database. Reason for this, is because I was unable to find a proper database without having to pay
money.)** and collect the PRIMARY keys which is the plant_names and put it into a list.

After the list has been created, the algorithm will compare the user input to the list of database plant_names and see wether or not the user input is actually a valid plant.
When the input has been accepted it will go through a main_characteristics function that will show us the designated attributes of said user input.
Once the attributes are extracted, the algorithm will proceed to give it a weighted value. This ranges from 1 to 40. The user input will always have a max weighted value of 150.
This means that the program will have to search through all records within the database and find other plant_names that have the lowest weighted delta in comparison to the user input.

All of the above will be handled with a function called recommendations, that essentially does this process for us, and locates all the attribute weight scores and saves it within a dictionary.
After receiving feedback from my mentor, I have decided to also add a secondary_recommendation, which in essence will do the same as the regular recommendation function, but this time around
it will use the highest weight score element within that dictionary so it can create secondary recommendations for said plant.

To put this into perspective, lets assume that plant_A returns a top_4 list with highest number of weighted values plants; [plant_B, plant_C, plant_D, plant_E].
This would mean that the secondary recommendation function will take plant_B and omit another algorithm on it, that is very similar to the recommendation function,
so that Plant_B will also have 3 recommendations. 

The reason behind the secondary recommendation code, is due to the lack of algorithm complexity that was prior to it. I had hoped that with this added, the possibility to grow the program
would be possible but just requires more finetuning and manual labor, however it seems to be a possibility regardless!

## Application

The application for this project is visualized by means of pygame. The code will show us a grid that will adjust its size based on the user input. The grid is meant to illustrate
our home gardens with the right width and length, so that the user can play around with the idea of localizing their primary plant.

The code will create an invisible array covered by white cubes that will light up in a green color, provided the user clicked on the designated location. The green color is an indicator for the primary plant.
What is also noteworthy, is that the code will also visualize cubes surrounding the primary green cube with different colors to indicate the recommendations based on the algorithm mentioned afore.
Along the same principle we get another color that will show us the secondary recommendation that will embody the recommended plants for the initial recommendations.

The grid has been structured in a way that will not allow excess cubes be transfered if the horziontal or vertical limit has been reached.



