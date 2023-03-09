create table "T_Administrator"
(
    "userId"     varchar,
    "adminName"  varchar,
    "adminEmail" varchar
);

alter table "T_Administrator"
    owner to postgres;

create table  "T_AssignProposal"
(
    "ProposalID"          bigint,
    "assignToInstitution" varchar,
    "ticPOC"              varchar,
    "ricPOC"              varchar,
    "ncatsPOC"            varchar
);