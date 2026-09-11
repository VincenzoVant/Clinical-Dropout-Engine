
  create view "postgres"."public"."stg_demo__dbt_tmp"
    
    
  as (
    with source as (

    select * from "postgres"."raw"."demo_raw"

),

renamed as (

    select
        trial_id,
        age,
        sex,
        raccat as race_category,
        b_ecogi as ecog_baseline,
        diagtype as diagnosis_type,
        b_weight as weight_kg,
        b_height as height_cm,
        b_bsa as bsa_m2,
        kras as kras_status,
        trt ilike '%panit%' as on_panitumumab
    from source

)

select * from renamed
  );