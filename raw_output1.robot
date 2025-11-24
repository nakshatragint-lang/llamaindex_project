*** Settings ***
Library    Collections
Library    BuiltIn
Library    RequestsLibrary
Suite Setup    Create Session    api    ${API_URL}

*** Variables ***
${API_URL}    http://localhost:8000

*** Test Cases ***
Add Function - Positive Numbers
    ${result}=    Add    2    3
    Should Be Equal As Numbers    ${result}    5

Add Function - Negative Numbers
    ${result}=    Add    -2    -5
    Should Be Equal As Numbers    ${result}    -7

Add Function - Zero
    ${result}=    Add    0    0
    Should Be Equal As Numbers    ${result}    0

Add Function - Large Numbers
    ${result}=    Add    123456789    987654321
    Should Be Equal As Numbers    ${result}    1111111110

Add Function - Invalid Types
    Run Keyword And Expect Error    TypeError*    Add    a    1

Subtract Function - Positive Numbers
    ${result}=    Subtract    10    4
    Should Be Equal As Numbers    ${result}    6

Subtract Function - Negative Result
    ${result}=    Subtract    4    10
    Should Be Equal As Numbers    ${result}    -6

Subtract Function - Zero
    ${result}=    Subtract    0    0
    Should Be Equal As Numbers    ${result}    0

Subtract Function - Invalid Types
    Run Keyword And Expect Error    TypeError*    Subtract    5    "b"

Multiply Function - Positive Numbers
    ${result}=    Multiply    6    7
    Should Be Equal As Numbers    ${result}    42

Multiply Function - With Zero
    ${result}=    Multiply    0    123
    Should Be Equal As Numbers    ${result}    0

Multiply Function - Negative Numbers
    ${result}=    Multiply    -3    5
    Should Be Equal As Numbers    ${result}    -15

Multiply Function - Invalid Types
    Run Keyword And Expect Error    TypeError*    Multiply    "x"    2

Divide Function - Normal Division
    ${result}=    Divide    20    4
    Should Be Equal As Numbers    ${result}    5

Divide Function - Float Result
    ${result}=    Divide    7    2
    Should Be Equal As Numbers    ${result}    3.5

Divide Function - Negative Numbers
    ${result}=    Divide    -9    3
    Should Be Equal As Numbers    ${result}    -3

Divide Function - Division By Zero
    Run Keyword And Expect Error    ValueError*    Divide    5    0

Divide Function - Invalid Types
    Run Keyword And Expect Error    TypeError*    Divide    10    "z"

Signup - Successful Registration
    ${payload}=    Create Dictionary    username=alice    password=Secret123
    ${resp}=    Post On Session    api    /signup    json=${payload}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    200
    ${json}=    Set Variable    ${resp.json()}
    Dictionary Should Contain Key    ${json}    message
    Should Be Equal    ${json['message']}    User created successfully

Signup - Duplicate User
    ${payload}=    Create Dictionary    username=bob    password=Pass123
    ${resp}=    Post On Session    api    /signup    json=${payload}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    200
    ${resp_dup}=    Post On Session    api    /signup    json=${payload}    expected_status=any
    Should Be Equal As Numbers    ${resp_dup.status_code}    400
    ${json_dup}=    Set Variable    ${resp_dup.json()}
    Dictionary Should Contain Key    ${json_dup}    detail
    Should Be Equal    ${json_dup['detail']}    User already exists

Signup - Missing Username
    ${payload}=    Create Dictionary    password=NoUserPass
    ${resp}=    Post On Session    api    /signup    json=${payload}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    422

Signup - Missing Password
    ${payload}=    Create Dictionary    username=nopass
    ${resp}=    Post On Session    api    /signup    json=${payload}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    422

Signup - Empty Username
    ${payload}=    Create Dictionary    username=    password=EmptyUser
    ${resp}=    Post On Session    api    /signup    json=${payload}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    200
    ${json}=    Set Variable    ${resp.json()}
    Should Be Equal    ${json['message']}    User created successfully

Signup - Empty Password
    ${payload}=    Create Dictionary    username=emptyPass    password=
    ${resp}=    Post On Session    api    /signup    json=${payload}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    200
    ${json}=    Set Variable    ${resp.json()}
    Should Be Equal    ${json['message']}    User created successfully

Signup - Invalid Types
    ${payload}=    Create Dictionary    username=12345    password=67890
    ${resp}=    Post On Session    api    /signup    json=${payload}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    200
    ${json}=    Set Variable    ${resp.json()}
    Should Be Equal    ${json['message']}    User created successfully

Login - Successful Authentication
    # Ensure user exists
    ${signup}=    Create Dictionary    username=charlie    password=MyPass123
    ${resp_signup}=    Post On Session    api    /signup    json=${signup}    expected_status=any
    Should Be Equal As Numbers    ${resp_signup.status_code}    200
    ${login}=    Create Dictionary    username=charlie    password=MyPass123
    ${resp}=    Post On Session    api    /login    json=${login}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    200
    ${json}=    Set Variable    ${resp.json()}
    Dictionary Should Contain Key    ${json}    message
    Should Be Equal    ${json['message']}    Login successful

Login - User Not Found
    ${login}=    Create Dictionary    username=nonexistent    password=any
    ${resp}=    Post On Session    api    /login    json=${login}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    404
    ${json}=    Set Variable    ${resp.json()}
    Dictionary Should Contain Key    ${json}    detail
    Should Be Equal    ${json['detail']}    User not found

Login - Invalid Password
    # Ensure user exists
    ${signup}=    Create Dictionary    username=dave    password=CorrectPass
    ${resp_signup}=    Post On Session    api    /signup    json=${signup}    expected_status=any
    Should Be Equal As Numbers    ${resp_signup.status_code}    200
    ${login}=    Create Dictionary    username=dave    password=WrongPass
    ${resp}=    Post On Session    api    /login    json=${login}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    401
    ${json}=    Set Variable    ${resp.json()}
    Dictionary Should Contain Key    ${json}    detail
    Should Be Equal    ${json['detail']}    Invalid credentials

Login - Missing Username
    ${login}=    Create Dictionary    password=NoUser
    ${resp}=    Post On Session    api    /login    json=${login}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    422

Login - Missing Password
    ${login}=    Create Dictionary    username=noPass
    ${resp}=    Post On Session    api    /login    json=${login}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    422

Login - Empty Username
    ${login}=    Create Dictionary    username=    password=SomePass
    ${resp}=    Post On Session    api    /login    json=${login}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    404

Login - Empty Password
    ${login}=    Create Dictionary    username=someuser    password=
    ${resp}=    Post On Session    api    /login    json=${login}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    401

Login - Invalid Types
    ${login}=    Create Dictionary    username=123    password=456
    ${resp}=    Post On Session    api    /login    json=${login}    expected_status=any
    Should Be Equal As Numbers    ${resp.status_code}    404

*** Keywords ***
Add
    [Arguments]    ${a}    ${b}
    ${result}=    Evaluate    ${a} + ${b}
    [Return]    ${result}

Subtract
    [Arguments]    ${a}    ${b}
    ${result}=    Evaluate    ${a} - ${b}
    [Return]    ${result}

Multiply
    [Arguments]    ${a}    ${b}
    ${result}=    Evaluate    ${a} * ${b}
    [Return]    ${result}

Divide
    [Arguments]    ${a}    ${b}
    ${result}=    Evaluate    (lambda a,b: a/b if b!=0 else (_ for _ in ()).throw(ValueError("cannot divide by zero")) )(${a}, ${b})
    [Return]    ${result}