*** Settings ***
Library    Collections
Library    DateTime

*** Variables ***
${TODAY}    2023-08-15

*** Test Cases ***
Valid Age Calculation
    ${age}=    Calculate Age    1990    1    10    ${TODAY}
    Should Be Equal As Numbers    ${age}[0]    33
    Should Be Equal As Numbers    ${age}[1]    7
    Should Be Equal As Numbers    ${age}[2]    5

Birth Today
    ${age}=    Calculate Age    2023    8    15    ${TODAY}
    Should Be Equal As Numbers    ${age}[0]    0
    Should Be Equal As Numbers    ${age}[1]    0
    Should Be Equal As Numbers    ${age}[2]    0

Future Birth Date
    Run Keyword And Expect Error    *Future birth date*    Calculate Age    2024    1    1    ${TODAY}

Leap Year Birth
    ${age}=    Calculate Age    2000    2    29    ${TODAY}
    Should Be Equal As Numbers    ${age}[0]    23
    Should Be Equal As Numbers    ${age}[1]    5
    Should Be Equal As Numbers    ${age}[2]    17

Invalid Month
    Run Keyword And Expect Error    *Invalid month*    Calculate Age    1990    13    1    ${TODAY}

Invalid Day
    Run Keyword And Expect Error    *Invalid day*    Calculate Age    1990    2    30    ${TODAY}

Very Old Birth Date
    ${age}=    Calculate Age    1900    1    1    ${TODAY}
    Should Be Equal As Numbers    ${age}[0]    123
    Should Be Equal As Numbers    ${age}[1]    7
    Should Be Equal As Numbers    ${age}[2]    14

*** Keywords ***
Calculate Age
    [Arguments]    ${year}    ${month}    ${day}    ${today_str}
    # Validate month
    Run Keyword If    ${month} < 1 or ${month} > 12    Raise Invalid Month
    # Validate day (basic check, detailed validation later)
    Run Keyword If    ${day} < 1 or ${day} > 31    Raise Invalid Day
    ${today}=    Evaluate    datetime.datetime.strptime('${today_str}', '%Y-%m-%d').date()    datetime
    ${birth}=    Evaluate    datetime.date(${year}, ${month}, ${day})    datetime
    Run Keyword If    ${birth} > ${today}    Raise Future Birth Date
    # Use relativedelta for accurate year/month/day difference
    ${rel}=    Evaluate    __import__('dateutil.relativedelta').relativedelta(${today}, ${birth})    datetime
    ${age_years}=    Set Variable    ${rel}.years
    ${age_months}=    Set Variable    ${rel}.months
    ${age_days}=    Set Variable    ${rel}.days
    [Return]    @{age_years}    ${age_months}    ${age_days}

Raise Invalid Month
    Fail    Invalid month

Raise Invalid Day
    Fail    Invalid day

Raise Future Birth Date
    Fail    Future birth date