with source as (

    select * from {{ source('raw', 'a_eendpt_raw') }}

),

renamed as (

    select
        trial_id,
        subjid,
        pfscr = 1 as progressed_or_died,
        pfsdycr as event_or_censor_day
    from source

)

select * from renamed