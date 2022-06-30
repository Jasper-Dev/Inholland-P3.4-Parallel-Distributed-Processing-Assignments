# **Assignment-1B show and sort**

## <a name="1."></a>**1. Student details**

|        |                                                                                          |
|:-------|:-----------------------------------------------------------------------------------------|
|Naam:   |Jasper Stedema                                                                            |
|Nummer: |621642                                                                                    |
|Github: |<https://github.com/ditislol10/Inholland-P4.4-Parallel-Distributed-Processing-Assignments>|

## <a name="2."></a>**2. Execution**

> :warning: **Warning:** In order to run the code in this assignment, first make sure your hadoop sandbox is properly set up!

The configuration and setup steps can be found in the The steps can be found in [main README.md file](<../Assignment-1#2-prerequisites>)

### <a name="2.1."></a>**2.1. Download the required dataset**

```bash
#download the movielens dataset from inholland, and place the dataset in the 
#‘data’ folder inside the assignment’s vitual environment
wget http://witan.nl/hadoop/u.data --no-check-certificate
```

### <a name="2.2."></a>**2.2. Run the Python script**

```bash
#place the script inside the ‘scripts’ folder (I did this with WinSCP, but you are free to do it your own way) and run the python script
python3.8 scripts/Assignment1B_show_and_sort.py data/u.data

# to output the results to a timestamped file, append the command with the following line:
[..command..] > `date +%Y.%m.%d-%H.%M.%S`-MRJob-output-Assigment-B.txt

#example:
python3.8 scripts/Assignment1B_show_and_sort.py data/u.data > output/`date +%Y.%m.%d-%H.%M.%S`-MRJob-output-Assigment-B.txt
```

## <a name="3."></a>**3. Code & Explanation**

In this chapter, you can find the SQL query and the Python code used to answer assignment-1B aswell as the explanation for the Python code in the form of commands.

The results and screenshots of those results can be found in chapter [4. Results & Screenshots](#4.)

### <a name="3.1."></a>**3.1. Hive query**

In order to have an essence on how our data is going to look like,
it is key to first write the query in Hive. This will run faster and troubleshooting is easier,
as there is more documentation available on Hive.

```sql
SELECT movie_id, count(movie_id) as ratingCount
FROM movie_ratings
GROUP BY movie_id
ORDER BY ratingCount DESC;
```

### <a name="3.2."></a>**3.2. MRJobs & MRSteps**

Now we know how our data needs to look like, we can begin writing our Python code for the Assignment1B.
As this is the extra / B assignment in order to get an grade 8, i'm only going to provide detailed comments on the parts that are different from the base assigment A

```python
from mrjob.job import MRJob
from mrjob.step import MRStep

# as this is the extra / B assignment in order to get an grade 8, i'm only going to provide detailed comments on the parts that are different from the base assigment A
class Assignment1B_show_and_sort(MRJob):
```

```python
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
```

```python
    # NO CHANGES MADE: 
    #
    # EXPLANATION:
    # mapping the data from the file to a table-like usable format
    def mapper_get_movies(self, _, line):
        (userID, movieID, rating, timestamp) = line.split('\t')
        yield movieID, 1
```

```python
    # NO CHANGES MADE: 
    #
    # EXPLANATION:
    # combining the data before being send to reducer, yields key-value-pairs for the summed up assigned_values up of each reccuring movieID and passes it on to the reducer
    def combiner_count_ratings(self, movieID, assigned_value):
        yield movieID, sum(assigned_value)
```

```python
    # NO CHANGES MADE: 
    #
    # EXPLANATION:
    # this will do basically the same as the combiner but on a different level, yields key-value-pairs for the summed up assigned_values up of each reccuring movieID
    # and because we are going to sort on the rating and not the movieID, the key-value-pairs are swapped before passing it on
    def reducer_count_ratings(self, movieID, occurrence):
        # yield None, (sum(occurrence), movieID)
        yield None, (movieID, sum(occurrence))
```

```python
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
```

```python
if __name__ == '__main__':
    Assignment1B_show_and_sort.run()
```

## <a name="4."></a>**4. Results & Screenshots**

- assignment B (Assignment1B_show_and_sort.py) is an extra assignment to score 2 extra points on the grade

### <a name="4.1."></a>**4.1 Results**

```Text
"MovieID:   50" " 583 ratings."
"MovieID:  258" " 509 ratings."
"MovieID:  100" " 508 ratings."
"MovieID:  181" " 507 ratings."
"MovieID:  294" " 485 ratings."
"MovieID:  286" " 481 ratings."
"MovieID:  288" " 478 ratings."
"MovieID:    1" " 452 ratings."
"MovieID:  300" " 431 ratings."
"MovieID:  121" " 429 ratings."
"MovieID:  174" " 420 ratings."
"MovieID:  127" " 413 ratings."
"MovieID:   56" " 394 ratings."
"MovieID:    7" " 392 ratings."
"MovieID:   98" " 390 ratings."
"MovieID:  237" " 384 ratings."
"MovieID:  117" " 378 ratings."
"MovieID:  172" " 367 ratings."
"MovieID:  222" " 365 ratings."
```

### <a name="4.2."></a>**4.2 Screenshots**

_Assignment1B Hive SQL_

![Assignment1B Hive SQL](Screenshots/Assignment1B_HIVE.png "Assignment1B Hive SQL")

_Assignment1B MRJob CLI_

![Assignment1B MRJob CLI](Screenshots/Assignment1B_MRJOB_CLI.png "Assignment1B MRJob CLI")
