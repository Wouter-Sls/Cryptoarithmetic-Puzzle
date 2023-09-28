from simpleai.search import CspProblem, backtrack
import streamlit as st

########################################################################## USER INPUT #######################################
isFilledIn=False
word1='' 
word2=''
word3=''

st.title("Cryptoarithmetic Puzzle") #Show the title of the app on Streamlit
st.subheader(':blue[_Created by Wouter Selis_] :male-technologist:', divider='rainbow') #Show a subheader on Streamlit with text in blue, an emoji and a rainbow line under the text

#This function checks if the given word only contains letters. Else it prints an error message and empty the variable so you must re-enter a word.
def only_letters(word):
    if not word.isalpha():
      if word == word1:
          word1=''
      elif word==word2:
          word2=''
      elif word==word3:
          word3=''
      

#Asks the user to give three words of choice and store them in variables. After every input we check if the input only contains letters.
#If the word contains anything other than letters it will display an error message
if word1 == '':
    try:
        word1 = st.text_input('Give the first word: ', 'to') #This will create an input field with label on the Streamlite app
        if word1!='':
            only_letters(word1)
    except UnboundLocalError: 
        st.error("Error: Please enter only letters!") #This will display an error message to the Streamlite app

if word2 == '' and word1 != '' and word1.isalpha():
    try:
        word2 = st.text_input('Give the second word: ', placeholder='go')
        if word2!='':
            only_letters(word2)
    except UnboundLocalError: 
        st.error("Error: Please enter only letters!")

if word3 == '' and word2 != '' and word2.isalpha() and word1 != '' and word1.isalpha():
    try:
        word3 = st.text_input('Give the result word: ', placeholder='out')
        if word3!='':
            only_letters(word3)
    except UnboundLocalError: 
        st.error("Error: Please enter only letters!")

#If all words are valid the program can start calculating the numbers
if word1 !='' and word2 != '' and word3!='' and word3.isalpha():
    isFilledIn = True

if isFilledIn:
    #The words are stored in a list to iterate over them (see further)
    words = [word1, word2, word3]

    ########################################################################## VARIABLES LIST ########################################
    #Empty variables list
    variables = []

    #get all unique letters of all the words and add them to the variables list so we get a list of all unique letters
    for word in words:
        for item in list(word):
            if item not in variables:
                variables.append(item)


    ########################################################################## DOMAINS DICTIONARY ####################################
    #Empty domains dictionary
    domains={}

    #For every unique letter in the variables list we assign the possible values the letter can have.
    for letter in variables:
        if letter == word1[0] or letter == word2[0] or letter == word3[0]: #If the letter is the first letter of a word the value can't be zero.
            domains[letter] = list(range(1,10)) #First letter of word cant have value zero.
        else:
            domains[letter] = list(range(0,10)) #Otherwise the value can be zero to ten.

    ######################################################################## CONSTRAINTS #################################################
    #Function to count value of word
    def count_value(word, values, variables):
        wordValue = '' #Empty string to add the values of the letters
        for letter in word: #For every letter in the word we add the value to a string
            wordValue+= str(values[variables.index(letter)]) #The corresponding value of the letter is searched by index in the values list and then added to the string
        return wordValue #Return the string of values 

    #A constraint that makes sure that the sum of the values of word1 & word2 is the value of word3. 
    def constraint_add(variables, values):
        factor1 = int(count_value(word1,values, variables)) #Calculate the value of word1 by using the helper function count_value()
        factor2 = int(count_value(word2, values, variables)) #Calculate the value of word2 by using the helper function count_value()
        result = int(count_value(word3, values, variables)) #Calculate the value of word3 by using the helper function count_value()
        return (factor1 + factor2) == result #This statement returns true when the sum is equal to the value of word3, otherwise this returns false and new values need to be used to get a true statement

    #This is a constraint so their are only unique values
    def constraint_unique(variables, values):
        return len(values) == len(set(values))  # Remove repeated values and count

    #Apply the constraints to the variables list
    constraints = [
        (variables, constraint_unique), #Make sure the values are unique
        (variables, constraint_add), #Make sure the value of word1 & word2 is the value of word3
    ]


    ########################################################################## CSP PROBLEM #############################################
    #This creates a new CspProblem object by using the variables list, the domains dictionary and the predefined constraints
    problem = CspProblem(variables, domains, constraints)

    #This line of code makes sure that the problem is solved by using backtracking when the constraints return false
    output = backtrack(problem)


    ######################################################################### SOLUTION ##################################################

    #Display the input words in a nice format on the Streamlite app
    st.write(word1, ' + ',word2, ' = ', word3)

    #Get the values of each word and display them
    all_values = ''
    for word in words:
        for letter in word:
            for key, value in output.items():
                if letter==key:
                   all_values+=str(value)  

    vw1=all_values[:len(word1)]
    vw2=all_values[len(word1): len(word1)+len(word2)]
    vw3=all_values[len(word1)+len(word2):]
    
    st.write(vw1, ' + ',vw2, ' = ', vw3)

    #Display the letters with their values on the Streamlite app
    for key, value in output.items():
        st.write(key, ' ==> ', str(value))