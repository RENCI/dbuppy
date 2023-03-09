create table t_removeditems2
(
    id        integer generated always as identity,
    created   timestamp with time zone,
    tablename text  not null,
    item      jsonb not null
);

