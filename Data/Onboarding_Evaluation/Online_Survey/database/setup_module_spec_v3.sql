-- module-spec-v3 update: run this complete file in a NEW Supabase SQL Editor query.
-- Keeps all earlier answers and counters. Re-running does not reset assignments.
-- Test mode is open. Live recruitment remains closed until the pilot is approved.
begin;

create schema if not exists survey_private;
revoke all on schema survey_private from public, anon, authenticated;

create table if not exists public.survey_settings (
  mode text primary key check (mode in ('test', 'live')),
  accepting boolean not null default false
);
insert into public.survey_settings values ('test', true), ('live', false)
on conflict (mode) do nothing;

create table if not exists public.survey_allocation (
  mode text not null references public.survey_settings(mode),
  study text not null default 'dog-test-v1',
  assigned_count bigint not null default 0,
  current_order text[] not null default array['A','B','C'],
  primary key (mode, study)
);
-- Preserve the previous study's counters. New materials have separate counters.
alter table public.survey_allocation add column if not exists study text not null default 'dog-test-v1';
alter table public.survey_allocation drop constraint if exists survey_allocation_pkey;
alter table public.survey_allocation add primary key (mode, study);
insert into public.survey_allocation(mode, study)
values ('test', 'module-spec-v3'), ('live', 'module-spec-v3')
on conflict (mode, study) do nothing;

-- Study-specific recruitment is independent of previous questionnaire versions.
create table if not exists public.survey_study_settings (
  study text not null, mode text not null references public.survey_settings(mode),
  accepting boolean not null default false, primary key(study,mode)
);
insert into public.survey_study_settings(study,mode,accepting)
values ('module-spec-v3','test',true), ('module-spec-v3','live',false)
on conflict(study,mode) do nothing;
alter table public.survey_study_settings enable row level security;
revoke all on public.survey_study_settings from public,anon,authenticated;

create table if not exists public.survey_responses (
  participant_id uuid primary key,
  token_hash bytea not null,
  study text not null default 'module-spec-v3',
  suite text not null default 'module.spec',
  mode text not null references public.survey_settings(mode),
  condition text check (condition in ('A','B','C')),
  block_number bigint,
  block_position integer check (block_position between 1 and 3),
  state jsonb,
  revision bigint not null default 0,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  assigned_at timestamptz,
  submitted_at timestamptz,
  constraint survey_response_assignment_key unique(study, mode, block_number, block_position)
);
-- Defaults affect new sessions only. Existing answers are not relabelled.
alter table public.survey_responses alter column study set default 'module-spec-v3';
alter table public.survey_responses alter column suite set default 'module.spec';
alter table public.survey_responses drop constraint if exists survey_responses_mode_block_number_block_position_key;
alter table public.survey_responses drop constraint if exists survey_response_assignment_key;
alter table public.survey_responses add constraint survey_response_assignment_key
  unique(study, mode, block_number, block_position);

alter table public.survey_settings enable row level security;
alter table public.survey_allocation enable row level security;
alter table public.survey_responses enable row level security;
-- No participant gets direct access to these tables, even with the public key.
revoke all on public.survey_settings, public.survey_allocation,
  public.survey_responses from public, anon, authenticated;

create or replace function survey_private.snapshot(r public.survey_responses)
returns jsonb language sql set search_path = '' as $$
  select jsonb_build_object(
    'participant_id', r.participant_id, 'condition', r.condition,
    'state', r.state, 'revision', r.revision,
    'submitted_at', r.submitted_at, 'mode', r.mode,
    'study', r.study, 'suite', r.suite
  );
$$;

create or replace function survey_private.check_token(p_token text)
returns void language plpgsql set search_path = '' as $$
begin
  if p_token is null or p_token !~ '^[0-9a-f]{64}$' then
    raise exception 'Invalid session token';
  end if;
end;
$$;

create or replace function survey_private.validate_state(s jsonb, complete_bg boolean, complete_all boolean)
returns void language plpgsql set search_path = '' as $$
declare
  k text; g text; v jsonb; n integer;
begin
  if s is null or jsonb_typeof(s) <> 'object' or octet_length(s::text) > 50000 then
    raise exception 'Invalid answer data';
  end if;
  if coalesce(s->>'step','') !~ '^[0-5]$' or coalesce(s->>'maxStep','') !~ '^[0-5]$' then
    raise exception 'Invalid survey step';
  end if;
  if (s->>'step')::integer > (s->>'maxStep')::integer then
    raise exception 'Invalid survey progress';
  end if;
  if jsonb_typeof(s->'bg03') is distinct from 'object' then
    raise exception 'Invalid background answers';
  end if;
  if jsonb_typeof(s->'bg01') is distinct from 'array'
    or jsonb_typeof(s->'bg02') is distinct from 'string'
    or jsonb_typeof(s->'bg01_other') is distinct from 'string'
    or length(s->>'bg01_other') > 2000 then
    raise exception 'Invalid background text';
  end if;
  if jsonb_array_length(s->'bg01') > 4 or exists (
    select 1 from jsonb_array_elements(s->'bg01') as role(value)
    where jsonb_typeof(value) is distinct from 'string'
      or value #>> '{}' not in ('Software developer / engineer','Software test / QA engineer','Researcher / academic','Other')
  ) or jsonb_array_length(s->'bg01') <> (select count(distinct value) from jsonb_array_elements(s->'bg01')) then
    raise exception 'Invalid role selection';
  end if;
  if s->>'bg02' not in ('','I am still learning about testing as part of my education',
      'Less than 1 year','1 to less than 3 years','3 to less than 6 years',
      '6 to less than 9 years','9 years or more') then
    raise exception 'Invalid background choice';
  end if;
  if complete_bg and (jsonb_array_length(s->'bg01') = 0 or s->>'bg02' = ''
    or ((s->'bg01' ? 'Other') and btrim(s->>'bg01_other') = '')) then
    raise exception 'Background answers are incomplete';
  end if;
  foreach k in array array['language','playwright','dom','css'] loop
    v := s->'bg03'->k;
    if v is not null and (jsonb_typeof(v) <> 'number' or v::text !~ '^[1-5]$') then
      raise exception 'Invalid familiarity rating';
    end if;
    if complete_bg and v is null then raise exception 'Background ratings are incomplete'; end if;
  end loop;
  if jsonb_typeof(s->'cq') is distinct from 'object' then
    raise exception 'Invalid comprehension answers';
  end if;
  v := s->'cq'->'cq1';
  if v is not null and (jsonb_typeof(v) is distinct from 'string'
    or s->'cq'->>'cq1' not in ('2', '5', '6', '7', 'Can''t tell from the material')) then
    raise exception 'Invalid comprehension choice: cq1';
  end if;
  if complete_all and v is null then raise exception 'Comprehension answers are incomplete'; end if;
  v := s->'cq'->'cq2';
  if v is not null and (jsonb_typeof(v) is distinct from 'string'
    or s->'cq'->>'cq2' not in ('It is visible immediately and stays visible', 'It is hidden at first and then becomes visible', 'It is visible at first and then becomes hidden', 'Can''t tell from the material')) then
    raise exception 'Invalid comprehension choice: cq2';
  end if;
  if complete_all and v is null then raise exception 'Comprehension answers are incomplete'; end if;
  v := s->'cq'->'cq3';
  if v is not null and (jsonb_typeof(v) is distinct from 'string'
    or s->'cq'->>'cq3' not in ('Yes, at least one test would fail', 'No, all tests would still pass', 'Can''t tell from the material')) then
    raise exception 'Invalid comprehension choice: cq3';
  end if;
  if complete_all and v is null then raise exception 'Comprehension answers are incomplete'; end if;
  if s->'cq' ? 'cq3_why' and (jsonb_typeof(s->'cq'->'cq3_why') is distinct from 'string'
    or length(s->'cq'->>'cq3_why') > 4000) then
    raise exception 'Invalid comprehension explanation';
  end if;
  foreach g in array array['g1','g2'] loop
    if jsonb_typeof(s->g) is distinct from 'object'
      or jsonb_typeof(s->g->'items') is distinct from 'object'
      or jsonb_typeof(s->g->'main') is distinct from 'string'
      or jsonb_typeof(s->g->'why') is distinct from 'string'
      or jsonb_typeof(s->g->'reason') is distinct from 'string' then
      raise exception 'Invalid feedback answers';
    end if;
    if s->g->>'main' not in ('','1','2','3','4','5','cj')
      or length(s->g->>'why') > 4000 or length(s->g->>'reason') > 4000 then
      raise exception 'Invalid feedback value';
    end if;
    if s->g ? 'why2' and (jsonb_typeof(s->g->'why2') is distinct from 'string'
      or length(s->g->>'why2') > 4000) then
      raise exception 'Invalid additional feedback text';
    end if;
    if complete_all and (s->g->>'main' = ''
      or (s->g->>'main' = 'cj' and btrim(s->g->>'reason') = '')) then
      raise exception 'Feedback answers are incomplete';
    end if;
    for n in 1..4 loop
      v := s->g->'items'->(n::text);
      if v is not null and (jsonb_typeof(v) <> 'number' or v::text !~ '^[1-5]$') then
        raise exception 'Invalid feedback rating';
      end if;
      if complete_all and v is null then raise exception 'Feedback ratings are incomplete'; end if;
    end loop;
  end loop;
end;
$$;

create or replace function public.survey_open(p_id uuid, p_token text, p_mode text)
returns jsonb language plpgsql security definer set search_path = '' as $$
declare r public.survey_responses;
begin
  perform survey_private.check_token(p_token);
  if p_id is null or p_mode is null or p_mode not in ('test','live') then
    raise exception 'Invalid session';
  end if;
  select * into r from public.survey_responses where participant_id = p_id;
  if not found then
    if not coalesce((select accepting from public.survey_settings where mode = p_mode), false)
      or not coalesce((select accepting from public.survey_study_settings where mode=p_mode and study='module-spec-v3'), false) then
      raise exception 'This survey is not accepting new participants';
    end if;
    insert into public.survey_responses(participant_id, token_hash, mode)
    values (p_id, sha256(convert_to(p_token, 'UTF8')), p_mode)
    on conflict (participant_id) do nothing;
    select * into r from public.survey_responses where participant_id = p_id;
  end if;
  if r.token_hash <> sha256(convert_to(p_token, 'UTF8')) or r.mode <> p_mode then
    raise exception 'Invalid session';
  end if;
  return survey_private.snapshot(r);
end;
$$;

create or replace function public.survey_save(p_id uuid, p_token text, p_revision bigint, p_state jsonb)
returns jsonb language plpgsql security definer set search_path = '' as $$
declare r public.survey_responses;
begin
  perform survey_private.check_token(p_token);
  if p_revision is null or p_revision < 1 then raise exception 'Invalid revision'; end if;
  perform survey_private.validate_state(p_state, false, false);
  select * into r from public.survey_responses where participant_id = p_id for update;
  if not found or r.token_hash <> sha256(convert_to(p_token, 'UTF8')) then
    raise exception 'Invalid session';
  end if;
  if r.study <> 'module-spec-v3' or r.suite <> 'module.spec' then
    raise exception 'This response belongs to an earlier survey version';
  end if;
  if r.submitted_at is null and p_revision > r.revision then
    update public.survey_responses set state = p_state, revision = p_revision, updated_at = now()
    where participant_id = p_id returning * into r;
  end if;
  return survey_private.snapshot(r);
end;
$$;

create or replace function public.survey_assign(p_id uuid, p_token text, p_revision bigint, p_state jsonb)
returns jsonb language plpgsql security definer set search_path = '' as $$
declare r public.survey_responses; a public.survey_allocation; ord text[]; pos integer;
begin
  perform survey_private.check_token(p_token);
  if p_revision is null or p_revision < 1 then raise exception 'Invalid revision'; end if;
  perform survey_private.validate_state(p_state, true, false);
  select * into r from public.survey_responses where participant_id = p_id for update;
  if not found or r.token_hash <> sha256(convert_to(p_token, 'UTF8')) then
    raise exception 'Invalid session';
  end if;
  if r.study <> 'module-spec-v3' or r.suite <> 'module.spec' then
    raise exception 'This response belongs to an earlier survey version';
  end if;
  if r.condition is not null then return survey_private.snapshot(r); end if;
  if not coalesce((select accepting from public.survey_settings where mode = r.mode), false)
    or not coalesce((select accepting from public.survey_study_settings where mode=r.mode and study=r.study), false) then
    raise exception 'This survey is not accepting new assignments';
  end if;
  if p_revision < r.revision then raise exception 'A newer draft exists. Reload this page'; end if;
  -- The row lock serializes assignments, including concurrent visitors.
  select * into a from public.survey_allocation where mode = r.mode and study = r.study for update;
  if not found then raise exception 'Survey allocation is not configured'; end if;
  pos := (a.assigned_count % 3)::integer + 1;
  ord := a.current_order;
  if pos = 1 then
    select array_agg(x order by random()) into ord from unnest(array['A','B','C']) as x;
  end if;
  update public.survey_allocation set assigned_count = a.assigned_count + 1, current_order = ord
    where mode = r.mode and study = r.study;
  update public.survey_responses set
    condition = ord[pos], block_number = a.assigned_count / 3 + 1,
    block_position = pos, assigned_at = now(), updated_at = now(),
    state = p_state, revision = p_revision
  where participant_id = p_id returning * into r;
  return survey_private.snapshot(r);
end;
$$;

create or replace function public.survey_submit(p_id uuid, p_token text, p_revision bigint, p_state jsonb)
returns jsonb language plpgsql security definer set search_path = '' as $$
declare r public.survey_responses;
begin
  perform survey_private.check_token(p_token);
  select * into r from public.survey_responses where participant_id = p_id for update;
  if not found or r.token_hash <> sha256(convert_to(p_token, 'UTF8')) then
    raise exception 'Invalid session';
  end if;
  -- Retrying a completed submission returns the same receipt; it never overwrites it.
  if r.submitted_at is not null then return survey_private.snapshot(r); end if;
  if r.study <> 'module-spec-v3' or r.suite <> 'module.spec' then
    raise exception 'This response belongs to an earlier survey version';
  end if;
  if p_revision is null or p_revision < 1 or p_revision < r.revision then
    raise exception 'A newer draft exists. Reload this page';
  end if;
  if r.condition is null then raise exception 'No material has been assigned'; end if;
  perform survey_private.validate_state(p_state, true, true);
  update public.survey_responses set state = p_state, revision = p_revision,
    submitted_at = now(), updated_at = now()
  where participant_id = p_id returning * into r;
  return survey_private.snapshot(r);
end;
$$;

revoke all on all functions in schema survey_private from public, anon, authenticated;
revoke all on function public.survey_open(uuid,text,text),
  public.survey_save(uuid,text,bigint,jsonb), public.survey_assign(uuid,text,bigint,jsonb),
  public.survey_submit(uuid,text,bigint,jsonb) from public, anon, authenticated;
grant execute on function public.survey_open(uuid,text,text),
  public.survey_save(uuid,text,bigint,jsonb), public.survey_assign(uuid,text,bigint,jsonb),
  public.survey_submit(uuid,text,bigint,jsonb) to anon, authenticated;

-- Researcher-only view. It omits session tokens and flattens answers for CSV export.
create or replace view public.survey_export with (security_invoker = true) as
select participant_id, study, suite, mode, condition, block_number, block_position,
  created_at, assigned_at, submitted_at,
  state->>'bg01' as role, state->>'bg01_other' as other_role,
  state->>'bg02' as testing_experience,
  state->'bg03'->>'js' as familiarity_js_ts,
  state->'bg03'->>'java' as familiarity_java,
  state->'bg03'->>'jest' as familiarity_jest_bun,
  state->'bg03'->>'e2e' as familiarity_browser_testing,
  state->'g1'->>'main' as understanding_overall,
  state->'g1'->'items'->>'1' as understanding_behavior,
  state->'g1'->'items'->>'2' as understanding_case_purpose,
  state->'g1'->'items'->>'3' as understanding_actions_assertions,
  state->'g1'->'items'->>'4' as understanding_case_relations,
  state->'g1'->>'reason' as understanding_cannot_judge_reason,
  state->'g1'->>'why' as understanding_why,
  state->'g2'->>'main' as extension_overall,
  state->'g2'->'items'->>'1' as extension_avoid_duplicates,
  state->'g2'->'items'->>'2' as extension_starting_point,
  state->'g2'->'items'->>'3' as extension_next_behavior,
  state->'g2'->'items'->>'4' as extension_inputs_results,
  state->'g2'->>'reason' as extension_cannot_judge_reason,
  state->'g2'->>'why' as extension_why,
  state->'secs' as elapsed_seconds_by_step,
  state->>'scrollCode' as max_scroll_code_pct,
  state->>'scrollDoc' as max_scroll_doc_pct,
  state->>'linkClicks' as document_line_link_clicks,
  state->'g1'->>'why2' as understanding_unclear_why,
  state->'g2'->>'why2' as extension_information_needed,
  state->'bg03'->>'language' as familiarity_language,
  state->'bg03'->>'playwright' as familiarity_playwright,
  state->'bg03'->>'dom' as familiarity_html_dom,
  state->'bg03'->>'css' as familiarity_css_bootstrap,
  case when jsonb_typeof(state->'bg01')='array' then state->'bg01' end as roles,
  state->'bg01' ? 'Software developer / engineer' as role_developer,
  state->'bg01' ? 'Software test / QA engineer' as role_tester,
  state->'bg01' ? 'Researcher / academic' as role_researcher,
  state->'bg01' ? 'Other' as role_other,
  state->'cq'->>'cq1' as comprehension_case_count,
  state->'cq'->>'cq2' as comprehension_page_visibility,
  state->'cq'->>'cq3' as comprehension_modal_failure,
  state->'cq'->>'cq3_why' as comprehension_modal_reason
from public.survey_responses;
revoke all on public.survey_export from public, anon, authenticated;

notify pgrst, 'reload schema';
commit;
