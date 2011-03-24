SELECT create_matview('cctv_mv', 'cctv');
CREATE INDEX id_idx ON cctv_mv(id);
ALTER TABLE cctv_mv
  ADD CONSTRAINT pk_cctv_nodes PRIMARY KEY(id);
ALTER TABLE cctv_mv
  ADD CONSTRAINT enforce_dims_geom CHECK (ndims(geom) = 2);
ALTER TABLE cctv_mv
  ADD CONSTRAINT enforce_geotype_geom CHECK (geometrytype(geom) = 'POINT'::text OR geom IS NULL);
ALTER TABLE cctv_mv
  ADD CONSTRAINT enforce_srid_geom CHECK (srid(geom) = 4326);
select probe_geometry_columns()