select *
from {{ ref('fct_patient_survival') }}
where time_days < 0