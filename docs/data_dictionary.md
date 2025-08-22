# TutorMatch Data Dictionary

## Table: user_profiles

| Field Name          | Data Type | Description                          | Constraints                  |
|---------------------|-----------|--------------------------------------|------------------------------|
| id                  | INTEGER   | Unique identifier for teacher        | PRIMARY KEY, AUTOINCREMENT  |
| name                | TEXT      | Full name of teacher                 | NOT NULL                     |
| profile_picture     | TEXT      | Path to profile picture              |                              |
| subjects            | TEXT      | Subjects taught by teacher          | NOT NULL                     |
| hourly_rate         | REAL      | Teacher's hourly rate               | NOT NULL                     |
| qualifications      | TEXT      | Teacher's qualifications            |                              |
| school              | TEXT      | Teacher's school/university         |                              |
| email               | TEXT      | Teacher's email address              | NOT NULL, UNIQUE            |
