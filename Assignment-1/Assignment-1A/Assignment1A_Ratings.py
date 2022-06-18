from mrjob.job import MRJob
from mrjob.step import MRStep

class Assignment1_Ratings(MRJob):

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

    # mapping the data from the file to a table-like usable format
    def mapper_get_movies(self, _, line):
        # split the lines from the file into columns at the 'tab' character and assign a header to the columns 
        (userID, movieID, rating, timestamp) = line.split('\t')
        # yield the movieID's and assign each ID with a value of 1. 
        # This number will function like a "weight" which we can later use to count and evaluate the movieID's,
        # in this specific case, the "weight" is depending on the amount of ratings per row, which is 1.
        yield movieID, 1

    # combiner is a mini-reducer that runs on the mapper-node before the data is being send over the network,
    # this will prevent the large amounts of data causing heavy traffic load or congestion (more effecive in larger datasets)
    # it takes the yielded movieID and assigned_value from the mapper and sums the assigned_values up for each reccuring movieID
    # which creates a list of key-value-pairs and passes it on to the reducer
    def combiner_count_ratings(self, movieID, assigned_value):
        yield movieID, sum(assigned_value)

    # this will do basically the same as the combiner but on a different level
    # but unlike a combiner (which runs directly after the mapper on the same node before the data is being send over the network),
    # a reducer retrieves data from all the mapper nodes and performs the same actions as the combiner, so sum up all the assigned_values for the reccuring movieIDs within the list.
    # which creates a list of key-value-pairs and passes it on to the next step
    def reducer_count_ratings(self, movieID, occurrence):
        # this yielding line looks a bit different from the one in the combiner, as we need to send the key-value-pair list to the next step, rather than to the next part of a step.
        yield None, (movieID, sum(occurrence))


    # reduce and output the data
    # mrjob can only have one reducer per step, thats why we are using mrstep to create multi-step jobs
    def reducer_output_ratings(self, _, input_generator):
        # convert generator to list
        inputlist = list(input_generator)
        # sort the list so the movieIDs are sorted in ASC order, don't ask me why it needs to be this abomination, but it doesnt work otherwise.. 🤷‍♂️
        sortedinputlist = sorted(sorted(inputlist), key=lambda row: (-len(row[0])), reverse=True)
        
        # loop through all the sorted list items
        for movieID, ratingcount in sortedinputlist:
            # print the list of movieIDs with their rating count.
            # the ".rjust(4,' ')" is to space the numbers evenly, so its easier to read.
            yield 'MovieID: ' + str(movieID).rjust(4, ' '), str(ratingcount).rjust(4, ' ') + ' ratings.'

if __name__ == '__main__':
    Assignment1_Ratings.run()