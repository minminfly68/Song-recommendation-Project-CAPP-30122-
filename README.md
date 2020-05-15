# Feeling Sentimental
Using Spotify Top 50 Songs data from 2010 to 2019, we created an application to recommend the best song to user based on his/her mood and preferences. <br>
We first scraped the lyrics based on top songs database, then we conducted the sentimental analysis based on the lyrics, finally we find the best variables to match one's mood and emotions. <br>
We used Django do display our results and returned the users with a random song in the database matching his/her selection.

## Prerequisites and installing
1.	create and activate environment
2.	run $pip install -r requirements.txt
3.	run the program

## Data Source
-	Spotify 10-year Top 50 Songs data downloaded from Kaggle, https://www.kaggle.com/leonardopena/top-spotify-songs-from-20102019-by-year
-	Lyrics scraped from genius by using crawler.py, https://genius.com

## Running the program

To run the whole program and song recommendation UI ? <br>
$ python manage.py migrate <br>
$ python manage.py runserver <br>

To run crawler.py, run the following command inside the terminal: <br>
$ python crawler.py <br>
Note: crawler.py takes a relatively long time to run. <br>

To run sentiment.py, run the following command inside the terminal: <br>
$ python sentiment.py <br>
Note: sentiment.py takes a relative long time to run. <br>

## Built With
* [Django] https://docs.djangoproject.com/en/3.0/ - The python-based web framework <br>
* [nltk4] https://www.nltk.org/ NTLK is a leading platform for building Python programs to work with human language data.

## Authors
Chun Hu (chunhu), YIMIN LI(liym15), Tianyue Niu (tniu)

## License
This project is licensed under the MIT License.

## Acknowledgments
* This project is designed for CAPP30122 final project. <br>
* We are grateful to CAPP 30122 teaching teams and anyone who helped us along the project.

