*** Settings ***
Library    RequestsLibrary
Library    Collections

*** Variables ***
${API_URL}    http://localhost:8001
${VALID_USERNAME}    testuser
${VALID_PASSWORD}    TestPass123

*** Test Cases ***
Successful Signup
    [Documentation]    Sign up a new user successfully
    Create Session    api    ${API_URL}
    ${payload}=    Create Dictionary    username=${VALID_USERNAME}    password=${VALID_PASSWORD}
    ${resp}=    Post On Session    api    /signup    json=${payload}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    200
    ${json}=    Set Variable    ${resp.json()}
    Dictionary Should Contain Key    ${json}    message
    Should Be Equal    ${json['message']}    User created successfully

Duplicate Signup
    [Documentation]    Attempt to sign up with an existing username
    Create Session    api    ${API_URL}
    ${payload}=    Create Dictionary    username=${VALID_USERNAME}    password=${VALID_PASSWORD}
    ${resp}=    Post On Session    api    /signup    json=${payload}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    400
    ${json}=    Set Variable    ${resp.json()}
    Dictionary Should Contain Key    ${json}    detail
    Should Contain    ${json['detail']}    User already exists

Signup Missing Username
    Create Session    api    ${API_URL}
    ${payload}=    Create Dictionary    password=${VALID_PASSWORD}
    ${resp}=    Post On Session    api    /signup    json=${payload}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    422

Signup Missing Password
    Create Session    api    ${API_URL}
    ${payload}=    Create Dictionary    username=${VALID_USERNAME}_missing_pwd
    ${resp}=    Post On Session    api    /signup    json=${payload}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    422

Signup Empty Username
    Create Session    api    ${API_URL}
    ${payload}=    Create Dictionary    username=    password=${VALID_PASSWORD}
    ${resp}=    Post On Session    api    /signup    json=${payload}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    422

Signup Empty Password
    Create Session    api    ${API_URL}
    ${payload}=    Create Dictionary    username=${VALID_USERNAME}_empty_pwd    password=
    ${resp}=    Post On Session    api    /signup    json=${payload}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    422

Signup Long Username and Password
    Create Session    api    ${API_URL}
    ${long_user}=    Evaluate    "'u'*1000"
    ${long_pass}=    Evaluate    "'p'*1000"
    ${payload}=    Create Dictionary    username=${long_user}    password=${long_pass}
    ${resp}=    Post On Session    api    /signup    json=${payload}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    200
    ${json}=    Set Variable    ${resp.json()}
    Should Be Equal    ${json['message']}    User created successfully

Signup Invalid Username Type
    Create Session    api    ${API_URL}
    ${payload}=    Create Dictionary    username=123    password=${VALID_PASSWORD}
    ${resp}=    Post On Session    api    /signup    json=${payload}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    422

Signup Invalid Password Type
    Create Session    api    ${API_URL}
    ${payload}=    Create Dictionary    username=${VALID_USERNAME}_invalid_pwd    password=True
    ${resp}=    Post On Session    api    /signup    json=${payload}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    422

Successful Login
    Create Session    api    ${API_URL}
    ${payload}=    Create Dictionary    username=${VALID_USERNAME}    password=${VALID_PASSWORD}
    ${resp}=    Post On Session    api    /login    json=${payload}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    200
    ${json}=    Set Variable    ${resp.json()}
    Should Be Equal    ${json['message']}    Login successful

Login Nonexistent User
    Create Session    api    ${API_URL}
    ${payload}=    Create Dictionary    username=nonexistent    password=any
    ${resp}=    Post On Session    api    /login    json=${payload}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    404
    ${json}=    Set Variable    ${resp.json()}
    Should Contain    ${json['detail']}    User not found

Login Wrong Password
    Create Session    api    ${API_URL}
    ${payload}=    Create Dictionary    username=${VALID_USERNAME}    password=WrongPass
    ${resp}=    Post On Session    api    /login    json=${payload}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    401
    ${json}=    Set Variable    ${resp.json()}
    Should Contain    ${json['detail']}    Invalid credentials

Login Missing Username
    Create Session    api    ${API_URL}
    ${payload}=    Create Dictionary    password=${VALID_PASSWORD}
    ${resp}=    Post On Session    api    /login    json=${payload}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    422

Login Missing Password
    Create Session    api    ${API_URL}
    ${payload}=    Create Dictionary    username=${VALID_USERNAME}
    ${resp}=    Post On Session    api    /login    json=${payload}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    422

Login Empty Username
    Create Session    api    ${API_URL}
    ${payload}=    Create Dictionary    username=    password=${VALID_PASSWORD}
    ${resp}=    Post On Session    api    /login    json=${payload}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    422

Login Empty Password
    Create Session    api    ${API_URL}
    ${payload}=    Create Dictionary    username=${VALID_USERNAME}    password=
    ${resp}=    Post On Session    api    /login    json=${payload}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    422

Login Invalid Username Type
    Create Session    api    ${API_URL}
    ${payload}=    Create Dictionary    username=123    password=${VALID_PASSWORD}
    ${resp}=    Post On Session    api    /login    json=${payload}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    422

Login Invalid Password Type
    Create Session    api    ${API_URL}
    ${payload}=    Create Dictionary    username=${VALID_USERNAME}    password=True
    ${resp}=    Post On Session    api    /login    json=${payload}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    422

*** Keywords ***