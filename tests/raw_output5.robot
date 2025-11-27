*** Settings ***
Library    RequestsLibrary

Suite Setup    Create Session    api    http://localhost:8001

*** Variables ***
${VALID_USERNAME}    testuser
${VALID_PASSWORD}    TestPass123!
${LONG_STRING}    ${'a'*256}
${NUMERIC_USERNAME}    12345
${NUMERIC_PASSWORD}    67890

*** Test Cases ***
Signup Successful
    ${payload}=    Create Dictionary    username=${VALID_USERNAME}    password=${VALID_PASSWORD}
    ${resp}=    Post On Session    api    /signup    json=${payload}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    200
    ${json}=    Set Variable    ${resp.json()}
    Dictionary Should Contain Key    ${json}    message
    Should Be Equal    ${json['message']}    User created successfully

Signup Duplicate User
    ${payload}=    Create Dictionary    username=${VALID_USERNAME}    password=${VALID_PASSWORD}
    ${first}=    Post On Session    api    /signup    json=${payload}    expected_status=any
    ${dup}=    Post On Session    api    /signup    json=${payload}    expected_status=any
    Should Be Equal As Numbers    ${dup.status_code}    400
    ${dup_json}=    Set Variable    ${dup.json()}
    Dictionary Should Contain Key    ${dup_json}    detail
    Should Contain    ${dup_json['detail']}    User already exists

Signup Missing Username
    ${payload}=    Create Dictionary    password=${VALID_PASSWORD}
    ${resp}=    Post On Session    api    /signup    json=${payload}    expected_status=any
    Should Not Be Equal As Numbers    ${resp.status_code}    200

Signup Missing Password
    ${payload}=    Create Dictionary    username=${VALID_USERNAME}
    ${resp}=    Post On Session    api    /signup    json=${payload}    expected_status=any
    Should Not Be Equal As Numbers    ${resp.status_code}    200

Signup Empty Username
    ${payload}=    Create Dictionary    username=    password=${VALID_PASSWORD}
    ${resp}=    Post On Session    api    /signup    json=${payload}    expected_status=any
    Should Not Be Equal As Numbers    ${resp.status_code}    200

Signup Empty Password
    ${payload}=    Create Dictionary    username=${VALID_USERNAME}    password=
    ${resp}=    Post On Session    api    /signup    json=${payload}    expected_status=any
    Should Not Be Equal As Numbers    ${resp.status_code}    200

Signup Username Too Long
    ${payload}=    Create Dictionary    username=${LONG_STRING}    password=${VALID_PASSWORD}
    ${resp}=    Post On Session    api    /signup    json=${payload}    expected_status=any
    Should Not Be Equal As Numbers    ${resp.status_code}    200

Signup Password Too Long
    ${payload}=    Create Dictionary    username=${VALID_USERNAME}    password=${LONG_STRING}
    ${resp}=    Post On Session    api    /signup    json=${payload}    expected_status=any
    Should Not Be Equal As Numbers    ${resp.status_code}    200

Signup Username Invalid Type
    ${payload}=    Create Dictionary    username=${NUMERIC_USERNAME}    password=${VALID_PASSWORD}
    ${resp}=    Post On Session    api    /signup    json=${payload}    expected_status=any
    Should Not Be Equal As Numbers    ${resp.status_code}    200

Signup Password Invalid Type
    ${payload}=    Create Dictionary    username=${VALID_USERNAME}    password=${NUMERIC_PASSWORD}
    ${resp}=    Post On Session    api    /signup    json=${payload}    expected_status=any
    Should Not Be Equal As Numbers    ${resp.status_code}    200

Login Successful
    # Ensure user exists
    ${payload}=    Create Dictionary    username=${VALID_USERNAME}    password=${VALID_PASSWORD}
    ${_}=    Post On Session    api    /signup    json=${payload}    expected_status=any
    ${login_payload}=    Create Dictionary    username=${VALID_USERNAME}    password=${VALID_PASSWORD}
    ${resp}=    Post On Session    api    /login    json=${login_payload}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    200
    ${json}=    Set Variable    ${resp.json()}
    Dictionary Should Contain Key    ${json}    message
    Should Be Equal    ${json['message']}    Login successful

Login User Not Found
    ${login_payload}=    Create Dictionary    username=nonexistent    password=${VALID_PASSWORD}
    ${resp}=    Post On Session    api    /login    json=${login_payload}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    404
    ${json}=    Set Variable    ${resp.json()}
    Dictionary Should Contain Key    ${json}    detail
    Should Contain    ${json['detail']}    User not found

Login Wrong Password
    # Ensure user exists
    ${payload}=    Create Dictionary    username=${VALID_USERNAME}    password=${VALID_PASSWORD}
    ${_}=    Post On Session    api    /signup    json=${payload}    expected_status=any
    ${login_payload}=    Create Dictionary    username=${VALID_USERNAME}    password=WrongPass123
    ${resp}=    Post On Session    api    /login    json=${login_payload}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    401
    ${json}=    Set Variable    ${resp.json()}
    Dictionary Should Contain Key    ${json}    detail
    Should Contain    ${json['detail']}    Invalid credentials

Login Missing Username
    ${payload}=    Create Dictionary    password=${VALID_PASSWORD}
    ${resp}=    Post On Session    api    /login    json=${payload}    expected_status=any
    Should Not Be Equal As Numbers    ${resp.status_code}    200

Login Missing Password
    ${payload}=    Create Dictionary    username=${VALID_USERNAME}
    ${resp}=    Post On Session    api    /login    json=${payload}    expected_status=any
    Should Not Be Equal As Numbers    ${resp.status_code}    200

Login Empty Username
    ${payload}=    Create Dictionary    username=    password=${VALID_PASSWORD}
    ${resp}=    Post On Session    api    /login    json=${payload}    expected_status=any
    Should Not Be Equal As Numbers    ${resp.status_code}    200

Login Empty Password
    ${payload}=    Create Dictionary    username=${VALID_USERNAME}    password=
    ${resp}=    Post On Session    api    /login    json=${payload}    expected_status=any
    Should Not Be Equal As Numbers    ${resp.status_code}    200

Login Username Invalid Type
    ${payload}=    Create Dictionary    username=${NUMERIC_USERNAME}    password=${VALID_PASSWORD}
    ${resp}=    Post On Session    api    /login    json=${payload}    expected_status=any
    Should Not Be Equal As Numbers    ${resp.status_code}    200

Login Password Invalid Type
    ${payload}=    Create Dictionary    username=${VALID_USERNAME}    password=${NUMERIC_PASSWORD}
    ${resp}=    Post On Session    api    /login    json=${payload}    expected_status=any
    Should Not Be Equal As Numbers    ${resp.status_code}    200

*** Keywords ***