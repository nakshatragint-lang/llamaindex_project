*** Settings ***
Library    RequestsLibrary
Suite Setup    Create API Session

*** Variables ***
${BASE_URL}    http://localhost:8001
${TEST_USER}    testuser
${TEST_PASS}    TestPass123
${LONG_USERNAME}    Evaluate    'u'*256
${LONG_PASSWORD}    Evaluate    'p'*256

*** Test Cases ***
Signup Successful
    ${resp}    ${json}=    Signup User    ${TEST_USER}    ${TEST_PASS}
    Should Be Equal As Numbers    ${resp.status_code}    200
    Should Be Equal    ${json["message"]}    User created successfully

Signup Duplicate User
    ${resp}    ${json}=    Signup User    ${TEST_USER}    ${TEST_PASS}
    Should Be Equal As Numbers    ${resp.status_code}    400
    Should Contain    ${json["detail"]}    User already exists

Signup Missing Username
    ${payload}=    Create Dictionary    password=${TEST_PASS}
    ${resp}=    Post On Session    api    /signup    json=${payload}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    422

Signup Missing Password
    ${payload}=    Create Dictionary    username=${TEST_USER}
    ${resp}=    Post On Session    api    /signup    json=${payload}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    422

Signup Empty Username
    ${resp}    ${json}=    Signup User    ${EMPTY}    ${TEST_PASS}
    Should Be Equal As Numbers    ${resp.status_code}    422

Signup Empty Password
    ${resp}    ${json}=    Signup User    ${TEST_USER}    ${EMPTY}
    Should Be Equal As Numbers    ${resp.status_code}    422

Signup Invalid Username Type
    ${payload}=    Create Dictionary    username=12345    password=${TEST_PASS}
    ${resp}=    Post On Session    api    /signup    json=${payload}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    422

Signup Invalid Password Type
    ${payload}=    Create Dictionary    username=${TEST_USER}    password=12345
    ${resp}=    Post On Session    api    /signup    json=${payload}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    422

Signup Very Long Username
    ${resp}    ${json}=    Signup User    ${LONG_USERNAME}    ${TEST_PASS}
    Should Be Equal As Numbers    ${resp.status_code}    200
    Should Be Equal    ${json["message"]}    User created successfully

Signup Very Long Password
    ${resp}    ${json}=    Signup User    ${TEST_USER}_long    ${LONG_PASSWORD}
    Should Be Equal As Numbers    ${resp.status_code}    200
    Should Be Equal    ${json["message"]}    User created successfully

Login Successful
    ${resp}    ${json}=    Login User    ${TEST_USER}    ${TEST_PASS}
    Should Be Equal As Numbers    ${resp.status_code}    200
    Should Be Equal    ${json["message"]}    Login successful

Login Nonexistent User
    ${resp}    ${json}=    Login User    nonexistent_user    ${TEST_PASS}
    Should Be Equal As Numbers    ${resp.status_code}    404
    Should Contain    ${json["detail"]}    User not found

Login Wrong Password
    ${resp}    ${json}=    Login User    ${TEST_USER}    WrongPassword123
    Should Be Equal As Numbers    ${resp.status_code}    401
    Should Contain    ${json["detail"]}    Invalid credentials

Login Missing Username
    ${payload}=    Create Dictionary    password=${TEST_PASS}
    ${resp}=    Post On Session    api    /login    json=${payload}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    422

Login Missing Password
    ${payload}=    Create Dictionary    username=${TEST_USER}
    ${resp}=    Post On Session    api    /login    json=${payload}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    422

Login Empty Username
    ${resp}=    Post On Session    api    /login    json=${EMPTY}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    422

Login Empty Password
    ${payload}=    Create Dictionary    username=${TEST_USER}    password=${EMPTY}
    ${resp}=    Post On Session    api    /login    json=${payload}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    422

Login Invalid Username Type
    ${payload}=    Create Dictionary    username=12345    password=${TEST_PASS}
    ${resp}=    Post On Session    api    /login    json=${payload}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    422

Login Invalid Password Type
    ${payload}=    Create Dictionary    username=${TEST_USER}    password=12345
    ${resp}=    Post On Session    api    /login    json=${payload}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    422

*** Keywords ***
Create API Session
    Create Session    api    ${BASE_URL}

Signup User
    [Arguments]    ${username}    ${password}
    ${payload}=    Create Dictionary    username=${username}    password=${password}
    ${resp}=    Post On Session    api    /signup    json=${payload}    expected_status=any
    ${json}=    Set Variable    ${resp.json()}
    [Return]    ${resp}    ${json}

Login User
    [Arguments]    ${username}    ${password}
    ${payload}=    Create Dictionary    username=${username}    password=${password}
    ${resp}=    Post On Session    api    /login    json=${payload}    expected_status=any
    ${json}=    Set Variable    ${resp.json()}
    [Return]    ${resp}    ${json}