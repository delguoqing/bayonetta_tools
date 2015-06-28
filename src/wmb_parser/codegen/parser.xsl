<?xml version="1.0"?>

<!DOCTYPE stylesheet[
<!ENTITY space "<xsl:text> </xsl:text>">
<!ENTITY cr "<xsl:text>
</xsl:text>">
<!ENTITY sep "<xsl:text/>">
<!ENTITY e2 "<xsl:text>
		</xsl:text>">
]>

<xsl:stylesheet	xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
		xmlns:exsl="http://exslt.org/common"
		extension-element-prefixes="exsl"
		version="1.0">

<xsl:import href="basics.xsl"/>

<!-- parser -->	
<xsl:template match="format">
<exsl:document href="g_{/format/@name}_parser_{/format/@ver}.py" method="text">
	
<xsl:variable name="root" select="/"/>

<xsl:text># -*- coding: utf-8</xsl:text>
# g_<xsl:value-of select="@name"/>_parser_<xsl:value-of select="@ver"/>.py
#
# This file is generated by format/parser.xsl
# DO NOT MODIFY
#
import struct
import numpy
import sys
import six
from six import b
if sys.version_info[0] == 3:
	buffer = memoryview&sep;

<xsl:for-each select="./*[@base_module]"><xsl:text>
</xsl:text>
	<xsl:call-template name="import_base_module"/>
</xsl:for-each>

############################
# declaring all custom types
############################&sep;
<xsl:for-each select="./type">
# -- <xsl:value-of select="@typename"/>
<xsl:if test="@comment">
# <xsl:value-of select="@comment"/>
</xsl:if>
class cls_<xsl:value-of select="@typename"/>(<xsl:call-template name="base"/>):	
	def __init__(self, f<xsl:call-template select="." name="unpack_args"/>):&sep;
		super(cls_<xsl:value-of select="@typename"/>, self).__init__()
		<xsl:for-each select="./*">
		<xsl:if test="@comment">
		# <xsl:value-of select="@comment"/>
		</xsl:if><xsl:text>
		</xsl:text>
		<xsl:apply-templates select="." mode="declare_and_load">
			<xsl:with-param name="root" select="exsl:node-set($root)"/>
		</xsl:apply-templates>
		</xsl:for-each>
		<xsl:if test="@log='1'">
		if self.need_log(): print (repr(self))&sep;
		</xsl:if>
		
	@staticmethod
	def get_unit_size():
		return sum((&sep;
			<xsl:for-each select="./*">
				<xsl:apply-templates select="." mode="size"/>, &sep;
			</xsl:for-each>
		&sep;))&sep;
	def need_log(self):
		return <xsl:for-each select="./*[@log]">
		<xsl:choose>
			<xsl:when test="@log='1'">
				&sep;True or &sep;
			</xsl:when>
			<xsl:otherwise>
				&sep;False or &sep;
			</xsl:otherwise>
		</xsl:choose>
		</xsl:for-each>False
	def __repr__(self):
		return ";".join([
		<xsl:for-each select="./*">
		<xsl:if test="@log='1'">
		&e2;	"<xsl:value-of select="@name"/>=%s" % repr(self.<xsl:value-of select="@name"/>),
		</xsl:if>
		</xsl:for-each>
		&sep;])
</xsl:for-each>
	
##################################
# helpers for analyze file format
##################################
coverage = {}
value_statistic = {}
def add_value_statistic(k, v):
	dic = value_statistic.setdefault(k, {})
	dic[v] = dic.get(v, 0) + 1
	
def print_value_statistic():
	for k, v_set in value_statistic.iteritems():
		print (k, ":")
		for v, v_count in v_set.iteritems():
			print ("\t", v, ":%d" % v_count)
			
if __name__ == "__main__":&sep;
<xsl:for-each select="./type">
	<xsl:if test="@assert_size='1'">
	assert cls_<xsl:value-of select="@typename"/>.get_unit_size() == <xsl:value-of select="@size"/>, "in cls_<xsl:value-of select="@typename"/>: size assert failed!!! 0x%x" % cls_<xsl:value-of select="@typename"/>.get_unit_size()&e2;
	</xsl:if>			
</xsl:for-each>
	pass
</exsl:document>
</xsl:template>

</xsl:stylesheet>