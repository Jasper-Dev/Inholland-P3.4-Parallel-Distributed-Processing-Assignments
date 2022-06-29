from mrjob.job import MRJob
from mrjob.step import MRStep


# as this is the extra / B assignment in order to get an grade 8, i'm only going to provide detailed comments on the parts that are different from the base assigment A
class Assignment1B_show_and_sort(MRJob):

    # NO CHANGES MADE:
    # initiate mrjobs steps
    def steps(self):
        # instead of writing a script for each iteration, we can make use of steps.
        # with steps we specify all the steps mrjob needs to take and chain them together
        return [
            MRStep(
                mapper=self.mapper_get_movies,          # step 1.1, map the data
                combiner=self.combiner_count_ratings,   # step 1.2, combine/ mini-reduce the data
                reducer=self.reducer_count_ratings      # step 1.3, reduce the data
            ),
            MRStep( 
                reducer=self.reducer_output_ratings     # step 2.1, reduce to show the workings of multi-step jobs
            ) 
        ]

    # NO CHANGES MADE: 
    #
    # EXPLANATION:
    # mapping the data from the file to a table-like usable format
    def mapper_get_movies(self, _, line):
        (userID, movieID, rating, timestamp) = line.split('\t')
        yield movieID, 1

    # NO CHANGES MADE: 
    #
    # EXPLANATION:
    # combining the data before being send to reducer, yields key-value-pairs for the summed up assigned_values up of each reccuring movieID and passes it on to the reducer
    def combiner_count_ratings(self, movieID, assigned_value):
        yield movieID, sum(assigned_value)

    # NO CHANGES MADE: 
    #
    # EXPLANATION:
    # this will do basically the same as the combiner but on a different level, yields key-value-pairs for the summed up assigned_values up of each reccuring movieID
    # and because we are going to sort on the rating and not the movieID, the key-value-pairs are swapped before passing it on
    def reducer_count_ratings(self, movieID, occurrence):
        # yield None, (sum(occurrence), movieID)
        yield None, (movieID, sum(occurrence))

    # CHANGES: 
    # - changed the identifier to 1 in the sorted function to swap the assigned_values and movieID as key-value-pair, as the list needs to be sorted based on ratingcount
    # - ordered DESC to have MOST (not highest) rated movie up top 
    # - ratingcount is already integer, so removed the casting
    #  
    # EXPLANATION:
    # reduce and output the data
    # mrjob can only have one reducer per step, thats why we are using mrstep to create multi-step jobs
    def reducer_output_ratings(self, _, input_generator):
        # convert generator to list
        inputlist = list(input_generator)
        # sort the list so the ratingcounts are sorted in DESC order, so most rated movie is up top
        sortedinputlist = sorted(inputlist, key=lambda row: row[1], reverse=True)
        
        # loop through all the sorted list items
        for movieID, ratingcount in sortedinputlist:
            # print the list of movieIDs with their rating count.
            # the ".rjust(4,' ')" is to space the numbers evenly, so its easier to read.
            yield 'MovieID: ' + str(movieID).rjust(4, ' '), str(ratingcount).rjust(4, ' ') + ' ratings.'


if __name__ == '__main__':
    Assignment1B_show_and_sort.run()