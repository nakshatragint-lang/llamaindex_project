*** Settings ***
Library    RequestsLibrary
Library    Collections
Suite Setup    Create Session    api    http://localhost:8001

*** Variables ***
${VALID_USERNAME}          testuser
${VALID_PASSWORD}          TestPass123
${DUPLICATE_USERNAME}      dupuser
${NONEXISTENT_USERNAME}    unknownuser
${LONG_USERNAME}           ${EMPTY}
${LONG_PASSWORD}           ${EMPTY}
${INVALID_USERNAME}        12345
${INVALID_PASSWORD}        67890
${EMPTY_STRING}            ${EMPTY}
${VERY_LONG_LENGTH}        1000

*** Test Cases ***
Signup Success
    ${payload}=    Create Dictionary    username=${VALID_USERNAME}    password=${VALID_PASSWORD}
    ${resp}=    Post On Session    api    /signup    json=${payload}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    200
    ${json}=    Set Variable    ${resp.json()}
    Dictionary Should Contain Value    ${json}    User created successfully

Signup Duplicate User
    ${payload}=    Create Dictionary    username=${DUPLICATE_USERNAME}    password=${VALID_PASSWORD}
    ${first}=    Post On Session    api    /signup    json=${payload}    expected_status=any
    Should Be Equal As Numbers    ${first.status_code}    200
    ${second}=    Post On Session    api    /signup    json=${payload}    expected_status=any
    Should Be Equal As Numbers    ${second.status_code}    400
    ${json}=    Set Variable    ${second.json()}
    Dictionary Should Contain Value    ${json}    User already exists

Signup Missing Username
    ${payload}=    Create Dictionary    password=${VALID_PASSWORD}
    ${resp}=    Post On Session    api    /signup    json=${payload}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    422

Signup Missing Password
    ${payload}=    Create Dictionary    username=${VALID_USERNAME}
    ${resp}=    Post On Session    api    /signup    json=${payload}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    422

Signup Empty Username
    ${payload}=    Create Dictionary    username=${EMPTY_STRING}    password=${VALID_PASSWORD}
    ${resp}=    Post On Session    api    /signup    json=${payload}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    200
    ${json}=    Set Variable    ${resp.json()}
    Dictionary Should Contain Value    ${json}    User created successfully

Signup Empty Password
    ${payload}=    Create Dictionary    username=${VALID_USERNAME}    password=${EMPTY_STRING}
    ${resp}=    Post On Session    api    /signup    json=${payload}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    200
    ${json}=    Set Variable    ${resp.json()}
    Dictionary Should Contain Value    ${json}    User created successfully

Signup Invalid Username Type
    ${payload}=    Create Dictionary    username=${INVALID_USERNAME}    password=${VALID_PASSWORD}
    ${resp}=    Post On Session    api    /signup    json=${payload}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    422

Signup Invalid Password Type
    ${payload}=    Create Dictionary    username=${VALID_USERNAME}    password=${INVALID_PASSWORD}
    ${resp}=    Post On Session    api    /signup    json=${payload}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    422

Signup Very Long Username
    ${LONG_USERNAME}=    Evaluate    'a' * ${VERY_LONG_LENGTH}
    ${payload}=    Create Dictionary    username=${LONG_USERNAME}    password=${VALID_PASSWORD}
    ${resp}=    Post On Session    api    /signup    json=${payload}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    200
    ${json}=    Set Variable    ${resp.json()}
    Dictionary Should Contain Value    ${json}    User created successfully

Login Success
    # Ensure user exists
    ${payload}=    Create Dictionary    username=${VALID_USERNAME}    password=${VALID_PASSWORD}
    ${signup}=    Post On Session    api    /signup    json=${payload}    expected_status=any
    ${login_payload}=    Create Dictionary    username=${VALID_USERNAME}    password=${VALID_PASSWORD}
    ${resp}=    Post On Session    api    /login    json=${login_payload}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    200
    ${json}=    Set Variable    ${resp.json()}
    Dictionary Should Contain Value    ${json}    Login successful

Login User Not Found
    ${payload}=    Create Dictionary    username=${NONEXISTENT_USERNAME}    password=${VALID_PASSWORD}
    ${resp}=    Post On Session    api    /login    json=${payload}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    404
    ${json}=    Set Variable    ${resp.json()}
    Dictionary Should Contain Value    ${json}    User not found

Login Wrong Password
    # Ensure user exists
    ${payload}=    Create Dictionary    username=${DUPLICATE_USERNAME}    password=${VALID_PASSWORD}
    ${signup}=    Post On Session    api    /signup    json=${payload}    expected_status=any
    ${login_payload}=    Create Dictionary    username=${DUPLICATE_USERNAME}    password=WrongPass
    ${resp}=    Post On Session    api    /login    json=${login_payload}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    401
    ${json}=    Set Variable    ${resp.json()}
    Dictionary Should Contain Value    ${json}    Invalid credentials

Login Missing Username
    ${payload}=    Create Dictionary    password=${VALID_PASSWORD}
    ${resp}=    Post On Session    api    /login    json=${payload}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    422

Login Missing Password
    ${payload}=    Create Dictionary    username=${VALID_USERNAME}
    ${resp}=    Post On Session    api    /login    json=${payload}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    422

Login Empty Username
    ${payload}=    Create Dictionary    username=${EMPTY_STRING}    password=${VALID_PASSWORD}
    ${resp}=    Post On Session    api    /login    json=${payload}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    404

Login Empty Password
    ${payload}=    Create Dictionary    username=${VALID_USERNAME}    password=${EMPTY_STRING}
    ${resp}=    Post On Session    api    /login    json=${payload}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    401

Login Invalid Username Type
    ${payload}=    Create Dictionary    username=${INVALID_USERNAME}    password=${VALID_PASSWORD}
    ${resp}=    Post On Session    api    /login    json=${payload}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    422

Login Invalid Password Type
    ${payload}=    Create Dictionary    username=${VALID_USERNAME}    password=${INVALID_PASSWORD}
    ${resp}=    Post On Session    api    /login    json=${payload}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    422

*** Keywords ***