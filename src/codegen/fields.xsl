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
	
<!-- generate field strings -->	
<xsl:template match="format">
<exsl:document href="g_fields_{/format/@name}_{/format/@ver}.py" method="text">
DATA = {
<xsl:for-each select="./*[@base_module]">
"<xsl:value-of select="@typename"/>": set((&sep;
	<xsl:for-each select="./*[@name]">
		<xsl:call-template select="." name="field_name"/>,&sep;
	</xsl:for-each>)),&sep;
</xsl:for-each>
}
</exsl:document>
</xsl:template>

<xsl:template name="field_name">
&sep;"<xsl:value-of select="@name"/>"&sep;
</xsl:template>
</xsl:stylesheet>