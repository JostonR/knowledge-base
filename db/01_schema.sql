-- 1) TYPES OF SOURCES (book, bible, catechism, movie, podcast, homily, etc.)
CREATE TABLE source_type (
    id          SERIAL PRIMARY KEY,
    source_type_name        VARCHAR(50) NOT NULL UNIQUE,  -- e.g. 'book', 'bible', 'catechism', 'homily'
    source_description TEXT
);

-- 2) CREATORS (authors, preachers, directors, artists, etc.)
CREATE TABLE creator (
    id          SERIAL PRIMARY KEY,
    full_name   VARCHAR(255) NOT NULL,
    title       TEXT,
    notes       TEXT
);

CREATE TABLE series (
    id      SERIAL PRIMARY KEY,
    series_name VARCHAR(255) UNIQUE,
    creator_id INT REFERENCES creator(id) ON DELETE CASCADE,
    source_type_id INT REFERENCES source_type(id) ON DELETE CASCADE
);
CREATE INDEX idx_series_name on series(series_name);
CREATE INDEX idx_series_creator on series(creator_id);

-- 3) SOURCES (books, movies, songs, homilies, catechism, bible, etc.)
CREATE TABLE source (
    id              SERIAL PRIMARY KEY,
    source_name     VARCHAR(255) NOT NULL,
    source_type_id  INT NOT NULL REFERENCES source_type(id),
    series_id          INT REFERENCES series(id),
    creator_id      INT REFERENCES creator(id), -- main creator/speaker/author (optional)
    secondary_creator_id    INT REFERENCES creator(id),
    source_description     TEXT,
    created_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_source_creator_id ON source(creator_id);
CREATE INDEX idx_source_type_id ON source(source_type_id); 
CREATE INDEX idx_second_source_creator_id     ON source(secondary_creator_id);
-- Helpful indexes

-- 4) INSIGHTS (your actual notes/reflections/homily seeds)
CREATE TABLE insight (
    id               SERIAL PRIMARY KEY,
    source_id        INT NOT NULL REFERENCES source(id) ON DELETE CASCADE,
    insight_creator_id   INT REFERENCES creator(id),
    insight_content  TEXT NOT NULL,    -- your insight text
    created_at       TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at       TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_insight_created_at ON insight(created_at);
CREATE INDEX idx_insight_source_id ON insight(source_id);
CREATE INDEX idx_insight_creator_id ON insight(insight_creator_id);

-- 5) BIBLE BOOKS (lookup for canonical book names)
CREATE TABLE bible_book (
    id              SERIAL PRIMARY KEY,
    bible_book_name            VARCHAR(50) NOT NULL UNIQUE,  -- 'Genesis', 'Exodus', 'Matthew', 'Romans'
    abbreviation    VARCHAR(16),                 -- 'Gen', 'Ex', 'Mt', 'Rom'
    testament       VARCHAR(4),                  -- 'OT', 'NT', 'DC' (Deuterocanonicals) if you like
    canonical_order INT,                          -- 1..73 for ordering
    last_chapter INT NOT NULL
);

-- 6) SCRIPTURE REFERENCES (structured Bible ranges per insight)
CREATE TABLE bible_reference (
    id             SERIAL PRIMARY KEY,
    insight_id     INT NOT NULL REFERENCES insight(id) ON DELETE CASCADE,
    bible_book_id  INT NOT NULL REFERENCES bible_book(id),
    chapter_start  INT,
    verse_start    INT,
    chapter_end    INT,
    verse_end      INT,
    note           TEXT             -- optional: 'main passage', 'cross-reference', etc.
);

CREATE INDEX idx_scripture_ref_book_chapter
    ON bible_reference (bible_book_id, chapter_start);

-- 7) BOOK REFERENCES (page/chapter info for sources that are books)
-- Since books live in `sources`, we just point back to source_id.
CREATE TABLE book_reference (
    id             SERIAL PRIMARY KEY,
    source_id      INT NOT NULL REFERENCES source(id) ON DELETE CASCADE,
    page_start     INT NOT NULL,
    page_end       INT,
    chapter_start  INT,   --
    chapter_end    INT,    --
    UNIQUE(id, source_id)
);

CREATE INDEX idx_book_ref_source_id  ON book_reference(source_id);

CREATE TABLE quote (
    id              SERIAL PRIMARY KEY,
    quote_text      TEXT NOT NULL,
    source_id       INT NOT NULL REFERENCES source(id) ON DELETE CASCADE,
    book_ref_id     INT,
    created_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_quote_bookref_same_source
        FOREIGN KEY (book_ref_id, source_id)
        REFERENCES book_reference(id, source_id)
);

