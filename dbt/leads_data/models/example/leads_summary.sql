{{ config(materialzied='view')}}

with lead_v as (select * from {{ref('flatten_leads')}})

SELECT
  DATE_TRUNC('month', TO_DATE("ENTRYDATE", 'MM-DD-YYYY')) AS month,
  "STATE",
  COUNT(*) AS leads_generated,
  SUM(CASE WHEN "ApptDate" IS NOT NULL THEN 1 END) AS leads_converted_to_appointments,
  SUM(CASE WHEN "Demo" IS NOT NULL THEN 1 END) AS leads_converted_to_demos
FROM lead_v
GROUP BY
  1, 2