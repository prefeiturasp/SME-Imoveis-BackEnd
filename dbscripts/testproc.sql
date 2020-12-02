CREATE OR REPLACE PROCEDURE public.test_procedure()
LANGUAGE 'plpgsql'
AS $BODY$
declare
	celular character varying(20) default "(00) 0 0000-0000";
begin
    update biiders set
       cel = celular;
end;
$BODY$;
