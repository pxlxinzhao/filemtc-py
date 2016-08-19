import filemtc

builder = filemtc.FilemtcBuilder()

#madatory
builder.write_hql()

#no harm
# builder.write_xml()
# builder.build_jsp_js();
builder.print_sql()

#optional
# builder.write_domain()
# builder.build_dao_service_resource()
