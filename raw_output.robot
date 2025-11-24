*** Settings ***
Library    Collections
Library    DateTime

*** Variables ***
${FIXED_TODAY}    2023-03-15

*** Test Cases ***
Age Same Day As Today
    [Documentation]    Birthdate equals today's date → age 0 years, 0 months, 0 days
    ${age_year}    ${age_month}    ${age_day}=    Calculate Age    2023    3    15
    Should Be Equal As Numbers    ${age_year}    0
    Should Be Equal As Numbers    ${age_month}    0
    Should Be Equal As Numbers    ${age_day}    0

Age One Day Before Today
    [Documentation]    Birthdate one day before today → age 0 years, 0 months, 1 day
    ${age_year}    ${age_month}    ${age_day}=    Calculate Age    2023    3    14
    Should Be Equal As Numbers    ${age_year}    0
    Should Be Equal As Numbers    ${age_month}    0
    Should Be Equal As Numbers    ${age_day}    1

Age One Month Before Today (Same Day)
    [Documentation]    Birthdate one month before today (same day) → age 0 years, 1 month, 0 days
    ${age_year}    ${age_month}    ${age_day}=    Calculate Age    2023    2    15
    Should Be Equal As Numbers    ${age_year}    0
    Should Be Equal As Numbers    ${age_month}    1
    Should Be Equal As Numbers    ${age_day}    0

Age One Year Before Today
    [Documentation]    Birthdate exactly one year before today → age 1 year, 0 months, 0 days
    ${age_year}    ${age_month}    ${age_day}=    Calculate Age    2022    3    15
    Should Be Equal As Numbers    ${age_year}    1
    Should Be Equal As Numbers    ${age_month}    0
    Should Be Equal As Numbers    ${age_day}    0

Age Leap Day Birthdate Non‑Leap Current Year
    [Documentation]    Birthdate Feb 29 on a leap year, current year is non‑leap (2023‑03‑15) → age 23 years, 0 months, 14 days
    ${age_year}    ${age_month}    ${age_day}=    Calculate Age    2000    2    29
    Should Be Equal As Numbers    ${age_year}    23
    Should Be Equal As Numbers    ${age_month}    0
    Should Be Equal As Numbers    ${age_day}    14

Future Birthdate Should Raise Error
    [Documentation]    Birthdate after today must raise a ValueError
    Run Keyword And Expect Error    ValueError    Calculate Age    2024    1    1

Invalid Month Should Raise Error
    [Documentation]    Month value greater than 12 must raise a ValueError
    Run Keyword And Expect Error    ValueError    Calculate Age    2020    13    10

Invalid Day Should Raise Error
    [Documentation]    Day value greater than 31 must raise a ValueError
    Run Keyword And Expect Error    ValueError    Calculate Age    2020    12    32

Negative Year Should Raise Error
    [Documentation]    Negative year must raise a ValueError
    Run Keyword And Expect Error    ValueError    Calculate Age    -1    5    10

Very Old Birthdate
    [Documentation]    Birthdate far in the past (1900‑01‑01) → verify large age calculation
    ${age_year}    ${age_month}    ${age_day}=    Calculate Age    1900    1    1
    Should Be Equal As Numbers    ${age_year}    123
    Should Be Equal As Numbers    ${age_month}    2
    Should Be Equal As Numbers    ${age_day}    14

*** Keywords ***
Calculate Age
    [Arguments]    ${birth_year}    ${birth_month}    ${birth_day}
    ${today}=    Convert To Date    ${FIXED_TODAY}
    ${birth}=    Evaluate    __import__('datetime').date(int(${birth_year}), int(${birth_month}), int(${birth_day}))
    ${today_date}=    Evaluate    __import__('datetime').date(int(${today.year}), int(${today.month}), int(${today.day}))
    Run Keyword If    ${birth} > ${today_date}    Raise ValueError    Birthdate is in the future
    ${years}=    Evaluate    ${today_date}.year - ${birth}.year - ((${today_date}.month, ${today_date}.day) < (${birth}.month, ${birth}.day))
    ${months}=    Evaluate    (${today_date}.month - ${birth}.month - (${today_date}.day < ${birth}.day)) % 12
    ${prev_month}=    Evaluate    (${today_date}.month - 1) if ${today_date}.day < ${birth}.day else ${today_date}.month
    ${prev_year}=    Evaluate    ${today_date}.year if ${today_date}.month != 1 else ${today_date}.year - 1
    ${days_in_prev_month}=    Evaluate    __import__('calendar').monthrange(${prev_year}, ${prev_month})[1]
    ${days}=    Evaluate    ${today_date}.day - ${birth}.day if ${today_date}.day >= ${birth}.day else ${today_date}.day - ${birth}.day + ${days_in_prev_month}
    [Return]    ${years}    ${months}    ${days}
