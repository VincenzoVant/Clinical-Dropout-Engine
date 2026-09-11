with source as (

    select * from {{ source('raw', 'ae_raw') }}

),

renamed as (

    select
        trial_id,
        subjid,
        upper(trim(aesoc)) as soc_term,
        upper(trim(aept)) as pt_term,
        upper(trim(aehlgt)) as hlgt_term,
        upper(trim(aehlt)) as hlt_term,
        upper(trim(aellt)) as llt_term,
        meddra_v as meddra_version,
        aesev as severity,
        aesevcd as severity_grade,
        aerel as related_to_drug,
        aeser as serious,
        saelife as life_threatening,
        aestdy as start_day,
        aeendy as end_day,
        aedur as duration_days
    from source

)

select * from renamed