# **Assignment-1C sort most rated genre**

## <a name="1."></a>**1. Student details**

|        |                                                                                          |
|:-------|:-----------------------------------------------------------------------------------------|
|Naam:   |Jasper Stedema                                                                            |
|Nummer: |621642                                                                                    |
|Github: |<https://github.com/Jasper-Dev/Inholland-P3.4-Parallel-Distributed-Processing-Assignments>|

## <a name="2."></a>**2. Execution**

> :warning: **Warning:** In order to run the code in this assignment, first make sure your hadoop sandbox is properly set up!

The configuration and setup steps can be found in the The steps can be found in [main README.md file](<../Assignment-1#2-prerequisites>)

### <a name="2.1."></a>**2.1. Download the required datasets**

```bash
#download the movielens datasets from inholland, and place the datasets in the 
#‘data’ folder inside the assignment’s vitual environment
wget http://witan.nl/hadoop/u.data --no-check-certificate
wget http://witan.nl/hadoop/u.item --no-check-certificate
```

### <a name="2.2."></a>**2.2. Run the Python script**

```bash
#place the script inside the ‘scripts’ folder (I did this with WinSCP, but you are free to do it your own way) and run the python script
python3.8 scripts/Assignment1C_sort_most_rated_genre.py data/u.data data/u.item

# to output the results to a timestamped file, append the command with the following line:
[..command..] > `date +%Y.%m.%d-%H.%M.%S`-MRJob-output-Assigment-C.txt

#example:
python3.8 scripts/Assignment1C_sort_most_rated_genre.py data/u.data data/u.item > output/`date +%Y.%m.%d-%H.%M.%S`-MRJob-output-Assigment-C.txt
```

## <a name="3."></a>**3. Code & Explanation**

In this chapter, you can find the SQL query and the Python code used to answer assignment-1C aswell as the explanation for the Python code in the form of commands.

The results and screenshots of those results can be found in chapter [4. Results & Screenshots](#4.)

### <a name="3.1."></a>**3.1. Hive query**

In order to have an essence on how our data is going to look like,
it is key to first write the query in Hive. This will run faster and troubleshooting is easier,
as there is more documentation available on Hive.

```sql
SELECT 
    sum(mn.unknown) AS Unknown_count,
    sum(mn.action) AS Action_count,
    sum(mn.adventure) AS Adventure_count,
    sum(mn.animation) AS Animation_count,
    sum(mn.childrens) AS Childrens_count,
    sum(mn.comedy) AS Comedy_count,
    sum(mn.crime) AS Crime_count,
    sum(mn.documentary) AS Documentary_count,
    sum(mn.drama) AS Drama_count,
    sum(mn.fantasy) AS Fantasy_count,
    sum(mn.film_Noir) AS Film_Noir_count,
    sum(mn.horror) AS Horror_count,
    sum(mn.musical) AS Musical_count,
    sum(mn.mystery) AS Mystery_count,
    sum(mn.romance) AS Romance_count,
    sum(mn.sci_fi) AS Sci_Fi_count,
    sum(mn.thriller) AS Thriller_count,
    sum(mn.war) AS War_count,
    sum(mn.western) AS Western_count

FROM 
    movie_names mn
    RIGHT JOIN movie_ratings AS mr ON mn.movie_id = mr.movie_id

GROUP BY CASE 
    WHEN mn.unknown = 1 THEN 1 
    WHEN mn.action = 1 THEN 1
    WHEN mn.adventure = 1 THEN 1 
    WHEN mn.animation = 1 THEN 1 
    WHEN mn.childrens = 1 THEN 1 
    WHEN mn.comedy = 1 THEN 1 
    WHEN mn.crime = 1 THEN 1 
    WHEN mn.documentary = 1 THEN 1 
    WHEN mn.drama = 1 THEN 1 
    WHEN mn.fantasy = 1 THEN 1 
    WHEN mn.film_Noir = 1 THEN 1 
    WHEN mn.horror = 1 THEN 1 
    WHEN mn.musical = 1 THEN 1 
    WHEN mn.mystery = 1 THEN 1 
    WHEN mn.romance = 1 THEN 1 
    WHEN mn.sci_fi = 1 THEN 1 
    WHEN mn.thriller = 1 THEN 1 
    WHEN mn.war = 1 THEN 1 
    WHEN mn.western = 1 THEN 1
    ELSE 0 
    END;
```

### <a name="3.2."></a>**3.2. MRJobs & MRSteps**

Because the extra / C assignment is vastly different than the extra B assignment, i'm going to provide all detailed comments eventho it's possible I already described them in assignment A or B

```python
from mrjob.job import MRJob
from mrjob.step import MRStep

# Because the extra / C assignment is vastly different than the extra B assignment, i'm going to provide all detailed comments eventho it's possible I already described them in assignment A or B
class Assignment1C_sort_most_rated_genre(MRJob):
```

```python
    #set constants
    GENRE_TYPES = ["unknown", "action", "adventure", "animation", "children", "comedy", "crime", "documentary", "drama", "fantasy", "film_noir", "horror", "musical", "mystery", "romance", "scifi", "thriller", "war", "western"]
    IS_FORMATTED_OUTPUT = True
```

```python
    # define all the steps mrjobs need to take
    def steps(self):
        # instead of writing a script for each iteration, we can make use of steps.
        # with steps we specify all the steps mrjob needs to take and chain them together
        return [
            MRStep(
                mapper=self.mapper_get_datasets
            ),
            MRStep( 
                mapper=self.mapper_assign_each_genre_an_ID,
                reducer=self.reducer_join_ratings_and_genres_on_movieID
            ),
            MRStep(
                reducer=self.reducer_join_ratings_on_value
            ),
            MRStep(
                combiner=self.combiner_reduce_genres,
                reducer=self.reducer_reduce_genres
            ),
            MRStep(
                reducer=self.reducer_sort_most_rated_genres
            ),
        ]
```

```python
    ###
    # in order to know the amount of ratings per genre we need to join two datafiles u.data for the ratings and u.item for the movie details
    # a quick google how to join two datasets leads us to the following code: https://gist.github.com/rjurney/2f350b2cbed9862b692b
    # this code is essential as it shows how mrjobs loads in datafiles.

    # which in my eyes is completely at random, when doing a yield directly after loading them in, the lines of the datasets are unordered and randomly placed in the output.
    # for this we need a solution. 
    # First, we need to determine beforehand which delimiters that are being used in the datasets, and how many columns each dataset has.
    # this way we can recognize which lines are from which dataset, choose which columns we wanna use and give each line their corresponding name / category.

    # this mapper yields the following {key:value}-pairs
    # {movieID:["rating", rating_value]} 
    # "1000" ["rating", "3"]

    # {movieID:["metadata", genre_value1, genre_value2, genre_value3...]}
    # "1000" ["metadata", "0", "0", "0", "0", "0", "1", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "1"]
    ###
    def mapper_get_datasets(self, _, line):
        TAB_DELIMITER = "\t"
        PIPE_DELIMITER = "|"

        if len(split_by_tab := line.split(TAB_DELIMITER)) == 4:   
            (userID, movieID, rating, timestamp) = split_by_tab
            yield movieID, ("rating", rating)

        elif len(split_by_pipe := line.split(PIPE_DELIMITER)) == 24:
            (movieID, movie_title, _, _, _, unknown, action, adventure, animation, children, comedy, crime, documentary, drama, fantasy, film_noir, horror, musical, mystery, romance, scifi, thriller, war, western) = split_by_pipe
            yield movieID, ("metadata", unknown, action, adventure, animation, children, comedy, crime, documentary, drama, fantasy, film_noir, horror, musical, mystery, romance, scifi, thriller, war, western)
         
        else:
            yield 0, ("invalid input", line)
```

```python
    ###
    # In the next step we have another mapper, I choose to do another mapper to accomodate for the genres in the metadata 
    # and because it splits all the genres into seperate lines, which makes the total dataset larger instead of smaller.
    # This is necessary, as we eventually need to assign the ratings to each corresponding genre.
    
    # The splitting of the genres is done by a for loop, which iterates over a 'genres-only' subset from the metadata dataset.
    # while iterating it replaces all genre-values of 1, with the corresponding genreID and all the genre-values of 0 are irrelevant and being dropped

    # this mapper yields the following {key:value}-pairs
    # {movieID:["genre", genreID]} 
    # "1000" ["genre", 5]
    # "1000" ["genre", 18]

    # {movieID:["rating", rating_value]}
    # "1000" ["rating", "3"]
    ###
    def mapper_assign_each_genre_an_ID(self, movieID, values_list):
        if values_list[0] == "metadata":
            genreID = 0
            for is_genre in values_list[-19:]:
                if is_genre == "1":
                    yield movieID, ("genre", genreID)
                genreID += 1  

        else:
            yield movieID, values_list
```

```python
    ###
    # After two mappers, its time to reduce the amount of lines.
    # in this reducer we join the two datasets based on the movieID,
    # first we create two lists, which we then fill up with their corresponding values and eventually assign them all to the movieID

    # This reducer yields the following {key:value}-pairs
    # {movie_id:[["rating", [rating_value1, rating_value2, rating_value3...]], ["genre", [genreID1, genreID2, genreID3...]]]} 
    # "1000" [["rating", ["2", "3", "3", "3", "2", "3", "3", "4", "3", "4"]], ["genre", [5, 18]]]
    ###
    def reducer_join_ratings_and_genres_on_movieID(self, movieID, values_generator):
        rating_list = []
        genre_list = []
        for name, value in values_generator:
            if name == "rating":
                rating_list.append(value)
            elif name == "genre":
                genre_list.append(value)
            else:
                yield 0, ("invalid input", values_generator)
        
        yield movieID, (("rating", rating_list), ("genre", genre_list))
```

```python
    ###
    # In the second reducer we:
    # - reduce the rating_list to the itemcount or "length" of the list
    # - assign each genreID from the genre_list their newly reduced rating_count

    # so this "reducer" does not really reduce the amount of lines, 
    # but reduces the size of the dataset, by reducing the ratings_list.

    # This reducer yields the following {key:value}-pairs
    # {movie_id:[genreID, rating_count]} 
    # "1000" [5, 10]
    # "1000" [18, 10]
    ###
    def reducer_join_ratings_on_value(self, movieID, values_generator):
        for rating_generator, genre_generator in values_generator:
            rating_list = rating_generator[1]
            genre_list = genre_generator[1]

            for genreID in genre_list:
                yield movieID, (genreID, len(rating_list))
```

```python
    ###
    # In order to prepare the lines for the next reducer, we need to semi-reduce / combine the lines a bit.
    # Before sending it over the network to the next reducer

    # This combiner yields the following {key:value}-pairs
    # {genreID:rating_count} 
    # 5     10
    # 18    10
    ###
    def combiner_reduce_genres(self, _, values_generator):
        for genreID, rating_count in values_generator:
            yield genreID, rating_count
```

```python
    ###
    # After the combiner, the reducer can go ahead and reduce the list by
    # - further summing up all the rating_counts 
    # - and grouping them by genreID

    # This reducer yields the following {key:value}-pairs (pasting full list, as its only 19 lines)
    # {None:[genreID, rating_count]} 
    # null [5, 29832]
    # null [15, 12730]
    # null [16, 21872]
    # null [17, 9398]
    # null [18, 1854]
    # null [2, 13753]
    # null [3, 3605]
    # null [4, 7182]
    # null [0, 10]
    # null [1, 25589]
    # null [10, 1733]
    # null [11, 5317]
    # null [12, 4954]
    # null [13, 5245]
    # null [14, 19461]
    # null [6, 8055]
    # null [7, 758]
    # null [8, 39895]
    # null [9, 1352]
    ###
    def reducer_reduce_genres(self, genreID, rating_count):
        yield None, (genreID, sum(rating_count)) 
```

```python
    ###
    # At this point the list is thus far reduced that it only consists of the 19 genre_types (As we can see in the description of the previous reducer), 
    # only thing to do now is sorting the list, so the most rated genre is up top and the least rated is at the bottom.

    # This final sorter reducer yields the following formatted string,
    # if the formatted output is not desired it can be turned off by setting the IS_FORMATTED_OUTPUT constant to False
    # "Genre: drama       with ID:  8 is rated:" "39895 times."
    # "Genre: comedy      with ID:  5 is rated:" "29832 times."
    # "Genre: action      with ID:  1 is rated:" "25589 times."
    # "Genre: thriller    with ID: 16 is rated:" "21872 times."
    # "Genre: romance     with ID: 14 is rated:" "19461 times."
    # "Genre: adventure   with ID:  2 is rated:" "13753 times."
    # "Genre: scifi       with ID: 15 is rated:" "12730 times."
    # "Genre: war         with ID: 17 is rated:" " 9398 times."
    # "Genre: crime       with ID:  6 is rated:" " 8055 times."
    # "Genre: children    with ID:  4 is rated:" " 7182 times."
    # "Genre: horror      with ID: 11 is rated:" " 5317 times."
    # "Genre: mystery     with ID: 13 is rated:" " 5245 times."
    # "Genre: musical     with ID: 12 is rated:" " 4954 times."
    # "Genre: animation   with ID:  3 is rated:" " 3605 times."
    # "Genre: western     with ID: 18 is rated:" " 1854 times."
    # "Genre: film_noir   with ID: 10 is rated:" " 1733 times."
    # "Genre: fantasy     with ID:  9 is rated:" " 1352 times."
    # "Genre: documentary with ID:  7 is rated:" "  758 times."
    # "Genre: unknown     with ID:  0 is rated:" "   10 times."
    ###
    def reducer_sort_most_rated_genres(self, _, values_generator):
        # sort the list so the rating_counts are sorted in DESC order, this only works when the sortingkey is cast to an int, otherwise you're in for a whole bunch of shenanigans 😅
        sorted_list = sorted(values_generator, key=lambda row: int(row[1]), reverse=True)
        for genreID, rating_count in sorted_list:
            if self.IS_FORMATTED_OUTPUT:
                yield 'Genre: ' + self.GENRE_TYPES[genreID].ljust(11, ' ') + " with ID: "+ str(genreID).rjust(2, ' ') + " is rated:", str(rating_count).rjust(5, ' ') + ' times.'
            else:
               yield genreID, rating_count
```

```python
if __name__ == '__main__':
    Assignment1C_sort_most_rated_genre.run()
```

## <a name="4."></a>**4. Results & Screenshots**

- assignment C (Assignment1C_sort_most_rated_genre.py) is an extra assignment to score 2 extra points on the grade

### <a name="4.1."></a>**4.1 Results**

```Text
"Genre: drama       with ID:  8 is rated:" "39895 times."
"Genre: comedy      with ID:  5 is rated:" "29832 times."
"Genre: action      with ID:  1 is rated:" "25589 times."
"Genre: thriller    with ID: 16 is rated:" "21872 times."
"Genre: romance     with ID: 14 is rated:" "19461 times."
"Genre: adventure   with ID:  2 is rated:" "13753 times."
"Genre: scifi       with ID: 15 is rated:" "12730 times."
"Genre: war         with ID: 17 is rated:" " 9398 times."
"Genre: crime       with ID:  6 is rated:" " 8055 times."
"Genre: children    with ID:  4 is rated:" " 7182 times."
"Genre: horror      with ID: 11 is rated:" " 5317 times."
"Genre: mystery     with ID: 13 is rated:" " 5245 times."
"Genre: musical     with ID: 12 is rated:" " 4954 times."
"Genre: animation   with ID:  3 is rated:" " 3605 times."
"Genre: western     with ID: 18 is rated:" " 1854 times."
"Genre: film_noir   with ID: 10 is rated:" " 1733 times."
"Genre: fantasy     with ID:  9 is rated:" " 1352 times."
"Genre: documentary with ID:  7 is rated:" "  758 times."
"Genre: unknown     with ID:  0 is rated:" "   10 times."
```

### <a name="4.2."></a>**4.2 Screenshots**

_Assignment1C Hive SQL_

![Assignment1C Hive SQL](Screenshots/Assignment1C_HIVE.png "Assignment1C Hive SQL")

_Assignment1C MRJob CLI_

![Assignment1C MRJob CLI](Screenshots/Assignment1C_MRJOB_CLI.png "Assignment1C MRJob CLI")
