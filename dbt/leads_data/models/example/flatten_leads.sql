-- model: flatten_tables
{{ config(
    materialized='table',
) }}

WITH sftp_data AS (
    SELECT
    "ENTRYDATE" ,
    "LEADNUMBER" ,
    email_hash ,
    phone_hash ,
    "CITY" ,
    "STATE" ,
    "ZIP" ,
    "ApptDate" ,
    "Set" ,
    "Demo" ,
    "Dispo" ,
    "JobStatus" ,
    "location",
    loaded_at
    FROM
        public.leads_sftp
),

parquet_data AS (
    SELECT
        "lead_UUID",
        phone_hash,
        email_hash
    FROM
        public.leads_parquet
)

SELECT
    sftp."ENTRYDATE" ,
    sftp."LEADNUMBER" ,
    sftp.email_hash ,
    sftp.phone_hash ,
    sftp."CITY" ,
    sftp."STATE" ,
    sftp."ZIP" ,
    sftp."ApptDate" ,
    sftp."Set" ,
    sftp."Demo" ,
    sftp."Dispo" ,
    sftp."JobStatus" ,
    sftp."location" ,
    parquet."lead_UUID",
    sftp.loaded_at
FROM
    sftp_data sftp
left join parquet_data parquet ON sftp.email_hash = parquet.email_hash and sftp.phone_hash = parquet.phone_hash