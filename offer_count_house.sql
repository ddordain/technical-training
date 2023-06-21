DO $$ BEGIN
    RAISE NOTICE 'House offers count';
END $$;
SELECT COUNT(*)
FROM estate_property_offer AS offer
INNER JOIN estate_property_type AS type
ON offer.property_type_id = type.id
WHERE type.name = 'House';

DO $$ BEGIN
    RAISE NOTICE 'Studio offers count';
END $$;
SELECT COUNT(*)
FROM estate_property_offer AS offer
INNER JOIN estate_property_type AS type
ON offer.property_type_id = type.id
WHERE type.name = 'Studio';
