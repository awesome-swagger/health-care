# Mobile Backend Spec

- [Swagger Link](https://careadopt.izeni.net/swagger/)
- [Zeplin](https://app.zeplin.io/project/5b00bc9f763ac82b0f0bb30a/dashboard)

The sections in this document are organized the same as in the zeplin design.  The large headers are the sections, and the sub headers are the pages/modals in zeplin.

The pages are marked with the following labels:

![ready](https://i.imgur.com/Wpcnwbh.png)
![testing](https://i.imgur.com/3Fpm1Uk.png)
![issues](https://i.imgur.com/ZZe2kT1.png)
![postpone](https://i.imgur.com/AIpN6IE.png)
![needs info](https://i.imgur.com/XsxuR59.png)
![v2](https://i.imgur.com/cYwxDLp.png)

# Document Navigation

### Login

- [login__verify](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/(WIP)-Mobile-Backend-Spec#login__verify-)
- [login__createAccount](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/(WIP)-Mobile-Backend-Spec#login__createaccount-)
- [login](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/(WIP)-Mobile-Backend-Spec#login-)
- [login__forgotPassword](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/(WIP)-Mobile-Backend-Spec#login__forgotpassword-)

### Tasks

- [tasks](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/(WIP)-Mobile-Backend-Spec#tasks-)
- [tasks--done](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/(WIP)-Mobile-Backend-Spec#tasks-done-)
- [tasks__task](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/(WIP)-Mobile-Backend-Spec#tasks__task-)
- [tasks__med](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/(WIP)-Mobile-Backend-Spec#tasks__med-)
- [tasks__assmt](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/(WIP)-Mobile-Backend-Spec#tasks__assmt-)
- [tasks__symptoms](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/(WIP)-Mobile-Backend-Spec#tasks__symptoms-)
- [tasks__addSymptomModal](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/(WIP)-Mobile-Backend-Spec#tasks__addsymptommodal-)
- [tasks__vitals](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/(WIP)-Mobile-Backend-Spec#tasks__vitals-)

### Health

- [health](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/(WIP)-Mobile-Backend-Spec#health-)
- [health__careTeam](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/(WIP)-Mobile-Backend-Spec#health__careteam-)
- [health__education](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/(WIP)-Mobile-Backend-Spec#health__education-)
- [health__conditions](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/(WIP)-Mobile-Backend-Spec#health__conditions-)
- [health__meds](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/(WIP)-Mobile-Backend-Spec#health__meds-)
- [health__symptoms](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/(WIP)-Mobile-Backend-Spec#health__symptoms-)
- [health__vitals](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/(WIP)-Mobile-Backend-Spec#health__vitals-)

### Goals

- [goals](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/(WIP)-Mobile-Backend-Spec#goals-)
- [goals__goal](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/(WIP)-Mobile-Backend-Spec#goals__goal-)

### Messages

- [chat](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/(WIP)-Mobile-Backend-Spec#chat-)
- [chat__thread](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/(WIP)-Mobile-Backend-Spec#chat__thread-)

### Notifications

- [notifications](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/(WIP)-Mobile-Backend-Spec#notifications-)
- [notifications__taskAddedModal](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/(WIP)-Mobile-Backend-Spec#notifications__taskaddedmodal-)

### Settings

- [settings](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/(WIP)-Mobile-Backend-Spec#settings-)
- [settings__profile](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/(WIP)-Mobile-Backend-Spec#settings__profile-)
- [settings__editNameModal](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/(WIP)-Mobile-Backend-Spec#settings__editnamemodal-)
- [settings__editPhoneModal](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/(WIP)-Mobile-Backend-Spec#settings__editphonemodal-)
- [settings__editPhoneModal--code](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/(WIP)-Mobile-Backend-Spec#settings__editphonemodal-code-)
- [settings__editEmailModal](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/(WIP)-Mobile-Backend-Spec#settings__editemailmodal-)
- [settings__emailCode](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/(WIP)-Mobile-Backend-Spec#settings__emailcode-)
- [settings__notifications](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/(WIP)-Mobile-Backend-Spec#settings__notifications-)
- [settings__editPasswordModal](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/(WIP)-Mobile-Backend-Spec#settings__editpasswordmodal-)
- [settings__changeBackgroundModal](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/(WIP)-Mobile-Backend-Spec#settings__changebackgroundmodal-)


# LOGIN

## login__verify ![ready](https://i.imgur.com/Wpcnwbh.png)

  - When a patient profile is created they are sent an email containing a six digit verification code that they will enter into this screen.
  - The request for this page will return the auth token, users name, and users, email.
  - Example request for this screen:

`POST` TO `/api/patient_profiles/verification/`
``` javascript
{
    "email": "patient@example.com",
    "code": "123abc"
}
```
  - Example response:

``` javascript
{
  "id": "182a449d-5871-41fa-ae99-24d61aba25e7", // Patient Profile ID
  "user": {
    "id": "39c8deae-045f-4d48-a68e-fd375be04c3e", // User ID
    "email": "jprice@izeni.com",
    "first_name": "Jordan",
    "last_name": "Price",
    "token": "6fda17d66f0f3d7210aae6cc11b169d540e55ab7" // Authentication token
  }
}
```

[Back To Top](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/(WIP)-Mobile-Backend-Spec#document-navigation)

## login__createAccount ![ready](https://i.imgur.com/Wpcnwbh.png)
  - Can either use two text fields, or send the same password for both new_password1 and new_password2

  - Example Request:

`POST` TO `/api/patient_profiles/create_account/`
``` javascript
{
    "preferred_name": "John",
    "new_password1": "john-password",
    "new_password2": "john-password"
}
```

  - Example Response:

```
{
  "detail": "Successfully created a patient account."
}
```

[Back To Top](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/(WIP)-Mobile-Backend-Spec#document-navigation)

## login ![img](https://i.imgur.com/Wpcnwbh.png)

  - See the [Authentication Wiki Page](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/Authentication) for a detail explanation of the authentication process.

[Back To Top](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/(WIP)-Mobile-Backend-Spec#document-navigation)

## login__forgotPassword ![ready](https://i.imgur.com/Wpcnwbh.png)

  - Post `email` to `/rest-auth/password/reset/`

  - Example request for this screen:

`POST` TO `/api/patient_profiles/verification/`
``` javascript
{
    "email": "patient@example.com",
}
```
  - A successful response to this endpoint will send an email to the user containing a link to reset their password in their browser.

[Back To Top](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/(WIP)-Mobile-Backend-Spec#document-navigation)

## login__code and login__resetPassword

  - These pages will no longer be included, as the password reset link will be sent to the user and will happen within their browser.

[Back To Top](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/(WIP)-Mobile-Backend-Spec#document-navigation)

# TASKS

## tasks ![img](https://i.imgur.com/Wpcnwbh.png)

  - See the [Todays Tasks Wiki Page](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/Listing-All-Tasks-For-Today) for detailed instruction on the endpoints for this page.

[Back To Top](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/(WIP)-Mobile-Backend-Spec#document-navigation)

## tasks--done ![img](https://i.imgur.com/Wpcnwbh.png)

  - For version one we've decided to simplify the message streams a little bit.  We will no longer be tracking "helpful/not helpful".
  - There is a `message_for_day` object serialized on the patient profile.  This is automatically updated every day, this is the message that will be shown on this page.

``` json
Patient Profile
...
"message_for_day": {
    "id": "68483b33-9144-417f-ac1d-4b3b67824c74",
    "queue": "26a37478-a601-4a24-9006-e00501cd0565",
    "text": "It mostly comes at night... mostly"
}
...
```

[Back To Top](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/(WIP)-Mobile-Backend-Spec#document-navigation)

## tasks__task ![img](https://i.imgur.com/Wpcnwbh.png)

  - Will get here by clicking a task of type `patient_task` on the tasks dashboard.

#### Getting Task

`GET` TO `/api/patient_tasks/<task_id>/`

`RESPONSE`

``` json
{
    "id": "8440467e-2c66-...-9ea093e3275d",
    "plan": "18304849-b27c-...-172c8ca44e27",
    "patient_task_template": {
        "id": "7a5e299d-1d7d-...-39cb18cd23b4",
        "start_on_day": 0,
        "frequency": "every_other_day",
        "repeat_amount": -1,
        "appear_time": "09:00:00",
        "due_time": "17:00:00",
        "name": "Eat Food",
        "plan_template": "d2006ad0-9df9-...-e2b74801240a"
    },
    "appear_datetime": "2018-10-05T03:00:00-06:00",
    "due_datetime": "2018-10-05T11:00:00-06:00",
    "status": "undefined",
    "is_complete": false,
    "state": "past due"
}
```

#### Marking Complete

  - Send a patch request with the `status` field. `done`, `missed`, and `undefined` are valid choices.
  - The task will automatically be marked complete when the status is either done or missed.

`PATCH` TO `/api/patient_tasks/<task_id>/`
``` json
{
    "status": "done"
}
```

`RESPONSE` - The updated patient task object.

[Back To Top](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/(WIP)-Mobile-Backend-Spec#document-navigation)

## tasks__med ![img](https://i.imgur.com/Wpcnwbh.png)

  - Will get here by clicking a task of type `medication_task` on the tasks dashboard.

#### Getting Task

`GET` TO `/api/medication_tasks/<task_id>/`

`RESPONSE`

``` json
{
    "id": "5f6c6b4c-7c0a...86-c98b31a651fa",
    "medication_task_template": {
        "id": "bb63e9e3-18...9-79b0cb7ae30e",
        "start_on_day": 0,
        "frequency": "daily",
        "repeat_amount": -1,
        "appear_time": "09:00:00",
        "due_time": "17:00:00",
        "plan": "18304849-b27c...-172c8ca44e27",
        "patient_medication": {
            "id": "291ba428-32d7-...-7aa3e8e62ad2",
            "patient": "41803bc8-b531-4...-e5443a71ded5",
            "medication": {
                "id": "ef324945-c2ac-...-7f6ac574b8c3",
                "name": "Zoloft",
                "rx_code": "901290"
            },
            "dose_mg": 10,
            "date_prescribed": "2018-08-09",
            "duration_days": 60,
            "instructions": "Take with food.",
            "prescribing_practitioner": {
                "id": "08e12b3f-7a09-...-9472289f1613",
                "user": ...,
                "title": ...
            }
        }
    },
    "appear_datetime": "2018-10-08T09:00:00-06:00",
    "due_datetime": "2018-10-08T17:00:00-06:00",
    "status": "done",
    "is_complete": true,
    "state": "done"
}
```

#### Marking Complete

  - Send a patch request with the `status` field. `done`, `missed`, and `undefined` are valid choices.
  - The task will automatically be marked complete when the status is either done or missed.

`PATCH` TO `/api/medication_tasks/<task_id>/`
``` json
{
    "status": "done"
}
```

[Back To Top](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/(WIP)-Mobile-Backend-Spec#document-navigation)

## tasks__assmt ![img](https://i.imgur.com/Wpcnwbh.png)

  - Will get here by clicking a task of type `assessment_task` on the tasks dashboard.

#### Getting Task

  - On assessment tasks, the template (with questions) and responses are all serialized onto the assessment task for ease of use.

`GET` TO `/api/assessment_tasks/<task_id>/`

`RESPONSE`

``` json
{
    "id": "7189be83-0a0b...e7-9f9040366933",
    "plan": "18304849-...2-172c8ca44e27",
    "assessment_task_template": {
        "id": "6d146e2f-2889-4a8c-...1100c30accc",
        "plan_template": "d2006ad0-...b74801240a",
        "name": "Outcome Assessment",
        "tracks_outcome": true,
        "tracks_satisfaction": false,
        "start_on_day": 0,
        "frequency": "weekly",
        "repeat_amount": -1,
        "appear_time": "09:00:00",
        "due_time": "17:00:00",
        "questions": [
            {
                "id": "055fb570-f0...a830-25c81387d935",
                "prompt": "Question two",
                "worst_label": "Worst",
                "best_label": "Best",
                "assessment_task_template": "6d146..9-4a8c-bda6-c1100c30accc"
            },
            {
                "id": "14c0a2a5-9cc1-4...cd-11b1a7284329",
                "prompt": "Question one",
                "worst_label": "Worst",
                "best_label": "Best",
                "assessment_task_template": "6d146e2f-2889-4...a6-c1100c30accc"
            }
        ]
    },
    "appear_datetime": "2018-10-05T03:00:00-06:00",
    "due_datetime": "2018-10-05T11:00:00-06:00",
    "comments": null,
    "is_complete": true,
    "state": "done",
    "responses": [
        {
            "id": "98d7e098-3b0...f9-9c00ceb6bbb2",
            "rating": 5,
            "assessment_task": "7189be83-0a0b-...4e7-9f9040366933",
            "assessment_question": "055fb570-f0...830-25c81387d935"
        },
        {
            "id": "ac854e6f-9ded...2-68695e5c8d7d",
            "rating": 3,
            "assessment_task": "7189be83-0a0...94e7-9f9040366933",
            "assessment_question": "14c0a2a5-9...-b5cd-11b1a7284329"
        }
    ]
}
```

#### Submitting Responses

  - The done button should be disabled until a response can be created for each question.
  - Clicking the done button should bulk create assessment responses by posting an array of responses to the `assessment_responses` endpoint.
  - The assessment task is automatically marked complete when there is a response for each question.

`POST` TO `/api/assessment_responses/`
``` json
[
    {
        "rating": 5,
        "assessment_task": "7189be83-0a0b-....7-9f9040366933",
        "assessment_question": "055fb570-f....30-25c81387d935"
    },
    {
        "rating": 3,
        "assessment_task": "7189be83-0a0b-4....4e7-9f9040366933",
        "assessment_question": "14c0a2a5-9cc....f-b5cd-11b1a7284329"
    }
]
```

`RESPONSE`

``` json
[
    {
        "id": "59977ef8-d7db-4b42-9350-a8f972fbc68a",
        "rating": 4,
        "assessment_task": "31609629-d9b2-40f7-8ab8-f89977bf8712",
        "assessment_question": "055fb570-f085-491d-a830-25c81387d935"
    }, 
    {
        "id": "bf028c73-f769-4f2e-8084-23e570526411",
        "rating": 4,
        "assessment_task": "31609629-d9b2-40f7-8ab8-f89977bf8712",
        "assessment_question": "14c0a2a5-9cc1-48ef-b5cd-11b1a7284329"
    }
]
```

[Back To Top](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/(WIP)-Mobile-Backend-Spec#document-navigation)

## tasks__symptoms ![img](https://i.imgur.com/Wpcnwbh.png)

  - Will get here by clicking a task of type `symptom_task` on the tasks dashboard.
  - Will grab the task instance from the `/api/symptom_tasks/` endpoint.
  - Ratings are automatically serialized onto the symptom task.
  - A symptom task is marked complete if there is at least one symptom reported.
  - Because a user will be reporting them one at a time, there is no need for bulk
    creating ratings in a single request.  It will be sufficient to make a request for
    each rating here.
  - In the designs it says that it will list all symptoms previously reported in the past
    but we're no longer doing that.  Instead, when they arrive at a symptom report it will
    be blank.  A user will then click the "Report Symptom" button.  They have to report
    at least one symptom before they can hit done.

[Back To Top](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/(WIP)-Mobile-Backend-Spec#document-navigation)

## tasks__addSymptomModal ![ready](https://i.imgur.com/Wpcnwbh.png)

  - GET request to `/api/symptoms/search/` with `q` in the request payload will return symptoms that match any fields with the search string.
  - Should only be hit with 3 or more characters to reduce the risk of returning thousands of entries.

[Back To Top](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/(WIP)-Mobile-Backend-Spec#document-navigation)

## tasks__vitals ![ready](https://i.imgur.com/Wpcnwbh.png)

  - Will get here by clicking a task of type `vital_task` on the tasks dashboard.
  - Will grab the task instance from the `/api/vital_tasks/` endpoint.
  - The done button should be disabled until a response can be created for each question.
  - Clicking the done button should bulk create vital responses by posting an array of responses to the `/api/vital_responses/` endpoint.
  - The vital task is automatically marked complete when there is a response with the correct type for each question.

[Back To Top](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/(WIP)-Mobile-Backend-Spec#document-navigation)

# PROGRESS

## progress ![testing](https://i.imgur.com/3Fpm1Uk.png)

  - The `/api/patient_profiles/dashboard/` endpoint should return all the data needed for the patient dashboard in a single request.
  - Nothing on this page needs to be interactive so it should be pretty straight forward.

[Back To Top](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/(WIP)-Mobile-Backend-Spec#document-navigation)


# HEALTH

## health ![ready](https://i.imgur.com/Wpcnwbh.png)

  - Currently it would take several requests to show the counts for each section on this page.  Lets leave the counts out for now, and come back to them later if they are truly needed.
  - This should not require any data or hitting any endpoints.

[Back To Top](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/(WIP)-Mobile-Backend-Spec#document-navigation)

## health__careTeam ![img](https://i.imgur.com/Wpcnwbh.png)

  - The `/api/care_team_members/` endpoint should return all the of the data needed for this page.
  - Remove "Organization" and "Location" from the care team members on this page, since it doesn't really make sense what to show there.

[Back To Top](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/(WIP)-Mobile-Backend-Spec#document-navigation)

## health__education ![img](https://i.imgur.com/Wpcnwbh.png)

  - We are no longer tracking if message is has been read, or if it is helpful/not helpful.
  - After the above ticket is resolved, `/api/info_message_queues/` should return all the data necessary for this page.

[Back To Top](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/(WIP)-Mobile-Backend-Spec#document-navigation)

## health__conditions ![ready](https://i.imgur.com/Wpcnwbh.png)

  - The `/api/patient_diagnosis/` endpoint should return everything on this page.
  - Where it shows "organization" show facility instead.

[Back To Top](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/(WIP)-Mobile-Backend-Spec#document-navigation)

## health__meds ![ready](https://i.imgur.com/Wpcnwbh.png)

  - The `/api/patient_medications/` endpoint should return everything on this page.

[Back To Top](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/(WIP)-Mobile-Backend-Spec#document-navigation)

## health__symptoms ![ready](https://i.imgur.com/Wpcnwbh.png)

  - List all unique symptoms and their latest rating.
  - The `/api/patient_profiles/<patient_id>/latest_symptoms/` should return all the data necessary for this page.
  - The `behavior` field is a string containing either `increasing`, `decreasing`, or `equal` compared to the previous time this symptom has been shown.  This field is what is used to show the arrow next to each symptom on this page.

`GET` TO `/api/patient_profiles/<patient_id>/latest_symptoms/`

`RESPONSE`

``` json
[
  {
    "id": "8059e994-ff87-....-549bc7bd9d9e",
    "symptom": {
      "id": "adae6691-7ab....0-d07494f6020e",
      "name": "Fatigue",
      "worst_label": "Very Fatigued",
      "best_label": "No Fatigue"
    },
    "rating": 3,
    "behavior": "increasing",
    "created": "2018-10-24T16:32:18.422153-06:00",
    "modified": "2018-10-24T16:32:18.422169-06:00"
  },
  {
    "id": "be40505b-78a1....-2ccd9d539bb7",
    "symptom": {
      "id": "fd4b6e17-....-e6b94dfe094b",
      "name": "Pain",
      "worst_label": "Very Painful",
      "best_label": "No Pain"
    },
    "rating": 1,
    "behavior": "decreasing",
    "created": "2018-10-24T16:32:18.424094-06:00",
    "modified": "2018-10-24T16:32:18.424109-06:00"
  }
]
```

[Back To Top](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/(WIP)-Mobile-Backend-Spec#document-navigation)

## health__vitals ![ready](https://i.imgur.com/Wpcnwbh.png)

  - List vitals that have been reported, and their results.
  - Similar to the `health__symptoms` page, we will not be showing just the latest results of each
    unique vital task, but a flat list of all the vital tasks that have been reported.
  - The `/api/vital_tasks/` endpoint will return all the data necessary for this page.

[Back To Top](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/(WIP)-Mobile-Backend-Spec#document-navigation)


# GOALS

## goals ![ready](https://i.imgur.com/Wpcnwbh.png)

  - The `/api/patients_profiles/{id}/care_plan_goals/` endpoint should return all the data necessary for this page.

[Back To Top](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/(WIP)-Mobile-Backend-Spec#document-navigation)

## goals__goal ![ready](https://i.imgur.com/Wpcnwbh.png)

  - The `/api/goals/` endpoint will return everything needed to display the goal, progress, and comment chain.
  - The `/api/goal_comments/` endpoint will be used to post a comment to a goal.

#### Submitting Comments

  - Goal comments can be made by employees or patients, so it is tied to a **User** id rather than a patient or employee id.  The comment response serializes whether or not it is from a patient or an employee.
  - The user id can be accessed from the patient profile response (`patient.user.id` etc.)

`POST` TO `/api/goal_comments/`
``` json
{
  "goal": "b4dc138b-e043-...-d064d84c1edb", // Goal id
  "user": "4c5688b2-6647-4255-9a77-31122df3497a", // **USER** id
  "content": "here is a comment from swagger" // Message content
}
```

`RESPONSE`

``` json
{
  "id": "eedcdd16-a476-4...1-aa387549ff1d",
  "goal": "b4dc138b-e043...63-d064d84c1edb",
  "user": {
    "id": "3112asdf497a-42....-6647-2df34311297a",
    "first_name": "Patient",
    "last_name": "Guy",
    "image_url": "/media/users/jprice%40izeni.com/profile.png",
    "user_type": "patient",
    "title": ""
  },
  "content": "here is a comment from swagger",
  "created": "2018-10-23T12:52:30.923915-06:00",
  "modified": "2018-10-23T12:52:30.923953-06:00"
}
```

[Back To Top](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/(WIP)-Mobile-Backend-Spec#document-navigation)


# MESSAGES

## chat ![postpone](https://i.imgur.com/AIpN6IE.png)

  Waiting on firebase implementation

[Back To Top](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/(WIP)-Mobile-Backend-Spec#document-navigation)

## chat__thread ![postpone](https://i.imgur.com/AIpN6IE.png)

  Waiting on firebase implementation

[Back To Top](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/(WIP)-Mobile-Backend-Spec#document-navigation)


# NOTIFICATIONS

## notifications ![postpone](https://i.imgur.com/AIpN6IE.png)

  Waiting on firebase implementation

[Back To Top](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/(WIP)-Mobile-Backend-Spec#document-navigation)

## notifications__taskAddedModal ![postpone](https://i.imgur.com/AIpN6IE.png)

  Waiting on firebase implementation

[Back To Top](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/(WIP)-Mobile-Backend-Spec#document-navigation)


# SETTINGS

## settings ![ready](https://i.imgur.com/Wpcnwbh.png)

  - No data necessary from backend for this page.

[Back To Top](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/(WIP)-Mobile-Backend-Spec#document-navigation)

## settings__profile ![ready](https://i.imgur.com/Wpcnwbh.png)

  - All data on this page is on the `/api/patient_profiles/` response.
  - Currently we don't have the `insurance` field.
  - There is a specific endpoint for updating a user's profile image.  `TODO`: Verify which endpoint this is.

[Back To Top](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/(WIP)-Mobile-Backend-Spec#document-navigation)

## settings__editNameModal ![ready](https://i.imgur.com/Wpcnwbh.png)

  - Patch request to `/api/users/<user_id>` containing the `preferred_name` field.  Note that the id is the user id, not the patient profile id.

[Back To Top](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/(WIP)-Mobile-Backend-Spec#document-navigation)

## settings__editPhoneModal ![skip](https://i.imgur.com/cYwxDLp.png)

  - SKIP FOR V1

[Back To Top](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/(WIP)-Mobile-Backend-Spec#document-navigation)

## settings__editPhoneModal--code ![skip](https://i.imgur.com/cYwxDLp.png)

  - SKIP FOR V1

[Back To Top](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/(WIP)-Mobile-Backend-Spec#document-navigation)

## settings__editEmailModal ![skip](https://i.imgur.com/cYwxDLp.png)

  - SKIP FOR V1

[Back To Top](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/(WIP)-Mobile-Backend-Spec#document-navigation)

## settings__emailCode ![skip](https://i.imgur.com/cYwxDLp.png)

  - SKIP FOR V1

[Back To Top](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/(WIP)-Mobile-Backend-Spec#document-navigation)

## settings__notifications ![postpone](https://i.imgur.com/AIpN6IE.png)

  - Waiting on firebase and notifications implementation

[Back To Top](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/(WIP)-Mobile-Backend-Spec#document-navigation)

## settings__editPasswordModal ![ready](https://i.imgur.com/Wpcnwbh.png)

  - POST `old_password`, `new_password1` and `new_password2` to `/rest-auth/password/change/`.

[Back To Top](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/(WIP)-Mobile-Backend-Spec#document-navigation)

## settings__changeBackgroundModal ![ready](https://i.imgur.com/Wpcnwbh.png)

  - This should not require any endpoints.  The app should have the images statically, and
    keep track of the user's selection in whatever persistent storage options available.

[Back To Top](https://dev.izeni.net/care-adopt/care-adopt-backend/wikis/(WIP)-Mobile-Backend-Spec#document-navigation)
