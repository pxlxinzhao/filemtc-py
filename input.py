import java_type

### top3 that need to be changed
workspace = "C:\Users\patrickpu\workspace10"

sql = '''
SELECT TOP 1000 [accounting_period_key]
  ,[date_from]
  ,[date_to]
  ,[fiscal_year]
  ,[period]
  ,[is_closed]
  ,[is_ar_closed]
  ,[is_ap_closed]
  ,[is_pr_closed]
  ,[version]
FROM [Fortigo_TMS].[dbo].[Accounting_Period]
'''

primary_key_java_type = "Integer"

### right now it is pretty specific to tms
tmsApp = "\TMSAppService\src\main\java\com\\fortigofreight\\tms"
tmsWeb = "\TMSWeb\src\main\java\com\\fortigofreight\\tms"

paths = {
    java_type.domain: workspace + tmsApp + "\domain",
    java_type.dao: workspace + tmsApp + "\dao",
    java_type.dao_impl: workspace + tmsApp + "\dao",
    java_type.service: workspace + tmsApp + "\service",
    java_type.service_impl: workspace + tmsApp + "\service",
    java_type.resource: workspace + tmsWeb + '\\rest'
}

front_end_files = [
    workspace + "\TMSWeb\src\main\webapp\\task.jsp",
    workspace + "\TMSWeb\src\main\webapp\\task_search.jsp",
    workspace + "\TMSWeb\src\main\webapp\js\\task.js",
    workspace + "\TMSWeb\src\main\webapp\js\\task_search.js"
]

xmlPath = workspace + "\TMSWeb\src\main\\resources\\applicationContext-master.xml"

scriptPath = workspace + "\TMSAppService\sql_scripts\hqlScriptsTMS.ini"

update_container = '''
insert into [Fortigo_Shell].[dbo].[dataset_container]
values ( 'task_search',	'com.fortigofreight.tms.dao.TaskDao'	,'getBasicHql'	,'taskDao'	,'sessionFactory',	NULL,	'HQL',	1)
'''

update_menu = '''
insert into [Fortigo_Shell].[dbo].[sec_menu] values (
'TMS',	'TMS9015',	'Task',	'A',	'TMS1014',	8,	NULL,	'CenterPaneUrl=/TMS/task.jsp',	1,	1,	1,	NULL,	NULL,	NULL,	0
)
'''



