INSERT INTO tool_lessons VALUES ('FOLD','折叠工具收纳','收纳标识套件',1,12,'feng'),
 ('LABEL','材料边角与标记','标记卡套件',1,10,'feng'),('CLAMP','固定台面操作观察','观察工位',2,18,'he'),
 ('SORT','小件清点','清单套件',1,15,'zu'),('GLOVE','防护用具识别','示范手套',2,16,'he')
 ON CONFLICT DO NOTHING;
INSERT INTO pupil_cards VALUES ('P01','新入门','active','2026-11-16'),('P02','新入门','active','2026-11-16'),
 ('P03','新入门','active','2026-11-16'),('P04','返训','active','2026-11-18'),
 ('P05','返训','active','2026-11-18'),('P06','返训','active','2026-11-18'),('P07','临访','expired','2026-11-12')
 ON CONFLICT DO NOTHING;
INSERT INTO module_attendance VALUES
 ('P01','FOLD','2026-11-16',true),('P01','LABEL','2026-11-16',true),
 ('P02','FOLD','2026-11-16',true),('P02','LABEL','2026-11-16',true),
 ('P03','FOLD','2026-11-16',true),('P03','LABEL','2026-11-16',true),('P03','SORT','2026-11-16',false),
 ('P04','CLAMP','2026-11-18',true),('P04','GLOVE','2026-11-18',true),
 ('P05','CLAMP','2026-11-18',true),('P05','GLOVE','2026-11-18',true),
 ('P06','SORT','2026-11-18',true),('P07','SORT','2026-11-18',false)
 ON CONFLICT DO NOTHING;
INSERT INTO road_stops VALUES ('XS1','许家巷社区','2026-11-26',50,4,ARRAY['feng','he']),
 ('DT2','渡头儿童中心','2026-11-27',35,1,ARRAY['feng']),
 ('C03','长东青少年空间','2026-11-30',25,3,ARRAY['feng','zu'])
 ON CONFLICT DO NOTHING;
