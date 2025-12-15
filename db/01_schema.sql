-- 1) TYPES OF SOURCES (book, bible, catechism, movie, podcast, homily, etc.)
CREATE TABLE source_types (
    id          SERIAL PRIMARY KEY,
    source_type_name        VARCHAR(50) NOT NULL UNIQUE,  -- e.g. 'book', 'bible', 'catechism', 'homily'
    source_description TEXT
);

-- 2) CREATORS (authors, preachers, directors, artists, etc.)
CREATE TABLE creators (
    id          SERIAL PRIMARY KEY,
    full_name   VARCHAR(255) NOT NULL,
    title       TEXT,
    notes       TEXT
);

-- 3) SOURCES (books, movies, songs, homilies, catechism, bible, etc.)
CREATE TABLE sources (
    id              SERIAL PRIMARY KEY,
    source_name     VARCHAR(255) NOT NULL,
    source_type_id  INT NOT NULL REFERENCES source_types(id),
    creator_id      INT REFERENCES creators(id), -- main creator/speaker/author (optional)
    secondary_creator_id    INT REFERENCES creators(id),
    source_description     TEXT,
    created_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Helpful indexes
CREATE INDEX idx_sources_source_type_id ON sources(source_type_id);
CREATE INDEX idx_sources_creator_id     ON sources(creator_id);

-- 4) INSIGHTS (your actual notes/reflections/homily seeds)
CREATE TABLE insights (
    id               SERIAL PRIMARY KEY,
    source_id        INT NOT NULL REFERENCES sources(id) ON DELETE CASCADE,
    insight_creator_id   INT REFERENCES creators(id),
    insight_content  TEXT NOT NULL,    -- your insight text
    quote_text       TEXT,          -- the passage from the book
    insight_type     VARCHAR(50),      -- 'quote', 'reflection', 'summary', 'homily_seed', etc.
    created_at       TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at       TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_insights_source_id ON insights(source_id);

-- 5) BIBLE BOOKS (lookup for canonical book names)
CREATE TABLE bible_books (
    id              SERIAL PRIMARY KEY,
    bible_book_name            VARCHAR(50) NOT NULL UNIQUE,  -- 'Genesis', 'Exodus', 'Matthew', 'Romans'
    abbreviation    VARCHAR(16),                 -- 'Gen', 'Ex', 'Mt', 'Rom'
    testament       VARCHAR(4),                  -- 'OT', 'NT', 'DC' (Deuterocanonicals) if you like
    canonical_order INT,                          -- 1..73 for ordering
    last_chapter INT NOT NULL
);

-- 6) SCRIPTURE REFERENCES (structured Bible ranges per insight)
CREATE TABLE scripture_references (
    id             SERIAL PRIMARY KEY,
    insight_id     INT NOT NULL REFERENCES insights(id) ON DELETE CASCADE,
    bible_book_id  INT NOT NULL REFERENCES bible_books(id),
    chapter_start  INT,
    verse_start    INT,
    chapter_end    INT,
    verse_end      INT,
    note           TEXT             -- optional: 'main passage', 'cross-reference', etc.
);

CREATE INDEX idx_scripture_refs_book_chapter
    ON scripture_references (bible_book_id, chapter_start);

-- 7) BOOK REFERENCES (page/chapter info for sources that are books)
-- Since books live in `sources`, we just point back to source_id.
CREATE TABLE book_references (
    id             SERIAL PRIMARY KEY,
    insight_id     INT NOT NULL REFERENCES insights(id) ON DELETE CASCADE,
    source_id      INT NOT NULL REFERENCES sources(id) ON DELETE CASCADE,
    page_start     INT,
    page_end       INT,
    chapter_start  INT,   --
    chapter_end    INT    --
);

CREATE INDEX idx_book_refs_source_id  ON book_references(source_id);
CREATE INDEX idx_book_refs_insight_id ON book_references(insight_id);
