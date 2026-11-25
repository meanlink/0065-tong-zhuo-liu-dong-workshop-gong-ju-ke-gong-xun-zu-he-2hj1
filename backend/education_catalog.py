def lesson_index(cx):
    return cx.execute('''
      SELECT t.*, count(DISTINCT a.pupil) FILTER (WHERE a.checked AND p.pass='active') AS valid
      FROM tool_lessons t LEFT JOIN module_attendance a ON t.code=a.lesson LEFT JOIN pupil_cards p ON a.pupil=p.code
      GROUP BY t.code ORDER BY t.minutes,t.code
    ''').fetchall()
