*** Settings ***
Library    RequestsLibrary
Library    Collections

*** Variables ***
${BASE_URL}    http://localhost:8001
${API}    api

*** Test Cases ***
Signup Successful
    [Setup]    Create Session    ${API}    ${BASE_URL}
    ${payload}=    Create Dictionary    username=testuser1    password=Pass123!
    ${resp}=    Post On Session    ${API}    /signup    json=${payload}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    200
    ${json}=    Set Variable    ${resp.json()}
    Dictionary Should Contain Value    ${json}    User created successfully

Signup Duplicate Username
    [Setup]    Create Session    ${API}    ${BASE_URL}
    ${payload}=    Create Dictionary    username=testuser2    password=Pass123!
    ${resp}=    Post On Session    ${API}    /signup    json=${payload}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    200
    ${payload_dup}=    Create Dictionary    username=testuser2    password=AnotherPass
    ${resp_dup}=    Post On Session    ${API}    /signup    json=${payload_dup}    expected_status=any
    Should Be Equal As Numbers    ${resp_dup.status_code}    400
    ${json}=    Set Variable    ${resp_dup.json()}
    Dictionary Should Contain Value    ${json}    User already exists

Signup Missing Username
    [Setup]    Create Session    ${API}    ${BASE_URL}
    ${payload}=    Create Dictionary    password=Pass123!
    ${resp}=    Post On Session    ${API}    /signup    json=${payload}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    422

Signup Missing Password
    [Setup]    Create Session    ${API}    ${BASE_URL}
    ${payload}=    Create Dictionary    username=testuser3
    ${resp}=    Post On Session    ${API}    /signup    json=${payload}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    422

Signup Empty Username
    [Setup]    Create Session    ${API}    ${BASE_URL}
    ${payload}=    Create Dictionary    username=    password=Pass123!
    ${resp}=    Post On Session    ${API}    /signup    json=${payload}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    422

Signup Empty Password
    [Setup]    Create Session    ${API}    ${BASE_URL}
    ${payload}=    Create Dictionary    username=testuser4    password=
    ${resp}=    Post On Session    ${API}    /signup    json=${payload}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    422

Signup Invalid Username Type
    [Setup]    Create Session    ${API}    ${BASE_URL}
    ${payload}=    Create Dictionary    username=12345    password=Pass123!
    ${resp}=    Post On Session    ${API}    /signup    json=${payload}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    422

Signup Invalid Password Type
    [Setup]    Create Session    ${API}    ${BASE_URL}
    ${payload}=    Create Dictionary    username=testuser5    password=12345
    ${resp}=    Post On Session    ${API}    /signup    json=${payload}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    422

Signup Long Username
    [Setup]    Create Session    ${API}    ${BASE_URL}
    ${long}=    Evaluate    'a'*300
    ${payload}=    Create Dictionary    username=${long}    password=Pass123!
    ${resp}=    Post On Session    ${API}    /signup    json=${payload}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    200

Login Successful
    [Setup]    Create Session    ${API}    ${BASE_URL}
    ${signup}=    Create Dictionary    username=loginuser    password=LoginPass!
    ${resp}=    Post On Session    ${API}    /signup    json=${signup}    expected_status=any
    ${login_payload}=    Create Dictionary    username=loginuser    password=LoginPass!
    ${login_resp}=    Post On Session    ${API}    /login    json=${login_payload}    expected_status=any
    Should Be Equal As Numbers    ${login_resp.status_code}    200
    ${json}=    Set Variable    ${login_resp.json()}
    Dictionary Should Contain Value    ${json}    Login successful

Login Nonexistent User
    [Setup]    Create Session    ${API}    ${BASE_URL}
    ${payload}=    Create Dictionary    username=nosuchuser    password=any
    ${resp}=    Post On Session    ${API}    /login    json=${payload}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    404
    ${json}=    Set Variable    ${resp.json()}
    Dictionary Should Contain Value    ${json}    User not found

Login Wrong Password
    [Setup]    Create Session    ${API}    ${BASE_URL}
    ${signup}=    Create Dictionary    username=wrongpassuser    password=CorrectPass!
    ${resp}=    Post On Session    ${API}    /signup    json=${signup}    expected_status=any
    ${login}=    Create Dictionary    username=wrongpassuser    password=BadPass!
    ${login_resp}=    Post On Session    ${API}    /login    json=${login}    expected_status=any
    Should Be Equal As Numbers    ${login_resp.status_code}    401
    ${json}=    Set Variable    ${login_resp.json()}
    Dictionary Should Contain Value    ${json}    Invalid credentials

Login Missing Username
    [Setup]    Create Session    ${API}    ${BASE_URL}
    ${payload}=    Create Dictionary    password=Pass123!
    ${resp}=    Post On Session    ${API}    /login    json=${payload}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    422

Login Missing Password
    [Setup]    Create Session    ${API}    ${BASE_URL}
    ${payload}=    Create Dictionary    username=someuser
    ${resp}=    Post On Session    ${API}    /login    json=${payload}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    422

Login Empty Username
    [Setup]    Create Session    ${API}    ${BASE_URL}
    ${payload}=    Create Dictionary    username=    password=Pass123!
    ${resp}=    Post On Session    ${API}    /login    json=${payload}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    422

Login Empty Password
    [Setup]    Create Session    ${API}    ${BASE_URL}
    ${payload}=    Create Dictionary    username=someuser    password=
    ${resp}=    Post On Session    ${API}    /login    json=${payload}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    422

Login Invalid Username Type
    [Setup]    Create Session    ${API}    ${BASE_URL}
    ${payload}=    Create Dictionary    username=12345    password=Pass123!
    ${resp}=    Post On Session    ${API}    /login    json=${payload}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    422

Login Invalid Password Type
    [Setup]    Create Session    ${API}    ${BASE_URL}
    ${payload}=    Create Dictionary    username=loginuser2    password=12345
    ${resp}=    Post On Session    ${API}    /login    json=${payload}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    422

Login Long Username
    [Setup]    Create Session    ${API}    ${BASE_URL}
    ${long}=    Evaluate    'b'*300
    ${payload}=    Create Dictionary    username=${long}    password=Pass123!
    ${resp}=    Post On Session    ${API}    /login    json=${payload}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    404