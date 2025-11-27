*** Settings ***
Library           Collections
Library           DateTime
Library           OperatingSystem

*** Variables ***
${FIXED_TODAY}    2025-05-20

*** Test Cases ***
Normal Age Calculation
    [Documentation]    Verify age calculation for a typical birth date.
    ${birth}=    Create Date    1990-01-15
    ${expected}=    Evaluate    {'years': 35, 'months': 4, 'days': 5}    datetime, dateutil
    ${result}=    Calculate Age    ${birth}    ${FIXED_TODAY}
    Dictionaries Should Be Equal    ${result}    ${expected}

Leap Year Birth On Feb 29 (Non‑Leap Current Year)
    [Documentation]    Verify age when born on Feb 29 and current year is not a leap year.
    ${birth}=    Create Date    2000-02-29
    ${expected}=    Evaluate    {'years': 25, 'months': 2, 'days': 19}    datetime, dateutil
    ${result}=    Calculate Age    ${birth}    ${FIXED_TODAY}
    Dictionaries Should Be Equal    ${result}    ${expected}

Leap Year Birth On Feb 29 (Leap Current Year)
    [Documentation]    Verify age when both birth year and current year are leap years.
    ${birth}=    Create Date    2004-02-29
    ${today}=    Set Variable    2024-02-29
    ${expected}=    Evaluate    {'years': 20, 'months': 0, 'days': 0}    datetime, dateutil
    ${result}=    Calculate Age    ${birth}    ${today}
    Dictionaries Should Be Equal    ${result}    ${expected}

Birth Date Is Today
    [Documentation]    Age should be zero when birth date equals today.
    ${birth}=    Create Date    2025-05-20
    ${expected}=    Evaluate    {'years': 0, 'months': 0, 'days': 0}    datetime, dateutil
    ${result}=    Calculate Age    ${birth}    ${FIXED_TODAY}
    Dictionaries Should Be Equal    ${result}    ${expected}

Future Birth Date Should Fail
    [Documentation]    Birth dates in the future must raise an error.
    ${birth}=    Create Date    2026-01-01
    Run Keyword And Expect Error    ValueError: Birth date cannot be in the future    Calculate Age    ${birth}    ${FIXED_TODAY}

Invalid Month Should Fail
    [Documentation]    Month value outside 1‑12 must raise an error.
    Run Keyword And Expect Error    ValueError: Invalid month value    Create Date    1990-13-01

Invalid Day Should Fail
    [Documentation]    Day value outside valid range for month must raise an error.
    Run Keyword And Expect Error    ValueError: Invalid day value    Create Date    1990-04-31

Edge Case End Of Month To Start Of Next Month
    [Documentation]    Verify age when birth date is last day of month and today is first day of next month.
    ${birth}=    Create Date    2024-04-30
    ${today}=    Set Variable    2024-05-01
    ${expected}=    Evaluate    {'years': 0, 'months': 0, 'days': 1}    datetime, dateutil
    ${result}=    Calculate Age    ${birth}    ${today}
    Dictionaries Should Be Equal    ${result}    ${expected}

Edge Case Start Of Year
    [Documentation]    Verify age when birth date is Jan 1 and today is Dec 31 of same year.
    ${birth}=    Create Date    2024-01-01
    ${today}=    Set Variable    2024-12-31
    ${expected}=    Evaluate    {'years': 0, 'months': 11, 'days': 30}    datetime, dateutil
    ${result}=    Calculate Age    ${birth}    ${today}
    Dictionaries Should Be Equal    ${result}    ${expected}

*** Keywords ***
Create Date
    [Arguments]    ${date_string}
    ${parts}=    Split String    ${date_string}    -
    ${year}=    Convert To Integer    ${parts[0]}
    ${month}=    Convert To Integer    ${parts[1]}
    ${day}=    Convert To Integer    ${parts[2]}
    Run Keyword If    ${month} < 1 or ${month} > 12    Raise Error    ValueError: Invalid month value
    ${max_day}=    Get Max Day Of Month    ${year}    ${month}
    Run Keyword If    ${day} < 1 or ${day} > ${max_day}    Raise Error    ValueError: Invalid day value
    ${date}=    Evaluate    datetime.date(${year}, ${month}, ${day})    datetime
    [Return]    ${date}

Get Max Day Of Month
    [Arguments]    ${year}    ${month}
    ${is_leap}=    Evaluate    calendar.isleap(${year})    calendar
    ${days_in_month}=    Evaluate
    ...    {1:31, 2:29 if ${is_leap} else 28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}[${month}]
    ...    datetime, calendar
    [Return]    ${days_in_month}

Calculate Age
    [Arguments]    ${birth_date}    ${today_date}
    Run Keyword If    ${birth_date} > ${today_date}    Raise Error    ValueError: Birth date cannot be in the future
    ${delta}=    Evaluate    relativedelta(${today_date}, ${birth_date})    dateutil.relativedelta
    ${years}=    Set Variable    ${delta.years}
    ${months}=    Set Variable    ${delta.months}
    ${days}=    Set Variable    ${delta.days}
    ${result}=    Create Dictionary    years=${years}    months=${months}    days=${days}
    [Return]    ${result}