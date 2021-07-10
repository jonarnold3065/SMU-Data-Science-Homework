# First we'll import the os module
# This will allow us to create file paths across operating systems
import os
import numpy as np
# Module for reading CSV files
import csv

# FIGURE OUT THE FILEPATH ON YOUR COMPUTER
csvpath = "Instructions\\PyPoll\\Resources\\election_data.csv"

# read in the CSV data into memory - a list of lists
with open(csvpath) as csvfile:

    # CSV reader specifies delimiter and variable that holds contents
    csvreader = csv.reader(csvfile, delimiter=',')

    # Read the header row first (skip this step if there is now header)
    csv_header = next(csvreader)
    # print(f"CSV Header: {csv_header}")

#     # assign name to the list, the list includes all rows as the [] are inclusive of the data. 
    poll_data = []
    for row in csvreader:
         poll_data.append(row)

    print(len(poll_data))  
    # now that i have confirmed that the total count works, i will assign a variable to that function, a quick key so to speak 
    vote_count = (len(poll_data))   

    # i previously tried to create a dictionary with no succes, then tried a unique value count and blew up my laptop
    # i had to close out VScode and start over.   I went back to the drawing board and referenced class material
    
    # create an empty dictionary 
    all_votes = {} 
    # then try the loop, hopefully i wont break my laptop again....
    #so, for whatever variable in my list, specifically index 2 which is the 3rd column, 
    # add 1 to the count (line 41 and so on)
    for row in poll_data:
        candidate =row[2]

        if candidate in all_votes.keys():
            all_votes[candidate] += 1
        else: 
            all_votes[candidate] = 1

    print(all_votes)

    # max(all_votes, key = )

 # found an alternative but it included "import collections as ct" and i have no idea 
 # what that is so ill leave it alone for now but the code is below.   
# filepath = "test.txt"
# with open(filepath) as f:
#     votes = ct.Counter()
#     reader = csv.reader(f)
#     next(reader)
#     for line in reader:
#         candidate = line[-1]
#         votes[candidate] += 1

winner = ""
starting_votes = 0
for runners in all_votes.keys():
    votes_received = all_votes[runners]
    if votes_received > starting_votes:
        starting_votes = votes_received
        winner = runners


# print(poll_data)

# # grab length of data set
# total_months = len(poll_data)
# print(total_months)



# # write to TXT file
out_path = "pypoll Arnold.txt"
with open(out_path, "w") as f:
     f.write(f"Election Results\n")
     f.write(f"----------------------------\n")
     f.write(f"Total Votes: {vote_count}\n")
     f.write(f"----------------------------\n")

     for runners in all_votes.keys():
         f.write(f"{runners}: {round(all_votes[runners]/vote_count * 100, 3)}% ({all_votes[runners]})\n")

     f.write(f"-------------------------------\n")
     f.write(f"Winner: {winner}\n")
     f.write(f"--------------------------------\n")