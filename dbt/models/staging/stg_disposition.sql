with source as (

    select * from {{ source('raw', 'disposit_raw') }}

),

renamed as (

    select
        trial_id,
        subjid,
        eoip as discontinuation_reason,
        eoipcd as discontinuation_reason_code,
        eoipdy as discontinuation_day
    from source

)

select * from renamed