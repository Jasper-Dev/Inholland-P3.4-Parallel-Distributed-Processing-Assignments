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
            MRStep(
                mapper=self.mapper_get_datasets #,          # step 1.1, map the data
                # reducer=self.reducer_count_ratings      # step 1.3, reduce the data
             ),
            MRStep( 
                mapper=self.generator_get_datasets
                # reducer=self.reducer_output_ratings     # step 2.1, reduce to show the workings of multi-step jobs
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
            # if len(split_by_tab) != 1 & len(split_by_pipe) != 1:
            yield 0, ("invalid input", line)



    def generator_get_datasets(self, movieID, values):

        # if values[0] == "metadata":

        # genre_types = ["unknown", "action", "adventure", "animation", "children", "comedy", "crime", "documentary", "drama", "fantasy", "film_noir", "horror", "musical", "mystery", "romance", "scifi", "thriller", "war", "western"]

        #     genres = split_by_pipe[-19:]
        #     genreID = 0
        #     for is_genre in genres:
        #         if is_genre == "1":
        #             yield movieID, ("genre", genre_types[genreID])
        #         genreID = genreID + 1  


            # yield movieID, ("metadata",
            # ("unknown", unknown),
            # ("action", action),
            # ("adventure", adventure),
            # ("animation", animation),
            # ("children", children),
            # ("comedy", comedy),
            # ("crime", crime),
            # ("documentary", documentary),
            # ("drama", drama),
            # ("fantasy", fantasy),
            # ("film_noir", film_noir),
            # ("horror", horror),
            # ("musical", musical),
            # ("mystery", mystery),
            # ("romance", romance),
            # ("scifi", scifi),
            # ("thriller", thriller),
            # ("war", war),
            # ("western", western))

        yield movieID, values[0]

if __name__ == '__main__':
    Assignment1C_sort_most_rated_genre.run()