CREATE TABLE IF NOT EXISTS tool_lessons (
 code text PRIMARY KEY,title text NOT NULL,kit text NOT NULL,units int NOT NULL CHECK(units>0),
 minutes int NOT NULL CHECK(minutes BETWEEN 5 AND 180), tutor_key text NOT NULL
);
CREATE TABLE IF NOT EXISTS pupil_cards (
 code text PRIMARY KEY, cohort text NOT NULL, pass text NOT NULL CHECK(pass IN ('active','expired')),
 joined date NOT NULL
);
CREATE TABLE IF NOT EXISTS module_attendance (
 pupil text REFERENCES pupil_cards(code), lesson text REFERENCES tool_lessons(code), seen date NOT NULL,
 checked boolean NOT NULL, PRIMARY KEY(pupil,lesson,seen)
);
CREATE TABLE IF NOT EXISTS joint_groups (
 group_key text PRIMARY KEY, members text[] NOT NULL, min_support numeric(5,4) CHECK(min_support BETWEEN 0 AND 1),
 evidence jsonb NOT NULL, calculated_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS road_stops (
 code text PRIMARY KEY, site text NOT NULL, workshop_on date NOT NULL, duration int NOT NULL CHECK(duration>0),
 kits int NOT NULL CHECK(kits>0), tutors text[] NOT NULL
);
CREATE TABLE IF NOT EXISTS stop_plans (
 stop text PRIMARY KEY REFERENCES road_stops(code), lessons text[] NOT NULL,
 expected_minutes int NOT NULL, expected_kits int NOT NULL, notes text NOT NULL,
 signed_by text NOT NULL, signed_at timestamptz NOT NULL DEFAULT now()
);
