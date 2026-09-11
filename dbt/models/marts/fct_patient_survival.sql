with demo as (

    select * from {{ ref('stg_demo') }}

),

disposition as (

    select * from {{ ref('stg_disposition') }}

),

progression as (

    select * from {{ ref('stg_progression') }}

),

joined as (

    select
        demo.trial_id,
        demo.subjid,
        demo.age,
        demo.sex,
        demo.race_category,
        demo.ecog_baseline,
        demo.diagnosis_type,
        demo.weight_kg,
        demo.height_cm,
        demo.bsa_m2,
        demo.kras_status,
        demo.on_panitumumab,
        disposition.discontinuation_reason,
        disposition.discontinuation_reason_code,
        disposition.discontinuation_day,
        progression.progressed_or_died as event,
        progression.event_or_censor_day as time_days
    from demo
    inner join disposition
        on demo.trial_id = disposition.trial_id
        and demo.subjid = disposition.subjid
    inner join progression
        on demo.trial_id = progression.trial_id
        and demo.subjid = progression.subjid

)

select * from joined