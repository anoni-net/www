-- 季報用的 Pulse 數字：季初與季末快照的中繼名單比對、整季的穩定度、季初與季末的 ASN 分布。
-- 每一天取當天最後一次快照，參數 since（含）與 until（不含）。用法見 tools/quarterly_report.py 的開頭。
WITH snaps AS (
  SELECT country, created_at::date AS day, max(created_at) AS snap
  FROM relay_details
  WHERE created_at >= :'since' AND created_at < :'until'
    AND country IN ('tw','jp','kr','hk','sg','vn','in','de','nl','us')
  GROUP BY 1, 2
),
bounds AS (
  SELECT country, min(snap) FILTER (WHERE day = (SELECT min(day) FROM snaps s2 WHERE s2.country = snaps.country)) AS first_snap,
         max(snap) AS last_snap, count(*) AS days
  FROM snaps GROUP BY 1
),
daily AS (
  SELECT r.country, r.fingerprint, r.asn, r.as_name, s.snap
  FROM relay_details r JOIN snaps s ON r.country = s.country AND r.created_at = s.snap
  WHERE r.running
),
start_set AS (SELECT d.country, d.fingerprint, d.asn, d.as_name FROM daily d JOIN bounds b USING (country) WHERE d.snap = b.first_snap),
end_set AS (SELECT d.country, d.fingerprint, d.asn, d.as_name FROM daily d JOIN bounds b USING (country) WHERE d.snap = b.last_snap),
presence AS (SELECT country, fingerprint, count(*) AS n FROM daily GROUP BY 1, 2),
churn AS (
  SELECT b.country, b.days, b.first_snap, b.last_snap,
    (SELECT count(*) FROM start_set s WHERE s.country = b.country) AS at_start,
    (SELECT count(*) FROM end_set e WHERE e.country = b.country) AS at_end,
    (SELECT count(*) FROM start_set s JOIN end_set e USING (country, fingerprint) WHERE s.country = b.country) AS stayed,
    (SELECT count(*) FROM presence p WHERE p.country = b.country) AS seen,
    (SELECT count(*) FROM presence p WHERE p.country = b.country AND p.n >= 0.9 * b.days) AS stable
  FROM bounds b
),
asn_end AS (
  SELECT country, asn, max(as_name) AS as_name, count(*) AS n FROM end_set GROUP BY 1, 2
),
asn_start AS (
  SELECT country, asn, count(*) AS n FROM start_set GROUP BY 1, 2
)
SELECT json_build_object(
  'since', :'since', 'until', :'until',
  'churn', (SELECT json_agg(c ORDER BY country) FROM churn c),
  'asn_end', (SELECT json_agg(a ORDER BY country, n DESC) FROM asn_end a),
  'asn_start', (SELECT json_agg(a ORDER BY country, n DESC) FROM asn_start a)
);
