SELECT 
    p.nome AS Produto,
    COUNT(pr.id_prod_fkc) AS Total_Prescricoes
FROM tb_prescricao pr
JOIN tb_produto p ON pr.id_prod_fkc = p.id_prod
JOIN tb_consulta c ON pr.id_con_fkc = c.id_con
GROUP BY p.nome
ORDER BY Total_Prescricoes DESC;
