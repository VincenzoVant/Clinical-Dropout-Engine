with source as (

    select * from {{ source('raw', 'disposit_raw') }}

),

renamed as (

    select
        trial_id,
        subjid,
        eoip as discontinuation_reason,
        eoipcd as discontinuation_reason_code
    from source

)

select * from renamed