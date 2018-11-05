Patients
======
`GET` request to `api/todays_tasks/`

`RESPONSE`

```json
[
    {
        "id": "1fb0ad5b-d1d4-...-3e0f4d138ebe",
        "type": "patient_task",
        "name": "Call Doctor",
        "state": "past due",
        "appear_datetime": "2018-09-11T15:00:00.435170Z",
        "due_datetime": "2018-09-11T23:00:00.435157Z"
    },
    {
        "id": "d1d4-3e0f4d138ebe-...-3e0f4d138ebe",
        "type": "assessment_task",
        "name": "Depression Assessment",
        "state": "available",
        "appear_datetime": "2018-09-11T15:00:00.435170Z",
        "due_datetime": "2018-09-11T23:00:00.435157Z"
    },
    ...
]
```

**NOTE** This list mixes multiple different models with similar fields, so to determine which model a task corresponds to, a `type` field is serialized onto the response.  You use `type` and `id` to get a task detail. 

- `id` - The id of the task object
- `type` - The type of the task (`patient_task`, `medication_task`, `symptom_task`, `assessment_task`, `vital_task`), used to determine how to retrieve the task detail object.
- `name` - This field is used to populate the list on the [Task List](https://app.zeplin.io/project/5b00bc9f763ac82b0f0bb30a/screen/5b0de50bf2dd81164e59fe12). 
 For medications this includes the dosage.
- `state` - Calculated on the backend to display the status of a task (missed, past due, available, done or upcoming)
- `appear_datetime` - The time that this task becomes "available".  If not past the available time this task will be an "upcoming"
- `due_datetime` - The time that this task becomes "past due" if not completed.

Employees
======
Not available at the moment