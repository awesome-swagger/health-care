The API uses tokens to determine the authenticated user.  To hit most endpoints in the app you need to be authenticated with a valid token.

Creating/Retrieving A Token
=======
`POST` to `/api-token-auth/`

```json
{
  "username": USERNAME,
  "password": PASSWORD
}
```
`RESPONSE`

```json
{
  "token":"3418be61de....cc177120d6d8",
  "employee_profile":"68523cec-.....3fb0c8de",
  "patient_profile":"68523cec-.....3fb0c8de"
}
```

- `token` - This is what you'll use to authenticate all further requests.  You'll need to save this token and add it as a header to all further requests.  The authorization header is accepted in this format:

  - `Authorization: Token 3418be61de....cc177120d6d8`

- `employee_profile` and `patient_profile` will only be returned if the user authenticating has either one.  It is possible for a user to have both, but it will be one or the other in most cases.  If you are authenticating through the mobile app you'll likely be using a `patient_profile`, and if you're authenticating through the web app you'll likely be using a `employee_profile`.
  - With these ids you can then get your patient or employee profile object by posting a GET request to `api/patient_profiles/<patient_profile>` or `api/employee_profiles/<employee_profile>/` respectively.