INSERT INTO dossier_event
(id,
 dossier_id,
 creation_date,
 application_date,
 type,
 content,
 retries_left)
VALUES ('{id}',
        '{dossier_id}',
        '{now}',
        '{now}',
        '{type}',
        '{content}',
        3);
