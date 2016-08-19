import helper
import input

dao = '''
package com.fortigofreight.tms.dao;

public interface TaskDao extends FmDao<Task>{
    String getBasicHql();
}
'''

daoImpl = '''
package com.fortigofreight.tms.dao;

public class TaskDaoImpl extends GenericFmDao<Task> implements TaskDao {
	private String TASK_HQL = null;

	@Override
	public String getBasicHql() { return TASK_HQL; }

	@Override
	public void setIniFile(IniFile iniFile) {
		super.setIniFile(iniFile);
		TASK_HQL = iniFile.getSqlStatement("GET_TASK_HQL");
		super.setListAllHql(TASK_HQL, "GET_TASK_HQL");
	}
}
'''

service = '''
package com.fortigofreight.tms.service;

public interface TaskService extends FmService<Task>{

}
'''

service_impl = '''
package com.fortigofreight.tms.service;

public class TaskServiceImpl extends GenericFmService<Task> implements TaskService {

}
'''

resource = '''
package com.fortigofreight.tms.rest;

@Component
@Path("/task")
public class TaskResource extends GenericFmRestResource<Task, GENERIC_TYPE>{

}
'''

spring = '''
    <!-- Task -->

 	<bean id="taskDao" class="com.fortigofreight.tms.dao.TaskDaoImpl">
 		<property name="sessionFactory" ref="sessionFactory"></property>
    	<property name="entityClass" value="com.fortigofreight.tms.domain.Task"></property>
    	<property name="iniFile" ref="iniFile"></property>
 	</bean>
 	<bean id="taskService" class="com.fortigofreight.tms.service.TaskServiceImpl">
 	    <property name="fmDao" ref="taskDao"></property>
 	</bean>
 	<bean id="taskResource" class="com.fortigofreight.tms.rest.TaskResource">
 	    <property name="fmService" ref="taskService"></property>
    	<property name="entityClass" value="com.fortigofreight.tms.domain.Task"></property>
	    <property name="catalog" value="Fortigo_TMS"></property>
	    <property name="schema" value="dbo"></property>
	    <property name="table" value="TABLE_NAME"></property>
    </bean>
'''

constants = {
    'dao': dao,
    'dao_impl': daoImpl,
    'service': service,
    'service_impl': service_impl,
    'resource': resource
}

def get(tmplName, tableName):
    x = constants[tmplName]
    x = helper.replaceTask(x, tableName)
    x = x.replace('GENERIC_TYPE', input.primary_key_java_type)
    return x

def getXml(tableName, sql_table_name, schema=None, catalog=None):
    x = spring
    x = helper.replaceTask(x, tableName)
    x = x.replace('TABLE_NAME', sql_table_name)
    return x
