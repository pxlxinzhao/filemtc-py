import re
import helper
import input
import constant
import java_type


class FilemtcBuilder:
    def __init__(self):
        self.sTable = ""
        self.jTable = ""
        self.sFields = []
        self.jFields = []

        l = re.findall('\[[\w]+\]', input.sql)
        self.sFields = map(helper.trim, l[0:-3])
        self.sTable = helper.trim(l[-1])

        self.writer = FileIO()


    def write_hql(self):
        hql_name = 'GET_' + helper.make_alias(self.sTable) + '_HQL'
        r = hql_name + '=\nselect\n'

        for field in self.sFields:
            r += helper.camel_case(field) + ' as ' + helper.make_alias(field) + ',\n'
            self.jFields.append(helper.camel_case(field))

        r = r[:-2]

        r += '\nfrom ' + helper.make_alias(self.sTable)
        r += '\n[SQL END]'

        self.jTable = helper.make_alias(self.sTable)

        self.writer.write(hql_name, r)

    def write_domain(self):
        domain = "package com.fortigofreight.tms.domain;\n"
        domain += "@Entity\n"
        domain += "@Table(name = \"" + self.sTable + "\")\n"
        domain += "public class " + self.jTable + " implements Serializable {\n"
        domain += "private static final long serialVersionUID = 1L;\n"
        domain += "@Id\n"
        domain += "@GeneratedValue(strategy = GenerationType.IDENTITY)\n"

        size = len(self.jFields)
        i = 0

        while i < size:
            domain += "@Column(name = \"" + self.sFields[i] + "\")\n"
            domain += "private String " + self.jFields[i] + ";\n"
            i += 1

        domain += "}\n"

        path = input.paths[java_type.domain] + '\\' + self.jTable + '.java'
        with open(path, 'w+') as f:
            f.write(domain)
            print "created " + path
            f.close()

    def write_xml(self):
        with open(input.xmlPath, 'r+') as f:
            l = list(f)
            index = -1
            dao_name = helper.deCapitalize(self.jTable) + "Dao"

            for i, line in enumerate(l):
                if line.find("id=\"" + dao_name + "\"") > -1:
                    print 'trying to update ' + input.xmlPath + ', but dao ' + dao_name + ' already exists, not overriding'
                    return
                if line.find("</beans>") > -1:
                    index = i
                    break

            l1 = l[:index]
            l2 = l[index]

            l1.append(constant.getXml(self.jTable, self.sTable))

            if isinstance(l2, basestring):
                l1.append('\n' + l2)
            else:
                l1 = l1 + l2

            f.close()

            with open(input.xmlPath, 'w+') as fw:
                for l in l1:
                    fw.write(str(l))
                print 'created ' + input.xmlPath
                fw.close()


    def build_dao_service_resource(self):
        self.writer.write_java(self, java_type.dao)
        self.writer.write_java(self, java_type.dao_impl)
        self.writer.write_java(self, java_type.service)
        self.writer.write_java(self, java_type.service_impl)
        self.writer.write_java(self, java_type.resource)

    def build_jsp_js(self):
        files = input.front_end_files
        for file in files:
            with open(file, 'r') as fin:
                data = fin.readlines()
                fin.close()
                newPath = helper.replaceTask(file, self.jTable)
                with open(newPath, 'w+') as fout:
                    for line in data:
                        fout.write(helper.replaceTask(line, self.jTable))
                    print 'created ' + newPath
                    fout.close()

    def print_sql(self):
        print helper.replaceTask(input.update_container, self.jTable)
        print helper.replaceTask(input.update_menu, self.jTable)

class FileIO:
    def __init__(self):
        self.end_tag = "[END SQL STATEMENTS]"

    def write(self, hql_name, hql):
        with open(input.scriptPath, 'r+') as f:
            l = list(f)
            index = -1
            for i, line in enumerate(l):
                if line.find(hql_name) > -1:
                    print 'trying to update ' + input.scriptPath + ',' + ' but hql ' + hql_name + ' already exists, not overriding'

                    return
                if line.find(self.end_tag) > -1:
                    index = i
                    break

            l1 = l[:index]
            l2 = l[index]

            l1.append(hql)

            if isinstance(l2, basestring):
                l1.append('\n' + l2)
            else:
                l1 = l1 + l2

            # print l1

            f.close()

            with open(input.scriptPath, 'w+') as fw:
                for l in l1:
                    fw.write(str(l))

                print "created " + input.scriptPath
                fw.close()

    def write_java(self, builder, java_class_type):
        table_name = builder.jTable
        full_path = input.paths[java_class_type] + '\\' + table_name + helper.make_alias(java_class_type) + '.java'

        with open(full_path, 'w+') as f1:
            f1.write(constant.get(java_class_type, table_name))
            print "created " + full_path
            f1.close()



