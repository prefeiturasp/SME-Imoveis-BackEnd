sql_create_view_listaimoveis = \
"""
 CREATE VIEW imovel_vw_listaimoveis AS
 SELECT imovel.id AS "Cód Cadastro",
    concat(imovel.endereco, ', ', imovel.numero) AS "Endereço",
    imovel.complemento AS "Complemento",
    imovel.bairro AS "Bairro",
    imovel.cep AS "Cep",
    imovel.numero_iptu AS "IPTU",
    contato.id AS "Cód Proprietário",
    contato.nome AS "Nome Proprietário",
    contato.cpf_cnpj AS "CPF/CNPJ Proprietário",
    contato.email AS "Email Proprietário",
    contato.telefone AS "Telefone Proprietário",
    prop.id AS "Cód Proponente",
    prop.nome AS "Nome Proponente",
    prop.cpf_cnpj AS "CPF/CNPJ Proponente",
    prop.email AS "Email Proponente",
    prop.telefone AS "Telefone Proponente",
        CASE prop.tipo
            WHEN 1 THEN 'Imobiliária'::text
            WHEN 2 THEN 'Procurador'::text
            WHEN 3 THEN 'ONG'::text
            ELSE 'Outros'::text
        END AS "Tipo Proponente",
    imovel.criado_em AS "Data do Cadastro"
   FROM imovel_imovel imovel
     JOIN imovel_contatoimovel contato ON contato.id = imovel.contato_id
     LEFT JOIN imovel_proponente prop ON imovel.proponente_id = prop.id
  ORDER BY imovel.id;
"""

sql_drop_view_listaimoveis = \
"""
DROP VIEW IF EXISTS imovel_vw_listaimoveis
"""