##	Tools and Frameworks
Language used: Python
Testing Framework: Pytest and requests library
Logging: CustomLogger using python logging library
Report: pytest-html reports

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
6. I tried to store all data in file.

## Improvements needed
1. Have to change absolute paths into relative paths to handle files

