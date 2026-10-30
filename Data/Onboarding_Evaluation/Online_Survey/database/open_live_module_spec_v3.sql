-- Open formal recruitment for module-spec-v3 after the schema update.
-- Does not delete responses or change assignment counters.
begin;
do $$
begin
  if not exists (select 1 from public.survey_study_settings where study='module-spec-v3' and mode='live') then
    raise exception 'Run setup_module_spec_v3.sql before opening formal recruitment';
  end if;
end;
$$;
update public.survey_settings set accepting=true where mode='live';
update public.survey_study_settings set accepting=true where study='module-spec-v3' and mode='live';
commit;
select study,mode,accepting from public.survey_study_settings where study='module-spec-v3' and mode='live';
