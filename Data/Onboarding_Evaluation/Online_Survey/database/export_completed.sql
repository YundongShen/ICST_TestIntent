-- Run as the researcher in the Supabase SQL Editor.
select *
from public.survey_export
where study = 'module-spec-v3'
  and mode = 'live'
  and submitted_at is not null
  and condition in ('A', 'B', 'C')
order by submitted_at;
