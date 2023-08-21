import pandas as pd
import csv


# Method for string manipulation to adjust number of tabs based on length of last name

def myStringManipulation(myList1, myList2, myList3, myList4, i, f):
    # get the length of guests last name
    if len(myList1[i]) > 7:
        f.write(f'\t{myList1[i]}\t{myList2[i]}\t{myList3[i]}\t{myList4[i]}\n')

    else:
        f.write(f'\t{myList1[i]}\t\t{myList2[i]}\t{myList3[i]}\t{myList4[i]}\n')


# Method to separate first and last names            
def myNames(myList, myInt):
    """Function to get split first and last names."""
    rets = []   # return
    for i in range(len(myList)):    # Iterate throught list
        ret = myList[i].split()[myInt].replace(',','').title()  # split first/last name, remove commas, format text
        rets.append(ret)    # add either first or last name to a list
    return rets # return the list

# Method to write data to file
def myRooms(myList1, myList2, myList3, myList4, f):
    """Method to write data to text file."""
    num = len(myList1)
    f.write(f'\t\tNumber of Arrivals: {num}\n\n')
    f.write(f'\tGuest\t\tResID\tRoom\tDate Out\n\n')
    for i in range(len(myList1)):
            
            # if i > 0 and i % 5 == 0: // This code is to designate dividing rooms up into blocks of 5
            # // Not using it becuase I want to seperate by date
            
            # Puts a blank line between groups of dates
        if myList4[i] > myList4[i-1]:
            f.write('\n')
            myStringManipulation(myList1, myList2, myList3, myList4, i, f)
        else:
            myStringManipulation(myList1, myList2, myList3, myList4, i, f)
                
def pandaMagic():
    # Setting the data frame from the csv file 
    df = pd.read_csv('data/arrivals.csv')

    # Variable set for how many rows to remove from beginning of file
    n = 5

    # Remove first 5 lines of file
    df2 = df.iloc[n:]

    # Remove every other line, useless data
    df2.iloc[::2]

    # List of unnecessary columns
    headers = ['Unnamed: 0', 'Unnamed: 2', 'Unnamed: 4', 'Unnamed: 5', 'Unnamed: 6', 'Unnamed: 8', 'Unnamed: 9',  
        'Unnamed: 13', 'Unnamed: 14', 'Unnamed: 15', 'Unnamed: 16', 'Unnamed: 17', 'Unnamed: 18', 'Alexandra Inn']

    # Remove unnecessary columns
    for i in headers:
        df2.pop(i)

    # Sort by Arrival Date
    df2.sort_values(by='Unnamed: 7', inplace = True)

    # Insert a row at the top with new header names for when we read it in again as a new file
    new_row = pd.DataFrame({'Unnamed: 1':'Guest', 'Unnamed: 3': 'Res. ID', 'Unnamed: 7':'Date Out','Unnamed: 10': 'Rate', 'Unnamed: 12': 'Room'}, index=[0])
    df3 = pd.concat([new_row,df2.loc[:]]).reset_index(drop=True)

    # Create CSV data file for us to work with for the final product
    df3.to_csv('data/myData.csv', index=False, header=False)


# Open the data file and send the information to lists for writing to a text file
def myData(myFile): 
#'data/myData.csv'
    with open(myFile) as f: # Open CSV file
            reader = csv.reader(f)  # Read CSV File
            names, resIDs, dateOuts, rooms = [], [], [], []  # retrieve nights, rooms, names

            for row in reader:
                try:
                    if "WUERFEL" in row[0]:
                        pass
                    else:
                        name = row[0]
                        resId = int(row[1])
                        dateOut = row[2]
                        if int(row[3]) < 5:
                            room = int(row[4])
                        else:
                            room = int(row[3])
                        names.append(name)
                        resIDs.append(resId)
                        dateOuts.append(dateOut)
                        rooms.append(room)
                except ValueError:
                    pass
    lastNames = myNames(names, 0)
    return lastNames, resIDs, dateOuts, rooms

def createFile(myList1, myList2, myList3, myList4):
    # Creating a text file and writing data to the file
    with open('data/arrivals.txt', 'w') as f:
        myRooms(myList1, myList2, myList3, myList4, f)
        

def main():
    pandaMagic()
    myDataFile = 'data/myData.csv'
    lastNames, resIDs, dateOuts, rooms = myData(myDataFile)
    createFile(lastNames, resIDs, rooms, dateOuts)


main()
#EOF
