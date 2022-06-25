from mrjob.job import MRJob
from mrjob.step import MRStep

# because the extra / C assignment is vastly different than the extra B assingment, i'm going to provide detailed comments eventho i've already described them in assignment A or B
class Assignment1C_sort_most_rated_genre(MRJob):

    #set constants
    SORT_VALUES = True
    


    # initiate mrjobs steps
    def steps(self):
        # instead of writing a script for each iteration, we can make use of steps.
        # with steps we specify all the steps mrjob needs to take and chain them together
        return [
            MRStep( mapper=self.mapper_get_datasets),
            MRStep( mapper=self.generator_seperate_genres,
                    reducer=self.reducer_join_ratings_with_genres_on_movieID
            ) 
        ]

    # in order to know the amount of ratings per genre we need to join 2 datafiles u.data for the ratings and u.item for the movie details
    # a quick google how to join 2 data sets leads us to the following code: https://gist.github.com/rjurney/2f350b2cbed9862b692b
    # here they first load in the data and then they assign each dataset to their own list with an id as key,
    # this same principle is what we are going to do here aswell, so we eventually get:
    # movie_id [[movie_title,genre1,genre2...],[sum_of_ratings]]
    def mapper_get_datasets(self, _, line):
        TAB_DELIMITER = "\t"
        PIPE_DELIMITER = "|"

        # first determine the seperator character

        if len(split_by_tab := line.split(TAB_DELIMITER)) == 4:   
            (userID, movieID, rating, timestamp) = split_by_tab
            yield movieID, ("rating", rating)

        elif len(split_by_pipe := line.split(PIPE_DELIMITER)) == 24:
            (movieID, movie_title, _, _, _, unknown, action, adventure, animation, children, comedy, crime, documentary, drama, fantasy, film_noir, horror, musical, mystery, romance, scifi, thriller, war, western) = split_by_pipe
            yield movieID, ("metadata", unknown, action, adventure, animation, children, comedy, crime, documentary, drama, fantasy, film_noir, horror, musical, mystery, romance, scifi, thriller, war, western)

        else:
            yield 0, ("invalid input", line)



    def generator_seperate_genres(self, movieID, values_list):

        if values_list[0] == "metadata":
            genreID = 0
            for is_genre in values_list[-19:]:
                if is_genre == "1":
                    yield movieID, ("genre", genreID)
                genreID = genreID + 1  

        else:
            yield movieID, values_list


    def reducer_join_ratings_with_genres_on_movieID(self, movieID, values_generator):
        # convert generator to list
        # values_list = list(values_generator)
        for values_list in values_generator:
            rating_count_list = []  
            if values_list[0] == "rating":
                movie_rating = values_list[1]
                rating_count_list.append(movie_rating)
                yield movieID, values_list

            elif values_list[0] == "genre":
                ratingamount = len(rating_count_list)
                genreID = values_list[1]                
                yield movieID, values_list
                # yield movieID, (("genre", genreID), ("ratings", rating_count_list))
            else:
                yield 0, ("holup", values_list)



if __name__ == '__main__':
    Assignment1C_sort_most_rated_genre.run()