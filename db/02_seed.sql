-- Source Type Seed
INSERT INTO source_type (source_type_name)
VALUES ('Book'), ('Bible'), ('Homily'), ('Podcast');

-- Bible Seed
INSERT INTO bible_book (bible_book_name, abbreviation, canonical_order, last_chapter)
VALUES ('Genesis', 'GEN', 1, 50);
-- Creator Seed

INSERT INTO creator (full_name)
VALUES ('Fr. Mike Schmitz');

INSERT INTO creator (full_name)
VALUES ('Jeff Cavins');

-- Series Seed

INSERT INTO series (series_name)
VALUES ('Bible In a Year');

INSERT INTO series (series_name)
VALUES ('Catechism In a Year');

-- Source Seed

INSERT INTO source (source_name, source_type_id, creator_id)
VALUES ('Walking with God', 1, 2);

INSERT INTO source (source_name, series_id, source_type_id, creator_id)
VALUES ('Day 10: God Visits Abram', 1, 4, 1);

INSERT INTO source (source_name, series_id, source_type_id, creator_id)
VALUES ('Day 5: Gods Revelation to Man', 2, 4, 1);

-- Insight Seed

INSERT INTO insight (source_id, insight_creator_id, insight_content)
VALUES (2, 1, 'God creates through speech');

INSERT INTO insight (source_id, insight_creator_id, insight_content)
VALUES (1, 2, 'Abram left his country but not totally. He brought Lot as backup indicating he didnt full trust GOD');

INSERT INTO insight (source_id, insight_creator_id, insight_content)
VALUES (1, 2, 'As a result of Abrams lack of faith in God saying he will have as many descendents as stars in the sky, the ground Abram lands in is not fertile.');

INSERT INTO insight (source_id, insight_creator_id, insight_content)
VALUES (3, 1, 'God has revealed everything for salvation. No other future revelation is needed');

-- Bible Reference Seed

INSERT INTO bible_reference (insight_id, bible_book_id, chapter_start, verse_start, chapter_end, verse_end, note)
VALUES (2, 1, 12, 1, NULL, 5, NULL);

INSERT INTO bible_reference (insight_id, bible_book_id, chapter_start, verse_start, chapter_end, verse_end, note)
VALUES (3, 1, 12, 10, Null, Null, 'theme: faithfullness to God''s exact words');

