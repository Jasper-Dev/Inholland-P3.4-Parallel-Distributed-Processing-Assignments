from mrjob.job import MRJob
from mrjob.step import MRStep

# because the extra / C assignment is vastly different than the extra B assingment, i'm going to provide detailed comments eventho i've already described them in assignment A or B
class Assignment1C_sort_most_rated_genre(MRJob):

    #set constants
    SORT_VALUES = True
    GENRE_TYPES = ["unknown", "action", "adventure", "animation", "children", "comedy", "crime", "documentary", "drama", "fantasy", "film_noir", "horror", "musical", "mystery", "romance", "scifi", "thriller", "war", "western"]
 


    # initiate mrjobs steps
    def steps(self):
        # instead of writing a script for each iteration, we can make use of steps.
        # with steps we specify all the steps mrjob needs to take and chain them together
        return [
            MRStep(
                mapper=self.mapper_get_datasets
            ),
            MRStep( 
                mapper=self.mapper_assign_each_genre_an_ID,
                reducer=self.reducer_join_ratings_on_genreID
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

    def mapper_assign_each_genre_an_ID(self, movieID, values_list):
        if values_list[0] == "metadata":
            genreID = 0
            for is_genre in values_list[-19:]:
                if is_genre == "1":
                    yield movieID, ("genre", genreID)
                genreID += 1  

        else:
            yield movieID, values_list

    def reducer_join_ratings_on_genreID(self, movieID, values_generator):
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

    def reducer_join_ratings_on_value(self, movieID, values_generator):
        for rating_generator, genre_generator in values_generator:
            rating_list = rating_generator[1]
            genre_list = genre_generator[1]

            for genreID in genre_list:
                yield movieID, (genreID, len(rating_list))
                

    def combiner_reduce_genres(self, _, values_generator):
        for genreID, rating_count in values_generator:
            yield genreID, rating_count

    def reducer_reduce_genres(self, genreID, rating_count):
        yield None, (genreID, sum(rating_count)) 

    def reducer_sort_most_rated_genres(self, _, values_generator):
        #for genreID, rating_count in values_generator:
        sorted_list = sorted(values_generator, key=lambda row: int(row[1]), reverse=True)



            # sort the list so the movieIDs are sorted in ASC order, this only works when the ID is cast to int, otherwise you're in for a whole bunch of shenanigans 😅
        for genreID, rating_count in sorted_list:
            yield 'Genre: ' + self.GENRE_TYPES[genreID] + " ID: "+ str(genreID).rjust(2, ' '), str(rating_count).rjust(5, ' ') + ' ratings.'




if __name__ == '__main__':
    Assignment1C_sort_most_rated_genre.run()