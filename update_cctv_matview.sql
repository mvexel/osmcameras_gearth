DROP INDEX id_idx;
SELECT refresh_matview('cctv_mv');
CREATE INDEX id_idx ON cctv_mv(id);
