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
                    #  combiner=self.combiner_join_ratings_on_genreID#,
                    # combiner=self.combiner_ratings_on_value,
                    # reducer=self.reducer_ratings_on_value
                    reducer=self.reducer_join_ratings_on_value
                    # reducer=self.reducer_join_ratings_with_genres_on_movieID
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
                genreID += 1  

        else:
            yield movieID, values_list


    # def combiner_join_ratings_on_genreID(self, movieID, values_generator):
    def reducer_join_ratings_on_value(self, movieID, values_generator):
        rating_list = []
        genre_list = []
        for name, value in values_generator:
            if name == "rating":
                rating_list.append(value)
            elif name == "genre":
                genre_list.append(str(value))
            else:
                yield 0, ("invalid input", values_generator)
        yield movieID, ("genre", genre_list)
        #yield movieID, (("rating", rating_list), ("genre", genre_list))

    # def reducer_join_ratings_on_value(self, movieID, values_generator):

    #     for rating_generator, genre_generator in values_generator:
    #         yield movieID, (rating_generator, genre_generator)
    #         # for name, genre in genre_generator:
    #         #     yield genre, rating_generator[1]
    #             #for name, rating in rating_generator:

            
    #        #


    # def reducer_ratings_on_value(self, movieID, values_generator):
    #     rating_list = []
    #     for name, value in values_generator:
    #         if name == "rating":
    #             rating_list = value

    #         if name == "genre":
    #             yield value, rating_list

        #yield movieID, ("rating", rating_list)



        # movie_dictionary = {}
        # #rating_list.append("rating_list")

        # for name, value in values_generator:
        #     rating_list = []
        #     genre_list = []
        #     # first lookup if movieID exists, if not create key:value pair with <movieID:List[]>
        #     if movieID not in movie_dictionary.keys():
        #         rating_dictionary.append({:[]})
        #         genre_dictionary.append({"genre":[]})

        #         movie_dictionary.update({movieID:{}})

        #     movie_dictionary[movieID][name].append(value)

        #    # if name == "rating":
        #          # add the movierating to the corresponding movie
        #         # curr_dict["rating"].append(value)
        #     #if name == "genre":
        #         # add the genres to the corresponding movie
        #         # curr_dict["genre"].append(value)






                




        #         # first lookup if movie_rating exists, if not create key:value pair with <movie_rating:List[]>
        #         # if movie_rating not in rating_dictionary.keys():
        #         #     rating_dictionary.update({movie_rating:[]})
                    
        #         # # add the movierating to the corresponding ratingdictionary
        #         # rating_dictionary[movie_rating].append(movie_rating)
                    

        #         # then lookup if the ratings
        #         # if rating_dictionary[movieID].count(movieID) == 0:
        #         #     rating_dictionary[value] = []
        #         # else:
        #         #     rating_list
        #     # yield name+"-"+str(value), (movieID, value)
        #         # yield None, (name, sum(movieID, value))
        #         # movie_rating = values_list
        #         # if movie_rating == "1":
        # yield movieID, (rating_dictionary)

                # rating_count_list.append(movie_rating)
                # yield movieID, rating_count_list

            # elif values_list[0] == "genre":
            #     ratingamount = len(rating_count_list)
            #     genreID = values_list[1]                
                
            #     yield movieID, (("genre", genreID), ("ratings", rating_count_list))
            # else:
                # yield movieID, (name, genreID)
                # yield 0, ("holup", values_list)


    # def reducer_join_ratings_with_genres_on_movieID(self, movieID, values_generator):
    #     rating_count_list = []
    #     # convert generator to list
    #     for values_list in values_generator:
    #         if values_list[0] == "rating":
    #             movie_rating = values_list[1]
    #             rating_count_list.append(movie_rating)
    #             yield movieID, rating_count_list

    #         # elif values_list[0] == "genre":
    #         #     ratingamount = len(rating_count_list)
    #         #     genreID = values_list[1]                
                
    #         #     yield movieID, (("genre", genreID), ("ratings", rating_count_list))
    #         else:
    #             yield 0, ("holup", values_list)



if __name__ == '__main__':
    Assignment1C_sort_most_rated_genre.run()