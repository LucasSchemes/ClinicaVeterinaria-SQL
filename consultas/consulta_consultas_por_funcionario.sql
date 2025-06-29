SELECT 
    f.nome AS Funcionario,
    COUNT(c.id_con) AS Total_Consultas
FROM tb_funcionario f
JOIN tb_consulta c ON f.id_fun = c.id_fun_fkc
JOIN tb_pet p ON c.id_pet_fkc = p.id_pet
GROUP BY f.nome
ORDER BY Total_Consultas DESC;
