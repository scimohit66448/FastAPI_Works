To run the Server :  uvicorn main:my_rest_app --reload
Before running server make sure that:
1. All the packages mentioned in requirements.txt is installed on your machine/Server.
2.DB details are correct in Conn String in Constants.py file
3. If table is not present in the DB , uncomment create table function and run DbOps.py to create the table
    3.1 you can manually create a table named "user" with fields firstname , lastname and age in your DB.


Points to improve :

Trim the spaces in firstname and last name
Apply validation for ge should not be less than 0
fname and lname should not be empty