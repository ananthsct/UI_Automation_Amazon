##	Tools and Frameworks
Language used: Python
Testing Framework: Pytest
Logging: CustomLogger using python logging library
Report: pytest-html reports
Data: Used JSON file to read few test case input data

## execution instructions
pytest -s -v .\tests\amazon\test_searchProduct.py --html=reports\report.html

## Reports
Test reports will be automatically generated in the reports/ directory after test execution.
Open the generated HTML report in your web browser to view detailed test results.

## Assumptions and challenges
While developing test cases, the following assumptions were made:
1. From the understanding of test-cases, I have modified few points.
2. I have chosen product with maximum ratings and minimum value
3. Only few data are read from JSON file
4. It was difficult to select the sub-menu of All-items, used execute_script
5. Selection of Go button was difficult, then simply pressed ENTER key after entering maximum price
6. Instead of printing search results, I have added them to a file 'search_result.txt'
7. Main challenge was to create product list along with its name, price and rating from the search result of page 1 and 2
8. Used parent and child method to overcome above challenge then created list of tuple

## Improvements needed
1. Have to change absolute paths into relative paths to handle files
2. Have to add comments and instructions for every function inside page objects

## Framework structure explanation according to test cases
1. Test cases 1 to 6 added to 'test_amazonLogin.py' file, and it's related functions are 
    created in POM 'loginPage.py'
2. Test cases 7 to 13 added to 'test_searchProduct.py' file, and it's related functions are 
    created in POM 'searchProductPage.py'