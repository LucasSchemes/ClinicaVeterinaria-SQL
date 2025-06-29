SELECT 
    c.nome AS Cliente,
    SUM(i.quantidade * p.preco) AS Total_Gasto
FROM tb_cliente c
JOIN tb_fatura f ON c.id_cli = f.id_cli_fkc
JOIN tb_item_fatura i ON f.id_fat = i.id_fat_fkc
JOIN tb_produto p ON i.id_prod_fkc = p.id_prod
GROUP BY c.nome
ORDER BY Total_Gasto DESC;
