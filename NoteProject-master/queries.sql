SELECT Date,Title,Contents,TaskState.State AS State, U1.Login AS Creator, U2.Login AS User
FROM Tasks
JOIN TaskState ON Tasks.StateID = TaskState.ID
JOIN Users U1 ON Tasks.CreatorID = U1.ID
JOIN Users U2 ON Tasks.UserID = U2.ID