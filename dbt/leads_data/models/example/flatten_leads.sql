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
  TO_DATE(sftp."ENTRYDATE", 'MM-DD-YYYY') as ENTRYDATE,
  CAST(sftp."LEADNUMBER" as VARCHAR) as LEADNUMBER ,
  cast(sftp."email_hash" as VARCHAR) as email_hash ,
  cast(sftp."phone_hash" as VARCHAR) as phone_hash ,
  cast(sftp."CITY" as VARCHAR) as CITY ,
  CASE WHEN sftp."STATE" = '' THEN NULL
       WHEN sftp."STATE" = '  ' THEN NULL
       ELSE sftp."STATE" END AS STATE,
  cast(sftp."ZIP" as VARCHAR) as ZIP ,
  TO_TIMESTAMP(CASE WHEN sftp."ApptDate" = '' THEN NULL ELSE sftp."ApptDate" end ,'MM/DD/YYYY HH:MIAM') AS ApptDate,
  cast(sftp."Set"  as VARCHAR) as Set ,
  cast(sftp."Demo" as VARCHAR) as Demo,
  cast(sftp."Dispo" as VARCHAR) as Dispo,
  cast(sftp."JobStatus"  as VARCHAR) as JobStatus,
  cast(sftp."location" as VARCHAR) as location,
  TRIM(SPLIT_PART(sftp."location", '|', 2)) AS state_2,
  cast(parquet."lead_UUID" as VARCHAR ) AS lead_UUID,
  TO_TIMESTAMP(sftp."loaded_at", 'YYYY-MM-DD HH24:MI:SS') as loaded_at
FROM
    sftp_data sftp
left join parquet_data parquet ON sftp.email_hash = parquet.email_hash and sftp.phone_hash = parquet.phone_hash