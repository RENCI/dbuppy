create table if not exists public.t_removeditems
(
    id        integer generated always as identity,
    created   timestamp with time zone,
    tablename text  not null,
    item      jsonb not null
);

