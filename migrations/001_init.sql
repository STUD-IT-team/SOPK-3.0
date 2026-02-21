-- +goose Up
-- +goose StatementBegin

CREATE TABLE IF NOT EXISTS timeslots (
    id UUID PRIMARY KEY,
    startt TIMESTAMPTZ NOT NULL UNIQUE,
    endt TIMESTAMPTZ NOT NULL UNIQUE,
    slotcnt INTEGER NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TYPE sex AS ENUM ('male', 'female');
CREATE TYPE department AS ENUM ('smm', 'cod', 'smm,cod');

CREATE TABLE IF NOT EXISTS activists (
    id UUID PRIMARY KEY,
    tgid BIGINT NOT NULL,
    full_name TEXT NOT NULL,
    sex sex NOT NULL,
    phone TEXT NOT NULL,
    timeslotid UUID REFERENCES timeslots(id),
    department department NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS organizers (
    id UUID PRIMARY KEY,
    tgid BIGINT NOT NULL,
    tgnick TEXT NOT NULL,
    full_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS sessions (
    id UUID PRIMARY KEY,
    startt TIMESTAMPTZ NOT NULL,
    endt TIMESTAMPTZ NULL,
    created_by UUID REFERENCES organizers(id),

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS sessions_activists (
    id UUID PRIMARY KEY,
    sessionid UUID REFERENCES sessions(id),
    activistid UUID REFERENCES activists(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS sessions_organizers (
    id UUID PRIMARY KEY,
    sessionid UUID REFERENCES sessions(id),
    organizerid UUID REFERENCES organizers(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS assessments (
    id UUID PRIMARY KEY,
    activistid UUID REFERENCES activists(id),
    organizerid UUID REFERENCES organizers(id),
    sessionid UUID REFERENCES sessions(id),

    logic INTEGER NOT NULL,
    charm INTEGER NOT NULL,
    speech INTEGER NOT NULL,
    resourcefulness INTEGER NOT NULL,
    stressresilience INTEGER NOT NULL,
    worthy BOOLEAN NOT NULL,
    comment TEXT NOT NULL,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin

DROP TABLE IF EXISTS activists;
DROP TABLE IF EXISTS organizers;
DROP TABLE IF EXISTS sessions;
DROP TABLE IF EXISTS sessions_activists;
DROP TABLE IF EXISTS sessions_organizers;
DROP TABLE IF EXISTS assessments;
DROP TABLE IF EXISTS timeslots;

DROP TYPE IF EXISTS sex;
DROP TYPE IF EXISTS department;

-- +goose StatementEnd