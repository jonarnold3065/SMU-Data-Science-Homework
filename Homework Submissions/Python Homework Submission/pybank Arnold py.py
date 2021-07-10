# Import systems and programs 
import os
import numpy as np
# Module for reading CSV files  (i just want to use pandas.....)
import csv

# pull file from folder in my computer and name the doc, in this case i chose pybankdoc (the csvreader stuff is confusing) 
pybankdoc = "Instructions\\PyBank\\Resources\\budget_data.csv"

# convert doc into a list, and name it.  in this one i named it bankfile (again the CSV stuff can get confusing)
with open(pybankdoc) as bankfile:

    # take the list and split the data by their commas, aka seperate the data into seperate columns? 
    # take the "bankfile" and use the csv.reader to split the values by using a delimiter
     csvreader = csv.reader(bankfile, delimiter=',')

    # run the csv_header to confirm that it is reading the data properly and can produce the correct header values. beyond that, not sure what this is for
     csv_header = next(csvreader)
    # print(f"CSV Header: {csv_header}")  # returned ['Date', 'Profit/Losses']
     
     # make list with all the info, orig_list = original list, this way i can easily understand that it is the ORIGINAL DATA SET!! 
     # "all rows" makes it seem like that is a function command or something 
     # clean rows and cast the second column to an integer, temp_row is created so that we dont lose the original data
     orig_list = []
     for row in csvreader:  
          orig_list.append(row)     
          temp_row = row  
          temp_row [1] = int(temp_row[1])
     total_months = len(orig_list) 
     # this code adds the temp row to the original list
     #print(temp_row)
     #csv_header = orig_list.pop(0)  ****inlcuding this cause my result to be missing the first entry. 
     # print(temp_row) brought back the month and profit/losses for the last entry.  unlcear how this works, will ask teach.
     print(len(orig_list)) 
     
     # profits = [x[1] for x in int(temp_row[1])]
     # profits = sum(temp_row)
     # total_profit = sum(profits)
     
     # after an hour of research i finally figured this out.  ####
     all_profits = [x[1] for x in orig_list]
     total_profit = sum(all_profits)
     print(total_profit)

               #### failed attempts below #######

     #      # profits = [x[1] for x in int(temp_row[1])]
     #      profits = sum(temp_row)
     #      # total_profit = sum(profits)
     # # sum_profit = [x[1] for x in orig_list]
     # # total_profit = sum(sum_profit)
     #      print(profits)

          # changes = []  **** this creates a new list so that the original data is in tact?  or just a new list to simply
          #  work off of for i in range and the following lines, for "i" (any variable) in length (86) of the file (orig_list)
          #  minus 1 as we dont have a change in the first row 
     changes = []
     for i in range(len(orig_list) - 1):
          curr_profit = orig_list[i][1]
          next_profit = orig_list[i + 1][1]

        ##  print(np.average(changes))  so this didnt work.  :-) 

     #defining change and changes
          change = next_profit - curr_profit
          changes.append(change)

     # adding the changes over each cell/ then divding by the count of changes i.e. the len of changes 
     # below are two different methods.  
     average_change = sum(changes)/len(changes)
     # print(average_change)
     average_change2 = np.mean(changes)
     #print(average_change2)
          # none of the above lines seemed to work .... until i fixed my indentation on the above "change and Changes"

          #new variables, the maximum change based on the lists created previously. line 65 and 66 
     max_change = max(changes)
     min_change = min(changes)

     # # get change indexes
     max_change_indx = changes.index(max_change) + 1
     max_change_indx2 = np.argmax(changes) + 1
     max_month = orig_list[max_change_indx][0]

     min_change_indx = changes.index(min_change) + 1
     min_change_indx2 = np.argmin(changes) + 1
     min_month = orig_list[min_change_indx][0]

     print(average_change2)

     # # write to TXT file
     out_path = "pybank_Arnold.txt"
     with open(out_path, "w") as f:
               f.write(f"Financial Analysis\n")
               f.write(f"----------------------------\n")
               f.write(f"Total Months: {total_months}\n")
               f.write(f"Total: ${total_profit}\n")
               f.write(f"Average Change: ${round(average_change, 2)}\n")
               f.write(f"Greatest Increase in Profits: {max_month} (${max_change})\n")
               f.write(f"Greatest Decrease in Profits: {min_month} (${min_change})")