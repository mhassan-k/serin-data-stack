{{ config(materialzied='view')}}

with lead_v as (select * from {{ref('flatten_leads')}})

SELECT
  DATE_TRUNC('month',ENTRYDATE) AS month,
  COALESCE(STATE,state_2) as STATE ,
  COUNT(*) AS leads_generated,
  COUNT(CASE WHEN ApptDate IS NOT NULL THEN 1 END) AS leads_converted_to_appointments,
  COUNT(CASE WHEN Demo = '1' THEN 1 END) AS leads_converted_to_demos,
  COUNT(CASE WHEN ApptDate IS NOT NULL THEN 1 END)::float / COUNT(*) * 100 AS appointment_conversion_rate,
  COUNT(CASE WHEN Demo = '1' THEN 1 END)::float / COUNT(*) * 100 AS demo_conversion_rate
FROM lead_v
WHERE STATE is not null or STATE != ''
GROUP BY
  1, 2
ORDER BY
  1, 2 DESC