```robot
*** Settings ***
Library  RequestsLibrary

*** Variables ***
${API_URL}  http://localhost:8001

*** Test Cases ***
Login User With Valid Credentials
    Create Session  api  ${API_URL}
    &{user}=  Create Dictionary  username=valid_user  password=valid_password
    ${resp}=  Post On Session  api /login  json=${user}  expected_status=any
    Should Be Equal As Strings  ${resp.status_code}  200

Login User With Invalid Credentials
    Create Session  api  ${API_URL}
    &{user}=  Create Dictionary  username=invalid_user  password=invalid_password
    ${resp}=  Post On Session  api /login  json=${user}  expected_status=any
    Should Be Equal As Strings  ${resp.status_code}  401

Signup User With Valid Credentials
    Create Session  api  ${API_URL}
    &{user}=  Create Dictionary  username=new_user  password=new_password
    ${resp}=  Post On Session  api /signup  json=${user}  expected_status=any
    Should Be Equal As Strings  ${resp.status_code}  200

Signup User With Existing Username
    Create Session  api  ${API_URL}
    &{user}=  Create Dictionary  username=new_user  password=new_password
    Post On Session  api /signup  json=${user}  expected_status=any
    Sleep  1s
    ${resp}=  Post On Session  api /signup  json=${user}  expected_status=any
    Should Be Equal As Strings  ${resp.status_code}  400

Signup User With Empty Username
    Create Session  api  ${API_URL}
    &{user}=  Create Dictionary  username=  password=new_password
    ${resp}=  Post On Session  api /signup  json=${user}  expected_status=any
    Should Be Equal As Strings  ${resp.status_code}  400

Signup User With Empty Password
    Create Session  api  ${API_URL}
    &{user}=  Create Dictionary  username=new_user  password=
    ${resp}=  Post On Session  api /signup  json=${user}  expected_status=any
    Should Be Equal As Strings  ${resp.status_code}  400

Login User With Empty Username
    Create Session  api  ${API_URL}
    &{user}=  Create Dictionary  username=  password=new_password
    ${resp}=  Post On Session  api /login  json=${user}  expected_status=any
    Should Be Equal As Strings  ${resp.status_code}  401

Login User With Empty Password
    Create Session  api  ${API_URL}
    &{user}=  Create Dictionary  username=new_user  password=
    ${resp}=  Post On Session  api /login  json=${user}  expected_status=any
    Should Be Equal As Strings  ${resp.status_code}  401

Login User With Invalid Username
    Create Session  api  ${API_URL}
    &{user}=  Create Dictionary  username=new_user  password=new_password
    ${resp}=  Post On Session  api /login  json=${user}  expected_status=any
    Should Be Equal As Strings  ${resp.status_code}  404

Login User With Invalid Password
    Create Session  api  ${API_URL}
    &{user}=  Create Dictionary  username=new_user  password=new_password
    Post On Session  api /login  json=${user}  expected_status=any
    Sleep  1s
    ${resp}=  Post On Session  api /login  json=${user}  expected_status=any
    Should Be Equal As Strings  ${resp.status_code}  401

```