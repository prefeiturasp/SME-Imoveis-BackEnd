CREATE OR REPLACE PROCEDURE public.detect_bidder_duplicity()
LANGUAGE 'plpgsql'
AS $BODY$
declare
    ic_row record;
    imovel record;
	pk_doc character varying(20);
	type_descr character varying(50);
	pk integer;
	bid_name character varying(255);
	iptu character varying(20);
	status character varying(255);
	flag_ok boolean;
	TYPE_BIDDER TEXT ARRAY  DEFAULT  ARRAY['Imobiliária', 'Procurador', 'Ong', 'Outro'];
begin
	SELECT EXISTS (
        SELECT FROM pg_catalog.pg_class c
           JOIN   pg_catalog.pg_namespace n ON n.oid = c.relnamespace
           WHERE  n.nspname = 'schema_name'
             AND    c.relname = 'table_name'
             AND    c.relkind = 'r'    -- only tables
   ) into flag_ok;
	if not flag_ok then
		create table public.imovel_conversion
		(
			date_conversion timestamp with time zone not null
		);
		insert into imovel_conversion 
			(date_conversion)
		values
			(CURRENT_TIMESTAMP);
	else
		return;
	end if;

	for ic_row in select * from imovel_proponente WHERE cpf_cnpj <> '' loop
		select pk_bidders into pk_doc from sme_bidders
		 where pk_bidders = ic_row.cpf_cnpj;
		select nome, pk_tipo_proponente into type_descr, pk 
		  from sme_tipo_proponente
		 where nome = TYPE_BIDDER[ic_row.tipo];
		if type_descr is null or type_descr = '' then
			insert into sme_type_bidders
				(name, insert_date, update_date)
			values
				(TYPE_BIDDER[ic_row.tipo], CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
			select Tpd.pk_type_bidders into pk from sme_type_bidders Tpd
			 where Tpd.name = TYPE_BIDDER[ic_row.tipo];
		end if;
		ic_row.tipo = pk;
		if pk_doc is null or pk_doc = '' then
			insert into sme_bidders
				(pk_bidders, fk_type_bidders_id, name, email, telefone, 
				 insert_date, update_date)
			values
				(ic_row.cpf_cnpj, pk, ic_row.nome, ic_row.email, 
				 ic_row.telefone, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
			update imovel_proponente set
				   fk_tipo_proponente = ic_row.tipo,
				   situacao = 'ok'
			 where id = ic_row.id;
		else
			update imovel_proponente set
				   fk_tipo_proponente = ic_row.tipo,
				   situacao = 'CNPJ Duplicado'
			 where id = ic_row.id;
		end if;
		select Prp.id, Prp.nome into pk, bid_name from imovel_proponente Prp
		 where Prp.nome like '%' || ic_row.nome || '%' and Prp.situacao is null;
		if bid_name is not null or bid_name <> '' then
			update imovel_proponente set
				   fk_tipo_proponente = ic_row.tipo,
				   situacao = 'CNPJ Duplicado'
			 where id = ic_row.id;
		end if;
	end loop;
	for imovel in select * from imovel_imovel Imv order by numero_iptu loop
	    select Prp.cpf_cnpj into pk_doc from imovel_proponente Prp
		 where Prp.id = imovel.proponente_id;
		select pk_bidders_buildings into pk
		  from sme_bidders_buildings
		 where fk_bidders_id = pk_doc
		   and number_iptu = imovel.numero_iptu
		   and latitude = cast(imovel.latitude as float)
		   and longitude = cast(imovel.longitude as float);
	    if pk is null or pk = 0 then
		    status = 'Ok';
		else
            if imovel.numero_iptu = '' then
		        status = 'Imovel duplicado e sem iptu';
		    else
				select pk_bidders_buildings, number_iptu into pk, iptu 
				  from sme_bidders_buildings
				 where fk_biiders_id = pk_doc
				   and number_iptu = imovel.numero_iptu;
				if pk_bidders_buildings is not null or pk_bidders_buildings = 0 then
				    status = 'Imovel duplicado pelo IPTU';
				else
				    status = 'Ok';
				end if;
			end if;
	    end if;
		update imovel_imovel set
			   situacao = status
		 where id = imovel.id;
	    if status = 'Ok' then
		    insert into sme_bidders_buildings
			    (cep. quarter, number, complement, latitude, 
				 longitude, number_iptu, fk_bidders_id, insert_date, update_date)
			values
				(imovel.cep, imovel.numero, imovel.bairro, imovel.complemento,
				imovel.latitude, imovel.longitude, imovel.numero_iptu, pk_doc, 
				 current_timestamp, current_timestamp);
	    end if;
	end loop;
    return;
end;
$BODY$;