CREATE OR REPLACE PROCEDURE public.detect_bidder_duplicity()
LANGUAGE 'plpgsql'
AS $BODY$
declare
    ic_row record;
    imovel record;
	pk_doc character varying(20);
	type_descr character varying(50);
	pk_aux integer;
	pk_tipo integer;
	pk_type integer;
	bid_name character varying(255);
	iptu character varying(20);
	status character varying(255);
	flag_ok boolean;
	TYPE_BIDDER TEXT ARRAY  DEFAULT  ARRAY['Imobiliária', 'Procurador', 'Ong', 'Outro'];
begin
	SELECT EXISTS (
        SELECT FROM pg_catalog.pg_class c
           JOIN   pg_catalog.pg_namespace n ON n.oid = c.relnamespace
           WHERE  n.nspname = 'public'
             AND    c.relname = 'imovel_conversion'
             AND    c.relkind = 'r'    -- only tables
   ) into flag_ok;
	if not flag_ok then
		create table public.imovel_conversion (
			date_conversion timestamp with time zone not null
		);
	else
		return;
	end if;
	-- Delete all data from aux tables
	delete from sme_bidders_buildings_docs_imgs;
	delete from sme_bidders_buildings;
	delete from sme_bidders;
	delete from sme_type_bidders;
	-- End delete
	-- Star looping from imovel-proponente
	for ic_row in select * from imovel_proponente WHERE cpf_cnpj <> '' loop
		-- check if exists tipo_proponente based on tipo description of record
		select exists (
            select * from imovel_tipoproponente
             where nome = TYPE_BIDDER[ic_row.tipo]
        ) into flag_ok;
		-- not exists
		if not flag_ok then
		    -- insert into table new tipo
			insert into imovel_tipoproponente
				(pk_tipo_proponente, nome, criado_em, atualizado_em)
			values
				(ic_row.tipo, TYPE_BIDDER[ic_row.tipo], CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
		end if;
		select exists (
            select * from sme_type_bidders
             where name = TYPE_BIDDER[ic_row.tipo]
        ) into flag_ok;
		-- not exists
		if not flag_ok then
			insert into sme_type_bidders
				(pk_type_bidders, name, insert_date, update_date)
			values
				(ic_row.tipo, TYPE_BIDDER[ic_row.tipo], CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
		end if;
		pk_tipo = ic_row.tipo;
		pk_type = ic_row.tipo;
		-- check if bidder already exists
		select exists (
			select * from sme_bidders
			 where pk_bidders = ic_row.cpf_cnpj
		) into flag_ok;
		-- not exists
		pk_doc = ic_row.cpf_cnpj;
		-- set status with 'ok'
		status = 'Ok';
		if not flag_ok then
			-- Insert into biders table
			insert into sme_bidders
				(pk_bidders, fk_type_bidders_id, name, email, cel_phone,
				 phone, insert_date, update_date)
			values
				(ic_row.cpf_cnpj, pk_type, ic_row.nome, ic_row.email, ic_row.celular,
				 ic_row.telefone, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
		else -- exists
			-- set status with 'Duplicado'
			status = 'CPF/CNPJ Duplicado';
		end if;
		-- update imovel_proponente with new status
		update imovel_proponente set
			   fk_tipo_proponente_id = pk_tipo,
			   situacao = status
		 where id = ic_row.id;
	end loop; -- End looping
	-- Read all imovel_imovel table to identify duplicates
	for imovel in select * from imovel_imovel Imv order by numero_iptu loop
	    -- get doc_id from imovel_proponete table
	    select Prp.cpf_cnpj into pk_doc from imovel_proponente Prp
		 where Prp.id = imovel.proponente_id;
		-- check if buildings alerady exists from iptu_number
	    status = 'Ok';
		select exists (
			select * from sme_bidders_buildings
			 where fk_bidders_id = pk_doc
			   and number_iptu = imovel.numero_iptu
		) into flag_ok;
		-- not exists
	    if not flag_ok then
			-- exists and IPTU is null
            if imovel.numero_iptu = '' then
		        status = 'Imovel duplicado e sem iptu';
		    else
				-- exists and set duplicate
			    status = 'Imovel duplicado pelo IPTU';
			end if;
	    end if;
		-- update status on imovel_imovel table
		-- check if exists other building with same address
		select exists (
			select * from sme_bidders_buildings
			 where address like '%' || imovel.endereco || '%'
			   and number = imovel.numero
	    ) into flag_ok;
		if flag_ok then
		    status = 'Endereço Duplicado';
		end if;
		if not flag_ok and pk_doc is null or pk_doc = '' then
		    status = 'Falta o cpf_cnpj do proponente';
			flag_ok = true;
		end if;
		update imovel_imovel set
			   situacao = status
		 where id = imovel.id;
		-- if status is ok then include this contact on sme_bidders_buildings table
	    if not flag_ok then
			if imovel.cep is null then
			    imovel.cep = '00.000-000';
			end if;
            insert into sme_bidders_buildings
			    (cep, address, quarter, number,
				 complement, latitude, longitude,
				 number_iptu, fk_bidders_id, insert_date, update_date)
			values
				(imovel.cep, imovel.endereco, imovel.bairro, imovel.numero, 
				 imovel.complemento, imovel.latitude, imovel.longitude, 
				 imovel.numero_iptu, pk_doc, imovel.criado_em, current_timestamp);
			SELECT currval('sme_bidders_buildings_id_seq') into pk_aux;
	    end if;
	end loop;
	-- insert images to sme_bidders_buildings_docs_imgs
	insert into sme_bidders_buildings_docs_imgs 
	    (document, fk_bidders_buildings_id, flag_type_docs, flag_type_file, insert_date, update_date)
--	values
	    select planta, pk_aux, flag_tipo_documento, flag_tipo_arquivo, criado_em, current_timestamp
		  from imovel_plantafoto
		 where imovel_id in (select id from imovel_imovel where status = 'Ok');
    return;
end;
$BODY$;
