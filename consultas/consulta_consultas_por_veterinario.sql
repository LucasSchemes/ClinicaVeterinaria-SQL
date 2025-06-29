SELECT f.nome AS Veterinario, COUNT(c.id_con) AS Total_Consultas
FROM tb_consulta c
JOIN tb_funcionario f ON c.id_fun_fkc = f.id_fun
WHERE f.tipo_funcionario = 'Veterinario'
GROUP BY f.nome;