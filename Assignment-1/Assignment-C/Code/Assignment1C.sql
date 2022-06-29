SELECT 
    sum(mn.unknown) AS Unknown_count,
    sum(mn.adventure) AS Adventure_count,
    sum(mn.animation) AS Animation_count,
    sum(mn.childrens) AS Childrens_count,
    sum(mn.comedy) AS Comedy_count,
    sum(mn.crime) AS Crime_count,
    sum(mn.documentary) AS Documentary_count,
    sum(mn.drama) AS Drama_count,
    sum(mn.fantasy) AS Fantasy_count,
    sum(mn.film_Noir) AS Film_Noir_count,
    sum(mn.horror) AS Horror_count,
    sum(mn.musical) AS Musical_count,
    sum(mn.mystery) AS Mystery_count,
    sum(mn.romance) AS Romance_count,
    sum(mn.sci_fi) AS Sci_Fi_count,
    sum(mn.thriller) AS Thriller_count,
    sum(mn.war) AS War_count,
    sum(mn.western) AS Western_count

FROM 
    movie_names mn
    RIGHT JOIN movie_ratings AS mr ON mn.movie_id = mr.movie_id

GROUP BY CASE 
    WHEN mn.unknown = 1 THEN 1 
    WHEN mn.adventure = 1 THEN 1 
    WHEN mn.animation = 1 THEN 1 
    WHEN mn.childrens = 1 THEN 1 
    WHEN mn.comedy = 1 THEN 1 
    WHEN mn.crime = 1 THEN 1 
    WHEN mn.documentary = 1 THEN 1 
    WHEN mn.drama = 1 THEN 1 
    WHEN mn.fantasy = 1 THEN 1 
    WHEN mn.film_Noir = 1 THEN 1 
    WHEN mn.horror = 1 THEN 1 
    WHEN mn.musical = 1 THEN 1 
    WHEN mn.mystery = 1 THEN 1 
    WHEN mn.romance = 1 THEN 1 
    WHEN mn.sci_fi = 1 THEN 1 
    WHEN mn.thriller = 1 THEN 1 
    WHEN mn.war = 1 THEN 1 
    WHEN mn.western = 1 THEN 1
    ELSE 0 
    END;